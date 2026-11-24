# Notebook source: notebooks/aitest/GroupXX_DMI_2627_Preprocessing.ipynb

## Cell 0 (markdown)
# Student data preprocessing

GroupXX ? Data Mining I ? 2026/2027

Group members and student numbers must be completed before submission.

This standalone notebook prepares a working dataset from the recorded-value
exploration. Run from `notebooks/` using Python and pandas. Input is
`../data/raw/student_data.csv`. The processed CSV is written to
`../outputs/student_data_preprocessed.csv` when the export cell runs.

## Treatment rationale

| Feature group | Treatment | Decision status |
|---|---|---|
| Failures and absences | Fill blanks with zero | User-confirmed assumption |
| Yes/No features | Represent blanks as Unknown | User-directed, 14 November 2026 |
| Recorded grades | Retain recorded values, including zeros | User-confirmed |
| Family size | Exclude from this draft dataset | Carried from submission, requires methodological review |
| School | Observed mode | Carried from submission, requires review |
| Sex and address | U and Unidentified respectively | Carried from submission, requires review |
| Parent status, jobs, reason, guardian | Unknown category | Carried from submission, requires review |
| Parental education | Observed mode, preserving literal None | Carried from submission, requires review |
| Travel time | Median within school and address, overall fallback | Draft grouped treatment |
| Study time | Median within school, overall fallback | Draft grouped treatment |
| Ratings | Observed median, checked against valid levels | Draft treatment from submission |

The family-size exclusion and remaining draft methods are candidate choices
for review and clustering sensitivity checks. Source confirmation that blank
counts represent zero remains pending. Family membership, zero travel times,
and grade zeros require interpretation with the limitations identified in EDA.

## Course patterns

Working copies, duplicate checks, and filling follow Practical 2,
`Data_Preprocessing.ipynb`, cells 18, 27, 79 and 81, and the solved exercise,
cell 54. Grouped `transform('median')`, row-preservation assertions, and CSV
round-trip checks extend those examples for this project. Cell references are
zero-based and include Markdown cells.

## Cell 1 (markdown)
## Environment

Record package versions for reproducibility. This notebook uses pandas for
loading, explicit filling, comparisons, and export.

## Cell 2 (code)
import sys
from pathlib import Path
import pandas as pd
from IPython.display import display

print('Python', sys.version.split()[0])
print('pandas', pd.__version__)

## Cell 3 (markdown)
## Load the recorded dataset

Preserve the education category "None" while parsing empty CSV fields as missing.
The exported row index is excluded from the analytical features.

## Cell 4 (code)
data = pd.read_csv(
    '../data/raw/student_data.csv',
    keep_default_na=False,
    na_values=['']
)
student_data = data.drop(columns=['Unnamed: 0'])
student_data_clean = student_data.copy()
raw_snapshot = student_data.copy()
print('Recorded dataset shape', student_data.shape)
display(pd.DataFrame({
    'Missing': student_data.isna().sum(),
    'Missing (%)': student_data.isna().mean() * 100
}).round(2))

## Cell 5 (markdown)
## Duplicate records

Evaluate duplicates across the analytical features before imputation. Matching
records are counted for review. Distinct students can share recorded attributes.

## Cell 6 (code)
duplicate_count = student_data.duplicated().sum()
print('Duplicate rows before preprocessing', duplicate_count)

## Cell 7 (markdown)
## Feature groups

Explicit lists identify the fields receiving each treatment. School, address,
parental education, binary responses, and ordered ratings have distinct meanings.

## Cell 8 (code)
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]
rating_columns = ['famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health']
education_columns = ['Medu', 'Fedu']
context_columns = ['Pstatus', 'Mjob', 'Fjob', 'reason', 'guardian']
grade_columns = ['G1', 'G2', 'G3']

## Cell 9 (markdown)
## Previous failures and absences

Apply the agreed assumption that blank entries represent zero occurrences.
This assumption is retained explicitly because its source meaning is unverified.
Observed positive counts provide the comparison for the filling checks.

## Cell 10 (code)
count_columns = ['failures', 'absences']
for column in count_columns:
    student_data_clean[column] = student_data_clean[column].fillna(0)

display(pd.DataFrame({
    'Missing before': student_data[count_columns].isna().sum(),
    'Missing after': student_data_clean[count_columns].isna().sum(),
    'Zeros after': student_data_clean[count_columns].eq(0).sum()
}))

## Cell 11 (markdown)
## Missing Yes/No responses and the affected students

Each Yes/No feature has fewer than 5% missing responses, but the affected rows
are spread across features. The current CSV contains 140 students with at least
one missing Yes/No response, representing 21.57% of all students. Mode filling
would assign at least one assumed answer to each of those students.

Missing responses receive the explicit category `Unknown`. This preserves their
uncertainty in the prepared dataset. A later clustering sensitivity experiment
can replace these entries with the mode in a separate copy. The observed modes
are recorded below to support that experiment.

Adding Unknown changes the categorical representation used by clustering.
Its effect should be assessed alongside the alternative mode treatment.

## Cell 12 (code)
missing_yes_no = student_data[yes_no_columns].isna().any(axis=1)
display(pd.DataFrame({
    'Students': [missing_yes_no.sum()],
    'Students (%)': [missing_yes_no.mean() * 100]
}, index=['At least one missing Yes/No response']).round(2))

binary_modes = pd.Series(index=yes_no_columns, dtype='str')
for column in yes_no_columns:
    observed_categories = set(student_data[column].dropna().unique())
    assert observed_categories.issubset({'yes', 'no'})
    binary_modes[column] = student_data[column].mode().iloc[0]
    student_data_clean[column] = student_data_clean[column].fillna('Unknown')

display(pd.DataFrame({
    'Missing before': student_data[yes_no_columns].isna().sum(),
    'Unknown after': student_data_clean[yes_no_columns].eq('Unknown').sum(),
    'Observed mode for later experiments': binary_modes
}))

## Cell 13 (markdown)
## Family-size treatment for this draft

The exploration identified zero family sizes and questionable combinations with
parental status. Household membership remains uncertain. This draft carries over
the submission notebook's choice to exclude family size. The feature-selection
choice requires review and can be revisited in later experiments.

## Cell 14 (code)
student_data_clean = student_data_clean.drop(columns=['famsize'])
print('Shape after family-size exclusion', student_data_clean.shape)

## Cell 15 (markdown)
## School, residence, and family context

Carry over the submission's candidate treatments for these nominal fields.
School uses its observed mode. Missing sex and address use the labels U and
Unidentified. Remaining contextual blanks use Unknown. The labels describe
missing information and supply no inferred personal circumstances.

## Cell 16 (code)
school_mode = student_data['school'].mode().iloc[0]
student_data_clean['school'] = student_data_clean['school'].fillna(school_mode)
student_data_clean['sex'] = student_data_clean['sex'].fillna('U')
student_data_clean['address'] = student_data_clean['address'].fillna('Unidentified')

for column in context_columns:
    student_data_clean[column] = student_data_clean[column].fillna('Unknown')

display(student_data_clean[['school', 'sex', 'address'] + context_columns].isna().sum().to_frame('Missing after'))

## Cell 17 (markdown)
## Parental education

The literal None category is an observed education response. Genuine blanks
receive the observed column mode as a draft imputation strategy. When modes tie,
the first value returned by pandas is used. The category counts allow review of
both the added responses and the preserved None category.

## Cell 18 (code)
education_fill = pd.Series(index=education_columns, dtype='str')
for column in education_columns:
    education_fill[column] = student_data[column].mode().iloc[0]
    student_data_clean[column] = student_data_clean[column].fillna(education_fill[column])

display(pd.DataFrame({
    'Missing before': student_data[education_columns].isna().sum(),
    'Fill category': education_fill,
    'Literal None before': student_data[education_columns].eq('None').sum(),
    'Literal None after': student_data_clean[education_columns].eq('None').sum()
}))

## Cell 19 (markdown)
## Travel and study time

Travel time is filled using the median among students with the same recorded
school and address. Study time uses the recorded-school median. Group statistics
are calculated from observed source values. If a group has no observed median,
the corresponding overall median is used as a fallback.

`transform('median')` returns a group median aligned to each student's row.
Recorded zero travel times and high study times remain part of the observations.

## Cell 20 (code)
travel_group_median = student_data.groupby(
    ['school', 'address'], dropna=False
)['traveltime'].transform('median')
study_group_median = student_data.groupby(
    'school', dropna=False
)['studytime'].transform('median')

student_data_clean['traveltime'] = (
    student_data_clean['traveltime']
    .fillna(travel_group_median)
    .fillna(student_data['traveltime'].median())
)
student_data_clean['studytime'] = (
    student_data_clean['studytime']
    .fillna(study_group_median)
    .fillna(student_data['studytime'].median())
)

display(pd.DataFrame({
    'Missing before': student_data[['traveltime', 'studytime']].isna().sum(),
    'Missing after': student_data_clean[['traveltime', 'studytime']].isna().sum()
}))

## Cell 21 (markdown)
## Ordered ratings

Fill missing ratings with each feature's observed median as a draft strategy.
The current medians are valid response levels. The check requires every selected
median to belong to the 1-5 scale, since a median can be fractional in other data.

## Cell 22 (code)
rating_medians = student_data[rating_columns].median()
assert rating_medians.isin([1, 2, 3, 4, 5]).all()
for column in rating_columns:
    student_data_clean[column] = student_data_clean[column].fillna(rating_medians[column])

display(pd.DataFrame({
    'Missing before': student_data[rating_columns].isna().sum(),
    'Median used': rating_medians,
    'Missing after': student_data_clean[rating_columns].isna().sum()
}))

## Cell 23 (markdown)
## Validate the prepared dataset

Check row identities, completeness, valid ratings, preserved recorded values, and
unchanged grades. Duplicates introduced by filling are reported for review.
The feature comparison counts all changed entries, including filled blanks.

## Cell 24 (code)
assert student_data_clean.index.equals(student_data.index)
assert len(student_data_clean) == len(student_data)
assert student_data_clean.isna().sum().sum() == 0
assert student_data_clean[rating_columns].isin([1, 2, 3, 4, 5]).all().all()
pd.testing.assert_frame_equal(student_data, raw_snapshot)
pd.testing.assert_frame_equal(student_data_clean[grade_columns], student_data[grade_columns])

for column in student_data_clean.columns:
    observed = student_data[column].notna()
    pd.testing.assert_series_equal(
        student_data_clean.loc[observed, column],
        student_data.loc[observed, column],
        check_dtype=False
    )

print('Prepared shape', student_data_clean.shape)
print('Remaining missing entries', student_data_clean.isna().sum().sum())
print('Duplicate rows after preprocessing', student_data_clean.duplicated().sum())
display(pd.DataFrame({
    'Missing before': student_data[student_data_clean.columns].isna().sum(),
    'Missing after': student_data_clean.isna().sum()
}))

## Cell 25 (markdown)
## Export and reload check

Save the prepared values with their source row identifiers. The index named
student_row_id is an exported row identifier and should be excluded from model
features. Preserve the literal None category when reloading this CSV.

## Cell 26 (code)
output_path = Path('../outputs/student_data_preprocessed.csv')
output_path.parent.mkdir(parents=True, exist_ok=True)
student_data_clean.to_csv(output_path, index=True, index_label='student_row_id')

reloaded = pd.read_csv(
    output_path,
    index_col='student_row_id',
    keep_default_na=False,
    na_values=['']
)
expected = student_data_clean.rename_axis('student_row_id')
pd.testing.assert_frame_equal(reloaded, expected, check_dtype=False)
print('Saved and verified', output_path.as_posix())

## Cell 27 (markdown)
## Preprocessing conclusion

The prepared dataset retains all 649 source rows and has 32 features after the
candidate family-size exclusion. Missing failures and absences become zero under
the agreed assumption. Missing Yes/No responses remain identifiable as Unknown,
affecting 140 students with at least one such response.

Draft treatments for other fields are documented above and require review before
final model selection. Recorded grades are preserved, including the student with
G1 = 0, G2 = 11, G3 = 11. Validation checks confirm completeness, preserved
observations, row alignment, and a successful export/reload comparison.

For later clustering experiments, create a separate copy and replace Unknown
entries in the eight Yes/No features with the modes calculated from recorded
responses. Compare resulting cluster profiles and stability. Feature encoding,
scaling, and model selection require their own justified decisions.
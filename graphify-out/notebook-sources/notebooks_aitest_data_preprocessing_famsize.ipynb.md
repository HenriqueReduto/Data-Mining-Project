# Notebook source: notebooks/aitest/data_preprocessing_famsize.ipynb

## Cell 0 (markdown)
# Data preprocessing — retain and estimate family size

This independent variant retains `famsize` and applies the provisional scenario
evaluated in `data_exploration_famsize.ipynb`. All other existing treatments are
carried over. Run from the project root or `notebooks/`; requires pandas and NumPy.
Outputs go to `outputs/famsize_scenario/`, separately from the existing pipeline.
Assistant execution does not verify the selected VS Code kernel.


## Cell 1 (markdown)
### Environment check

The Python interpreter, version, working directory, and pandas version
are displayed to record the execution environment.

## Cell 2 (code)
import sys
import os
import pandas as pd
from pathlib import Path

print(sys.executable)
print(sys.version)
print(os.getcwd())
print(pd.__version__)

## Cell 3 (markdown)
### Data loading and initial dimensions

The CSV is loaded into the DataFrame `data`.
The loading options preserve the literal education category "None"
while treating empty fields as missing values.

The imported dataset contains 649 rows and 34 columns.
One column is an exported row index, so these are not 34 analytical features.

## Cell 4 (code)
from pathlib import Path
project_root = Path.cwd().resolve()
if not (project_root / 'data/raw/student_data.csv').exists():
    project_root = project_root.parent
assert (project_root / 'data/raw/student_data.csv').exists(), 'Open the project root or notebooks directory.'
data = pd.read_csv(
    project_root / 'data/raw/student_data.csv',
    keep_default_na=False,
    na_values=['']
)
student_data = data.drop(columns=['Unnamed: 0'])
assert len(student_data) == len(data)
data.shape

## Cell 5 (markdown)
### Student variables

The exported row index is excluded to create the table of student
variables used for preprocessing.

## Cell 6 (code)
student_data = data.drop(columns=['Unnamed: 0'])

student_data.shape

## Cell 7 (markdown)
### Missing values before preprocessing

Missing counts and percentages are recorded before applying the selected treatment.

## Cell 8 (code)
missing_counts = data.isna().sum()
missing_percentages = (missing_counts / len(data) * 100).round(2)

missing_summary = pd.DataFrame({
    'Missing count': missing_counts,
    'Missing (%)': missing_percentages
})

missing_summary

## Cell 9 (markdown)
### Treatment of missing absences and failures

A working copy of the dataset is created for preprocessing.
Missing absences and previous failures are replaced with zero,
assuming that blanks represent no absences or failures.
This interpretation remains subject to source confirmation.

## Cell 10 (code)
student_data_clean = student_data.copy()

student_data_clean['absences'] = student_data_clean['absences'].fillna(0)
student_data_clean['failures'] = student_data_clean['failures'].fillna(0)

## Cell 11 (markdown)
### Validation of zero replacement

Before-and-after counts verify the replacement of missing absences and failures with zero.

## Cell 12 (code)
replacement_check = pd.DataFrame({
    'Missing before': student_data[['absences', 'failures']].isna().sum(),
    'Missing after': student_data_clean[['absences', 'failures']].isna().sum(),
    'Zeros after': student_data_clean[['absences', 'failures']].eq(0).sum()
})

replacement_check

## Cell 13 (markdown)
### Row preservation and remaining missing values

Row counts and order are checked after filling. Remaining missing values
are displayed for later preprocessing decisions.

## Cell 14 (code)
assert student_data_clean.shape == student_data.shape
assert student_data_clean.index.equals(student_data.index)
assert student_data_clean[['absences', 'failures']].isna().sum().sum() == 0

student_data_clean.isna().sum()

## Cell 15 (markdown)
### Order of remaining treatments

Remaining missing values are sorted from most to least frequent.
Variables are treated in this order, and variables of the same type
share one treatment.

## Cell 16 (code)
remaining_missing = student_data_clean.isna().sum()

remaining_missing = remaining_missing[remaining_missing > 0].sort_values(
    ascending=False
)

remaining_missing

## Cell 17 (markdown)
### Treatment of missing Yes/No responses

The eight Yes/No features contain between 1 (`romantic`) and 31
(`paid`, `activities`) missing responses. Missing responses are recorded
as a separate "Unknown" category, so no answer is guessed for a student.

`data_exploration.ipynb` (Missing-value overlap in Yes/No features) shows
that missing responses rarely occur together. Of the 140 students missing
at least one Yes/No response, 135 are missing exactly one, and the largest
pairwise overlap involves two students. "Unknown" therefore marks
individual unanswered questions rather than a group of students who left
the questionnaire incomplete.

"Unknown" adds a third level to each Yes/No feature. This must be
considered when the features are encoded.

## Cell 18 (code)
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

for column in yes_no_columns:
    student_data_clean[column] = student_data_clean[column].fillna('Unknown')

## Cell 19 (markdown)
### Validation of Yes/No replacement

Before-and-after counts verify that every missing response became
"Unknown" and that recorded "yes" and "no" answers are unchanged.

## Cell 20 (code)
yes_no_check = pd.DataFrame({
    'Missing before': student_data[yes_no_columns].isna().sum(),
    'Missing after': student_data_clean[yes_no_columns].isna().sum(),
    'Unknown after': student_data_clean[yes_no_columns].eq('Unknown').sum()
})

assert student_data_clean[yes_no_columns].eq('yes').sum().equals(
    student_data[yes_no_columns].eq('yes').sum()
)
assert student_data_clean[yes_no_columns].eq('no').sum().equals(
    student_data[yes_no_columns].eq('no').sum()
)

yes_no_check

## Cell 21 (markdown)
### Study time by school

Missing study times are counted by school, and the median study time of
each school is calculated from recorded values. Every student with a
missing study time has a recorded school.

## Cell 22 (code)
study_by_school = pd.DataFrame({
    'Missing studytime': student_data_clean.loc[
        student_data_clean['studytime'].isna(), 'school'
    ].value_counts(),
    'Median studytime': student_data_clean.groupby('school')['studytime'].median()
})

study_by_school

## Cell 23 (markdown)
### Treatment of missing study time

GP students report more weekly study time than MS students, so a single
overall median would understate study time at GP and overstate it at MS.
Each missing value is replaced with the median of the student's school.
The median is used because study time is strongly right-skewed.

`transform('median')` returns, for every student, the median of their
school, aligned with the original rows. `fillna` uses that value only
where study time is missing.

## Cell 24 (code)
school_study_median = student_data_clean.groupby('school')['studytime'].transform('median')

student_data_clean['studytime'] = student_data_clean['studytime'].fillna(school_study_median)

## Cell 25 (markdown)
### Validation of study-time replacement

The filled values are displayed by school. The checks confirm that no
study time is missing and that recorded values are unchanged.

## Cell 26 (code)
filled_study = student_data_clean.loc[
    student_data['studytime'].isna(),
    ['school', 'studytime']
]

assert student_data_clean['studytime'].isna().sum() == 0
assert student_data_clean['studytime'].where(
    student_data['studytime'].notna()
).equals(student_data['studytime'])

filled_study.value_counts()

## Cell 27 (markdown)
### Travel time by school and residence

Missing travel times are counted by school and residence type, and the
median travel time of each combination is calculated from recorded values.
Every student with a missing travel time has a recorded school and
residence. `data_exploration.ipynb` (Travel time, residence, and school)
shows that rural students travel longer than urban students within both
schools.

## Cell 28 (code)
travel_by_group = pd.DataFrame({
    'Missing traveltime': student_data_clean.loc[
        student_data_clean['traveltime'].isna(), ['school', 'address']
    ].value_counts(),
    'Median traveltime': student_data_clean.groupby(
        ['school', 'address']
    )['traveltime'].median()
})

travel_by_group['Missing traveltime'] = (
    travel_by_group['Missing traveltime'].fillna(0).astype(int)
)

travel_by_group

## Cell 29 (markdown)
### Treatment of missing travel time

Travel time depends on the school and on where the student lives, so a
single overall median would understate rural journeys and overstate urban
ones. Each missing value is replaced with the median of students from the
same school and residence type.

## Cell 30 (code)
group_travel_median = student_data_clean.groupby(
    ['school', 'address']
)['traveltime'].transform('median')

student_data_clean['traveltime'] = student_data_clean['traveltime'].fillna(group_travel_median)

## Cell 31 (markdown)
### Validation of travel-time replacement

The filled values are displayed by school and residence. The checks
confirm that no travel time is missing and that recorded values are
unchanged.

## Cell 32 (code)
filled_travel = student_data_clean.loc[
    student_data['traveltime'].isna(),
    ['school', 'address', 'traveltime']
]

assert student_data_clean['traveltime'].isna().sum() == 0
assert student_data_clean['traveltime'].where(
    student_data['traveltime'].notna()
).equals(student_data['traveltime'])

filled_travel.value_counts()

## Cell 33 (markdown)
### Rating medians

The median of each 1–5 rating feature is calculated from recorded
responses before filling.

## Cell 34 (code)
rating_columns = [
    'famrel', 'freetime', 'goout',
    'Dalc', 'Walc', 'health'
]

rating_medians = student_data_clean[rating_columns].median()

rating_medians

## Cell 35 (markdown)
### Treatment of missing ratings

The six rating features contain between 17 (`health`) and 31 (`goout`)
missing responses. Each missing response is replaced with the median of
its feature. The median of an ordered 1–5 scale is always a valid
response level and is not affected by extreme responses.

`data_exploration.ipynb` (Missing-value overlap in rating features) shows
that missing ratings rarely occur together. Of the 129 students missing
at least one rating, 115 are missing exactly one, and the largest
pairwise overlap involves three students. Each feature can therefore be
filled separately.

## Cell 36 (code)
for column in rating_columns:
    student_data_clean[column] = student_data_clean[column].fillna(
        rating_medians[column]
    )

## Cell 37 (markdown)
### Validation of rating replacement

Before-and-after counts verify that no rating is missing, that every
filled value equals the feature median, and that recorded responses are
unchanged.

## Cell 38 (code)
rating_check = pd.DataFrame({
    'Missing before': student_data[rating_columns].isna().sum(),
    'Missing after': student_data_clean[rating_columns].isna().sum(),
    'Median used': rating_medians
})

assert student_data_clean[rating_columns].isna().sum().sum() == 0
assert student_data_clean[rating_columns].where(
    student_data[rating_columns].notna()
).equals(student_data[rating_columns])

rating_check

## Cell 39 (markdown)
### Treatment of missing categorical values

Missing parental status, parental education, parental occupation,
reason for choosing the school, and residence type are recorded as a
separate unknown category rather than guessed. The observed values give
no basis for inferring, for example, a parent's occupation or education.

- `Pstatus` uses "U", following the single-letter coding of "T"
  (together) and "A" (apart).
- The other features use "Unknown". In `address`, "U" already means
  urban, so a single letter would merge unknown residences with urban
  ones.
- In `Medu` and `Fedu`, "Unknown" remains distinct from the recorded
  level "None" (no formal education).

The unknown category has no position on the education scale. This must
be considered when parental education is encoded.

## Cell 40 (code)
student_data_clean['Pstatus'] = student_data_clean['Pstatus'].fillna('U')

unknown_columns = ['Medu', 'Fedu', 'Fjob', 'address', 'reason', 'Mjob']

for column in unknown_columns:
    student_data_clean[column] = student_data_clean[column].fillna('unknown')

## Cell 41 (markdown)
### Validation of categorical replacement

Before-and-after counts verify that every missing value became the
unknown category and that recorded categories are unchanged.

## Cell 42 (code)
category_columns = ['Pstatus'] + unknown_columns

unknown_after = student_data_clean[unknown_columns].eq('unknown').sum()
unknown_after['Pstatus'] = student_data_clean['Pstatus'].eq('U').sum()

category_check = pd.DataFrame({
    'Missing before': student_data[category_columns].isna().sum(),
    'Missing after': student_data_clean[category_columns].isna().sum(),
    'Unknown after': unknown_after
}).loc[category_columns]

assert student_data_clean[category_columns].isna().sum().sum() == 0
assert student_data_clean[category_columns].where(
    student_data[category_columns].notna()
).equals(student_data[category_columns])

category_check

## Cell 43 (markdown)
### Treatment of missing sex

Ten students have no recorded sex. The missing values are recorded as a
separate category, "U", rather than assigned to the more frequent
category. Following the single-letter coding of "F" and "M", "U" marks
an unknown value, as in `Pstatus`.

## Cell 44 (code)
student_data_clean['sex'] = student_data_clean['sex'].fillna('U')

## Cell 45 (markdown)
### Validation of sex replacement

Category counts before and after filling are compared.

## Cell 46 (code)
sex_check = pd.DataFrame({
    'Before': student_data['sex'].value_counts(dropna=False),
    'After': student_data_clean['sex'].value_counts(dropna=False)
}).fillna(0).astype(int)

assert student_data_clean['sex'].isna().sum() == 0

sex_check

## Cell 47 (markdown)
### Treatment of missing guardian

Eight students have no recorded guardian. The missing values are replaced
with the most frequent guardian (the mode). Mothers are the recorded
guardian for most students, and eight values are too few to change the
distribution meaningfully.

## Cell 48 (code)
guardian_mode = student_data_clean['guardian'].mode()[0]

student_data_clean['guardian'] = student_data_clean['guardian'].fillna(guardian_mode)

## Cell 49 (markdown)
### Validation of guardian replacement

Guardian counts before and after filling are compared.

## Cell 50 (code)
guardian_check = pd.DataFrame({
    'Before': student_data['guardian'].value_counts(dropna=False),
    'After': student_data_clean['guardian'].value_counts(dropna=False)
}).fillna(0).astype(int)

assert student_data_clean['guardian'].isna().sum() == 0

guardian_check

## Cell 51 (markdown)
### Family-size scenario and source boundaries

The user reports that the student is excluded from `famsize`, and that the
professor advised correcting questionable values instead of dropping the feature.
We retain the feature and preserve every recorded positive value, including 1.
Zero is treated as an unknown count **for this provisional scenario**; living
alone is not ruled out by these data. Guardian and parental status do not prove
co-residence. Therefore we do not force `Pstatus = T` to imply a size of 2.

We estimate zero/missing values from positive recorded sizes grouped by recorded
`Pstatus` and `guardian`. Missing grouping keys remain missing until explicitly
labelled for matching; we do not use imputed guardians as observed evidence.
Fallback order is joint-group median, parental-status median, then overall
median. No minimum group-size threshold has been approved; group counts and
spread are displayed for review. Donor values are plausible observations, not
independently verified household counts. Fractional estimates are rounded to
the nearest integer, with halves rounded upward, because this is a people count.
These are transparent candidate rules, not reconstructed household facts.

`Medu` and `Fedu` provide context only: education does not establish residence,
and literal `None` denotes no education rather than an absent parent.
Grouped imputation may reinforce associations with parental status/guardian;
review sensitivity before using the feature in clustering.

Course adaptations: `memory/course-reference/exploration.md` (P1 cells 89, 91:
group summaries) and `memory/course-reference/preprocessing.md` (P2 cells 79, 81:
imputation alternatives; P2 cells 56–58: before/after checks). The lab archives
and `memory/prior-experiments.md` are absent in this checkout, so cited source
cells could not be re-inspected. These notes do not establish that the proposed
grouping or zero treatment was prescribed by the course.


## Cell 52 (markdown)
### Check duplicate student records

Exclude the exported row index and count duplicate records. This check does not delete students.


## Cell 53 (code)
duplicate_count = student_data.duplicated().sum()
print('Duplicate records:', int(duplicate_count))


## Cell 54 (markdown)
### Inspect family-size donors from recorded values

Use the raw-loaded `student_data`, not already filled parental/guardian values, to build comparison groups.


## Cell 55 (code)
family_donors = student_data.loc[
    student_data['famsize'].ge(1), ['famsize', 'Pstatus', 'guardian']
].copy()
family_donors['Pstatus'] = family_donors['Pstatus'].fillna('Missing')
family_donors['guardian'] = family_donors['guardian'].fillna('Missing')
family_donor_summary = family_donors.groupby(['Pstatus', 'guardian'])['famsize'].agg(
    ['count', 'median', 'min', 'max']
)
assert len(family_donors) + student_data['famsize'].eq(0).sum() + student_data['famsize'].isna().sum() == len(student_data)
family_donor_summary


## Cell 56 (markdown)
### Estimate a candidate family size

Join medians to each student using recorded grouping keys. `.fillna` implements the stated fallback order. Add 0.5 and take the floor to round positive half-values upward. The original table stays unchanged.


## Cell 57 (code)
import numpy as np

family_candidates = student_data[['famsize', 'Pstatus', 'guardian']].copy()
family_candidates['Pstatus'] = family_candidates['Pstatus'].fillna('Missing')
family_candidates['guardian'] = family_candidates['guardian'].fillna('Missing')
joint_medians = family_donors.groupby(['Pstatus', 'guardian'])['famsize'].median()
status_medians = family_donors.groupby('Pstatus')['famsize'].median()
family_candidates = family_candidates.join(joint_medians.rename('Joint median'), on=['Pstatus', 'guardian'])
family_candidates['Status median'] = family_candidates['Pstatus'].map(status_medians)
family_candidates['Overall median'] = family_donors['famsize'].median()
family_candidates['Estimate'] = family_candidates['Joint median'].fillna(
    family_candidates['Status median']
).fillna(family_candidates['Overall median'])
family_candidates['Method'] = 'Joint-group median'
family_candidates.loc[family_candidates['Joint median'].isna(), 'Method'] = 'Parental-status median'
family_candidates.loc[
    family_candidates['Joint median'].isna() & family_candidates['Status median'].isna(), 'Method'
] = 'Overall median'
family_candidates['Proposed'] = np.floor(family_candidates['Estimate'] + 0.5)
family_target = student_data['famsize'].eq(0) | student_data['famsize'].isna()
family_candidates.loc[~family_target, 'Proposed'] = student_data.loc[~family_target, 'famsize']
family_candidates.loc[~family_target, 'Method'] = 'Recorded value retained'
assert family_candidates['Proposed'].notna().all()
assert family_candidates.loc[~family_target, 'Proposed'].equals(student_data.loc[~family_target, 'famsize'])
family_candidates.loc[family_target].groupby(['Pstatus', 'guardian', 'Proposed', 'Method']).size().rename('Rows').to_frame()


## Cell 58 (markdown)
### Review changes before adoption

Compare recorded and candidate distributions and the number of affected students. Only zero/missing values are targets; education and guardian values are not inferred from family size.


## Cell 59 (code)
family_audit = pd.DataFrame({
    'Original': student_data['famsize'],
    'Proposed': family_candidates['Proposed'],
    'Method': family_candidates['Method'],
    'Targeted': family_target
}, index=student_data.index)
family_distribution = pd.DataFrame({
    'Recorded': student_data['famsize'].value_counts(dropna=False),
    'Candidate': family_candidates['Proposed'].value_counts(dropna=False)
}).fillna(0).astype(int)
assert family_audit.loc[~family_target, 'Original'].equals(family_audit.loc[~family_target, 'Proposed'])
assert student_data.loc[student_data['famsize'].eq(1), 'famsize'].eq(1).all()
print('Targeted rows:', int(family_target.sum()))
family_distribution.sort_index()


## Cell 60 (markdown)
### Apply the candidate and validate preservation

Assign only the candidate family-size Series. Check positive recorded sizes, all other features, row identities, completeness and integer counts. This is a scenario export, not final methodological approval.


## Cell 61 (code)
before_family_treatment = student_data_clean.copy()
student_data_clean['famsize'] = family_candidates['Proposed']
pd.testing.assert_frame_equal(
    student_data_clean.drop(columns=['famsize']),
    before_family_treatment.drop(columns=['famsize'])
)
assert student_data_clean.index.equals(student_data.index)
assert student_data_clean.shape == student_data.shape
assert student_data_clean['famsize'].ge(1).all()
assert student_data_clean['famsize'].mod(1).eq(0).all()
assert student_data_clean.loc[~family_target, 'famsize'].equals(student_data.loc[~family_target, 'famsize'])
student_data_clean.shape


## Cell 62 (markdown)
### Treatment of missing school

One student has no recorded school. The value is replaced with the most
frequent school (the mode). With a single missing value, this has no
meaningful effect on the distribution. `.mode()` returns a Series because
several values can tie, so `[0]` selects the first.

## Cell 63 (code)
school_mode = student_data_clean['school'].mode()[0]

student_data_clean['school'] = student_data_clean['school'].fillna(school_mode)

## Cell 64 (markdown)
### Validation of school replacement

School counts before and after filling are compared.

## Cell 65 (code)
school_check = pd.DataFrame({
    'Before': student_data['school'].value_counts(dropna=False),
    'After': student_data_clean['school'].value_counts(dropna=False)
}).fillna(0).astype(int)

assert student_data_clean['school'].isna().sum() == 0

school_check

## Cell 66 (markdown)
### Remaining missing values

After all treatments, no missing values should remain in the working
dataset.

## Cell 67 (code)
assert student_data_clean.isna().sum().sum() == 0

student_data_clean.shape

## Cell 68 (markdown)
### Working dataset

The prepared table is available as `student_data_clean` in this notebook.
Missing failures and absences are interpreted as zero by user decision.
The source meaning of those blanks remains unconfirmed. Missing Yes/No
responses are recorded as "Unknown". Missing study times are replaced
with the median of the student's school, and missing travel times with
the median of the student's school and residence type. Missing ratings
are replaced with the median of each feature. Missing parental status and
sex are recorded as "U"; missing parental education, parental occupation,
reason, and residence are recorded as "Unknown". Missing guardians and the
missing school are replaced with the mode. `famsize` is retained with the provisional group-median estimates documented above. Further treatments require an explicit decision.
Duplicate records are evaluated above.

## Cell 69 (markdown)
### Save the prepared dataset

The processed-data folder is created if needed, then the prepared dataset
is saved with its source row identifier.

## Cell 70 (code)
output_folder = project_root / 'outputs/famsize_scenario'
output_folder.mkdir(parents=True, exist_ok=True)
output_path = output_folder / 'student_data_preprocessed_famsize.csv'
student_data_clean.to_csv(output_path, index=True, index_label='student_row_id')
family_audit.to_csv(output_folder / 'famsize_correction_audit.csv', index=True, index_label='student_row_id')
reloaded = pd.read_csv(output_path, index_col='student_row_id', keep_default_na=False, na_values=[''])
assert reloaded.shape == student_data_clean.shape
assert reloaded.index.equals(student_data_clean.index)
pd.testing.assert_frame_equal(reloaded.rename_axis(student_data_clean.index.name), student_data_clean, check_dtype=False)
print(output_path)
print('Prepared rows and features:', student_data_clean.shape)
print('Family-size estimates:', int(family_target.sum()))
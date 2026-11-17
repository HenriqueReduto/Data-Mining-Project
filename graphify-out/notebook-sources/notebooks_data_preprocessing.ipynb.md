# Notebook source: notebooks/data_preprocessing.ipynb

Source-only extract; outputs omitted. Cell numbers are zero-based.

## Cell 0 (markdown)
# Data preprocessing

Evaluate duplicate records and apply the approved missing-value treatment.
Exploratory findings are documented in `data_exploration.ipynb`.

Run this notebook from the `notebooks/` directory with Python and pandas installed. The input is `../data/raw/student_data.csv`. Each notebook loads the input independently. The previous user environment used Python 3.14.10 and pandas 3.1.1. Execution outputs below record the validation runtime.

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
data = pd.read_csv(
    '../data/raw/student_data.csv',
    keep_default_na=False,
    na_values=['']
)

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
### Exclusion of family size

`famsize` is excluded from the working dataset.

- **The values are unreliable.** 57 students have a family size of 0 and
  31 more have a family size of 1 while living with both parents. These
  88 inconsistent records (13.56%), together with 3 missing values, affect
  91 students (14.02%).
- **The errors cannot be corrected.** No other feature records the number
  of family members, so a correct value cannot be derived for these
  students. Replacing 91 values would introduce invented data, and it is
  unclear whether the remaining values count the student, the household,
  or the wider family.
- **Little information is lost.** In `data_exploration.ipynb` (Correlation
  between numerical features), `famsize` has a correlation of −0.06 with
  the final grade. Family context remains represented by `Pstatus`,
  `guardian`, `famrel`, and `famsup`.

Because the feature is excluded, its 3 missing values require no
treatment.

## Cell 52 (code)
student_data_clean = student_data_clean.drop(columns=['famsize'])

student_data_clean.shape

## Cell 53 (markdown)
### Validation of family-size exclusion

The checks confirm that `famsize` is no longer present, that only that
column was removed, and that every student is retained.

## Cell 54 (code)
assert 'famsize' not in student_data_clean.columns
assert list(student_data_clean.columns) == list(
    student_data.columns.drop('famsize')
)
assert student_data_clean.index.equals(student_data.index)

## Cell 55 (markdown)
### Treatment of missing school

One student has no recorded school. The value is replaced with the most
frequent school (the mode). With a single missing value, this has no
meaningful effect on the distribution. `.mode()` returns a Series because
several values can tie, so `[0]` selects the first.

## Cell 56 (code)
school_mode = student_data_clean['school'].mode()[0]

student_data_clean['school'] = student_data_clean['school'].fillna(school_mode)

## Cell 57 (markdown)
### Validation of school replacement

School counts before and after filling are compared.

## Cell 58 (code)
school_check = pd.DataFrame({
    'Before': student_data['school'].value_counts(dropna=False),
    'After': student_data_clean['school'].value_counts(dropna=False)
}).fillna(0).astype(int)

assert student_data_clean['school'].isna().sum() == 0

school_check

## Cell 59 (markdown)
### Remaining missing values

After all treatments, no missing values should remain in the working
dataset.

## Cell 60 (code)
assert student_data_clean.isna().sum().sum() == 0

student_data_clean.shape

## Cell 61 (markdown)
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
missing school are replaced with the mode. `famsize` is excluded because
of inconsistent values. Further treatments require an explicit decision.
Duplicate records are evaluated above.

## Cell 62 (markdown)
### Save the prepared dataset

The processed-data folder is created if needed, then the prepared dataset
is saved with its source row identifier.

## Cell 63 (code)
output_path = Path('../data/processed/student_data_preprocessed.csv')
output_path.parent.mkdir(parents=True, exist_ok=True)

student_data_clean.to_csv(
    output_path,
    index=True,
    index_label='student_row_id'
)

print(output_path.resolve())
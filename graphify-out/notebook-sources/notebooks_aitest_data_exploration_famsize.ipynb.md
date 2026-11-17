# Notebook source: notebooks/aitest/data_exploration_famsize.ipynb

Source-only extract; outputs omitted. Cell numbers are zero-based.

## Cell 0 (markdown)
# Data exploration — family-size retention scenario

Inspect recorded values and evaluate a candidate correction while retaining family size.
This separate variant preserves the existing exploration notebook. Run from the
project root or `notebooks/`. Requires pandas, NumPy, Matplotlib and Seaborn.
Assistant execution, if recorded, does not verify the selected VS Code kernel.


## Cell 1 (markdown)
### Environment check

The Python interpreter, version, working directory, and pandas version
are displayed to record the execution environment.

## Cell 2 (code)
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Cell 3 (markdown)
### Data loading and initial dimensions

The CSV is loaded into the DataFrame `data`.
The loading options preserve the literal education category "None"
while treating empty fields as missing values.

A table of student variables is created by excluding the exported row index.

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
### Inspect the next result

Run this small follow-up step using the variables above. Check the resulting counts, categories, or dimensions before interpreting them.


## Cell 6 (code)
student_data = data.drop(columns=['Unnamed: 0'])

student_data.shape

## Cell 7 (markdown)
---

## Cell 8 (markdown)
### Duplicate records

Records are checked for identical values across the student variables.
The exported row index is excluded because its unique values could
hide otherwise identical records.

## Cell 9 (code)
duplicate_count = student_data.duplicated().sum()

duplicate_count

## Cell 10 (markdown)
---

## Cell 11 (markdown)
### Missing-value analysis

Missing values are counted for each column to assess data completeness.
The distribution of recorded values is also inspected, including missing
entries, to support later preprocessing decisions.

## Cell 12 (code)
missing_counts = student_data.isna().sum()
missing_percentages = (missing_counts / len(student_data) * 100).round(2)

missing_summary = pd.DataFrame({
    'Missing count': missing_counts,
    'Missing (%)': missing_percentages
})

missing_summary

## Cell 13 (markdown)
### Students with at least one missing value

The number and percentage of students with at least one missing value
are calculated across the features, excluding absences and previous failures.

## Cell 14 (code)
features_to_check = student_data.drop(columns=['absences', 'failures'])

rows_with_missing = features_to_check.isna().any(axis=1)

missing_rows_summary = pd.DataFrame({
    'Students': [rows_with_missing.sum()],
    'Percentage (%)': [rows_with_missing.mean() * 100]
}, index=['At least one missing value'])

display(missing_rows_summary.round(2))

## Cell 15 (markdown)
### Column types and structure

Inspect each column's stored data type and number of non-missing
values before reviewing variable roles and distributions.

## Cell 16 (code)
student_data.info()

## Cell 17 (markdown)
### Numerical summary

Summary statistics are inspected to understand the distribution and
range of numerical columns and identify values requiring investigation.

## Cell 18 (code)
student_data.describe()

## Cell 19 (markdown)
### Categorical summary

Categorical columns are inspected to identify the number of distinct
categories, the most frequent category, and its frequency.

## Cell 20 (code)
student_data.describe(include=['object', 'string']).T

## Cell 21 (markdown)
---

## Cell 22 (markdown)
### Correlation between numerical features

A Pearson correlation matrix is calculated for the numerical features
to examine the direction and strength of linear relationships.

Each coefficient uses students with recorded values for both features.
The number of observations can therefore differ between comparisons.

## Cell 23 (code)
correlation_matrix = student_data.corr(numeric_only=True)

plt.figure(figsize=(16, 12))

sns.heatmap(
    data=correlation_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    vmin=-1,
    vmax=1,
    center=0
)

plt.title('Pearson correlation between numerical features')
plt.tight_layout()
plt.show()

## Cell 24 (markdown)
### Correlation between binary and rating features

Yes/No responses are represented numerically as 1 and 0 in a separate
analysis copy. The rating features retain their existing 1–5 values.

Spearman correlations examine associations between these features.
Missing responses are excluded separately for each pair.

## Cell 25 (markdown)
### Correlation between Yes/No features

Yes/No responses are encoded as 1 and 0 in a separate analysis copy.
Pearson correlations examine associations between the binary features.
Missing responses are excluded separately for each pair.

## Cell 26 (code)
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

yes_no_numeric = student_data[yes_no_columns].copy()

yes_no_numeric = student_data[yes_no_columns].copy()

for column in yes_no_columns:
    yes_no_numeric[column] = yes_no_numeric[column].map({
        'yes': 1,
        'no': 0
    })

yes_no_correlation = yes_no_numeric.corr(method='pearson')

plt.figure(figsize=(10, 8))

sns.heatmap(
    yes_no_correlation,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    vmin=-1,
    vmax=1,
    center=0
)

plt.title('Pearson correlation between Yes/No features')
plt.tight_layout()
plt.show()

## Cell 27 (markdown)
### Correlation between rating features

Spearman correlations examine associations between the ordered
1–5 ratings. Missing responses are excluded separately for each pair.

## Cell 28 (code)
rating_columns = [
    'famrel', 'freetime', 'goout',
    'Dalc', 'Walc', 'health'
]

rating_correlation = student_data[rating_columns].corr(
    method='spearman'
)

rating_correlation = student_data[rating_columns].corr(
    method='spearman'
)

plt.figure(figsize=(9, 7))

sns.heatmap(
    rating_correlation,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    vmin=-1,
    vmax=1,
    center=0
)

plt.title('Spearman correlation between rating features')
plt.tight_layout()
plt.show()

## Cell 29 (markdown)
### Distribution of categorical features

The percentage of students in each category is displayed for every
categorical feature. Missing responses are included in the percentages.

## Cell 30 (code)
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

rating_columns = [
    'famrel', 'freetime', 'goout',
    'Dalc', 'Walc', 'health'
]

categorical_columns = student_data.select_dtypes(
    include=['string', 'object']
).columns

remaining_columns = categorical_columns.drop(yes_no_columns)

## Cell 31 (markdown)
### Inspect the next result

Run this small follow-up step using the variables above. Check the resulting counts, categories, or dimensions before interpreting them.


## Cell 32 (code)
yes_no_percentages = pd.DataFrame(index=yes_no_columns)

for column in yes_no_columns:
    yes_no_percentages.loc[column, 'Yes'] = (
        student_data[column].eq('yes').sum() / len(student_data) * 100
    )
    yes_no_percentages.loc[column, 'No'] = (
        student_data[column].eq('no').sum() / len(student_data) * 100
    )
    yes_no_percentages.loc[column, 'Missing'] = (
        student_data[column].isna().sum() / len(student_data) * 100
    )

display(yes_no_percentages.round(2))

## Cell 33 (markdown)
### Rating percentages

The percentage of students selecting each rating is displayed alongside
the percentage with missing responses.

## Cell 34 (code)
rating_percentages = pd.DataFrame(index=rating_columns)

for column in rating_columns:
    for rating in range(1, 6):
        rating_percentages.loc[column, rating] = (
            student_data[column].eq(rating).sum() / len(student_data) * 100
        )

    rating_percentages.loc[column, 'Missing'] = (
        student_data[column].isna().sum() / len(student_data) * 100
    )

display(rating_percentages.round(2))

## Cell 35 (markdown)
### Remaining categorical percentages

The remaining categorical features are displayed with one row per feature
and one column per category. Empty cells indicate categories that do not
apply to that feature.

## Cell 36 (code)
for column in remaining_columns:
    remaining_percentages = (
        student_data[column]
        .fillna('Missing')
        .value_counts(normalize=True)
        .mul(100)
        .to_frame(name=column)
        .T
    )

    display(remaining_percentages.round(2))

## Cell 37 (markdown)
---

## Cell 38 (markdown)
### Parental education and occupation

Parental education and occupation are examined together to identify
common combinations and records requiring further investigation.

## Cell 39 (code)
mother_education_job = pd.crosstab(
    student_data['Medu'].fillna('Missing'),
    student_data['Mjob'].fillna('Missing')
)

mother_education_job

## Cell 40 (markdown)
### Inspect the next result

Run this small follow-up step using the variables above. Check the resulting counts, categories, or dimensions before interpreting them.


## Cell 41 (code)
father_education_job = pd.crosstab(
    student_data['Fedu'].fillna('Missing'),
    student_data['Fjob'].fillna('Missing')
)

father_education_job

## Cell 42 (markdown)
### Parental status and guardian

Parental living arrangements are compared with the recorded guardian.

## Cell 43 (code)
parental_status_guardian = pd.crosstab(
    student_data['Pstatus'].fillna('Missing'),
    student_data['guardian'].fillna('Missing')
)

parental_status_guardian

## Cell 44 (markdown)
### Family size and parental status

Family-size values are compared with parental living arrangements.

## Cell 45 (code)
family_size_parental_status = pd.crosstab(
    student_data['famsize'].astype('string').fillna('Missing'),
    student_data['Pstatus'].fillna('Missing')
)

family_size_parental_status

## Cell 46 (markdown)
### Family size and guardian

Family-size values are compared with the recorded guardian.

## Cell 47 (code)
family_size_guardian = pd.crosstab(
    student_data['famsize'].astype('string').fillna('Missing'),
    student_data['guardian'].fillna('Missing')
)

family_size_guardian

## Cell 48 (markdown)
### Family-size 0 consistency checks

Family size 0 is examined alongside parental status and guardian information
to identify and count combinations requiring further investigation.

## Cell 49 (code)
zero_family_together = (
    (student_data['famsize'] == 0) &
    (student_data['Pstatus'] == 'T')
)

zero_family_parent_guardian = (
    (student_data['famsize'] == 0) &
    student_data['guardian'].isin(['mother', 'father'])
)

one_family_together = (
    (student_data['famsize'] == 1) &
    (student_data['Pstatus'] == 'T')
)

family_combination_counts = pd.DataFrame({
    'Combination': [
        'Family size 0 and parents together',
        'Family size 0 and parent as guardian',
        'Family size 1 and parents together'
    ],
    'Records': [
        zero_family_together.sum(),
        zero_family_parent_guardian.sum(),
        one_family_together.sum()
    ]
})

family_combination_counts

## Cell 50 (markdown)
### Interpretation under the revised family-size definition

The student is excluded from the count. Size 1 is plausible and retained.
Zeros and missing values warrant review, but guardianship and parental status
do not prove co-residence. Earlier counts of size 1 with `Pstatus = T` are
descriptive flags, not confirmed errors. Parental education does not count residents.


## Cell 51 (markdown)
---

## Cell 52 (markdown)
### Analysis of failures and absences

The distributions of previous failures and absences are inspected,
including missing entries, to investigate recorded values and the
possible meaning of blanks before deciding on a treatment.

## Cell 53 (code)
student_data['failures'].value_counts(dropna=False).sort_index()

## Cell 54 (markdown)
### Inspect the next result

Run this small follow-up step using the variables above. Check the resulting counts, categories, or dimensions before interpreting them.


## Cell 55 (code)
student_data['absences'].value_counts(dropna=False).sort_index()

## Cell 56 (markdown)
### Interpretation of missing failures and absences

`failures` contains 551 missing values (84.9%), while `absences`
contains 260 (40.1%). Both columns contain only positive recorded
counts, with no explicit zeros.

This pattern suggests that NaN may represent zero previous failures
or absences. We can adopt this interpretation and replace missing entries
with zero during preprocessing.

## Cell 57 (markdown)
---

## Cell 58 (markdown)
### Travel time, residence, and school

Travel-time distributions are compared across residence types and
schools. Zero-duration journeys are inspected to identify patterns
requiring clarification.

## Cell 59 (code)
travel_summary = student_data.groupby(
    ['school', 'address'],
    dropna=False
)['traveltime'].describe()

travel_summary

## Cell 60 (markdown)
### Zero travel times

Zero-duration journeys are counted by school and residence type.

## Cell 61 (code)
zero_travel = student_data.loc[
    student_data['traveltime'] == 0,
    ['school', 'address', 'traveltime']
]

zero_travel.groupby(
    ['school', 'address'],
    dropna=False
).size()

## Cell 62 (markdown)
### Interpretation of zero travel times

There are 29 recorded zero-minute journeys, including 24 among urban
students at GP, 1 among urban students at MS, 3 among rural students,
and 1 with missing residence information.

The concentration among urban GP students is compatible with very short journeys rounded to zero or a school-specific practice where students live in the same building. At GP it could be an error in data recording. Should be analysed further. #(!)#

## Cell 63 (markdown)
---

## Cell 64 (markdown)
### Study-time distribution

Weekly study time is inspected to identify zero values and unusually
high observations requiring further investigation.

## Cell 65 (code)
student_data['studytime'].describe()

## Cell 66 (markdown)
### Study-time intervals

Zero and missing study times are counted separately.
Positive study times are grouped into 100-minute intervals
to inspect their distribution.

## Cell 67 (code)
study_intervals = pd.cut(
    student_data['studytime'],
    bins=range(0, 1501, 100)
)

study_counts = study_intervals.value_counts().sort_index()

study_summary = pd.DataFrame({
    'Students': study_counts
})

study_summary.loc['Zero study time', 'Students'] = (
    student_data['studytime'].eq(0).sum()
)

study_summary.loc['Missing', 'Students'] = (
    student_data['studytime'].isna().sum()
)

study_summary


## Cell 68 (markdown)
---

## Cell 69 (markdown)
### Yes/No variables

Response frequencies are inspected for educational support,
activities, aspirations, internet access, and personal background.
Missing responses are included to assess completeness.

## Cell 70 (code)
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

yes_no_summary = pd.DataFrame(
    index=yes_no_columns,
    columns=['Yes', 'No', 'Missing']
)

for column in yes_no_columns:
    yes_no_summary.loc[column, 'Yes'] = student_data[column].eq('yes').sum()
    yes_no_summary.loc[column, 'No'] = student_data[column].eq('no').sum()
    yes_no_summary.loc[column, 'Missing'] = student_data[column].isna().sum()

yes_no_summary

## Cell 71 (markdown)
### Students with missing rating responses

Students with at least one missing response across the six rating
features are counted, together with their percentage of the dataset.

## Cell 72 (code)
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

missing_yes_no = student_data[yes_no_columns].isna().any(axis=1)

yes_no_missing_summary = pd.DataFrame({
    'Students': [missing_yes_no.sum()],
    'Percentage (%)': [missing_yes_no.mean() * 100]
}, index=['At least one missing Yes/No response'])

display(yes_no_missing_summary.round(2))

## Cell 73 (markdown)
### Missing-value overlap in Yes/No features

Students with missing responses in each pair of Yes/No features
are counted to examine how often unanswered fields occur together.

## Cell 74 (code)
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

missing_indicators = student_data[yes_no_columns].isna().astype(int)

missing_overlap = missing_indicators.T.dot(missing_indicators)

missing_overlap

## Cell 75 (markdown)
### Interpretation of missing-value overlap

Missing responses in the Yes/No features rarely occur together.
Of the 140 students missing at least one response, 135 are missing
exactly one and 5 are missing two or more.

The largest pairwise overlaps involve only two students, between
`schoolsup` and `paid`, and between `famsup` and `nursery`.
This suggests that missing responses are mostly scattered across
students.

## Cell 76 (markdown)
---

## Cell 77 (markdown)
### Rating-value counts

Responses from 1 to 5 and missing entries are counted for each
rating feature to examine their distributions and completeness.

## Cell 78 (code)
rating_columns = [
    'famrel', 'freetime', 'goout',
    'Dalc', 'Walc', 'health'
]

rating_summary = pd.DataFrame(
    index=rating_columns,
    columns=[1, 2, 3, 4, 5, 'Missing']
)

for column in rating_columns:
    for rating in range(1, 6):
        rating_summary.loc[column, rating] = (
            student_data[column].eq(rating).sum()
        )

    rating_summary.loc[column, 'Missing'] = (
        student_data[column].isna().sum()
    )

rating_summary

## Cell 79 (markdown)
### Students with missing rating responses

Students with at least one missing response across the six rating
features are counted, together with their percentage of the dataset.

## Cell 80 (code)
rating_columns = [
    'famrel', 'freetime', 'goout',
    'Dalc', 'Walc', 'health'
]

missing_ratings = student_data[rating_columns].isna().any(axis=1)

rating_missing_summary = pd.DataFrame({
    'Students': [missing_ratings.sum()],
    'Percentage (%)': [missing_ratings.mean() * 100]
}, index=['At least one missing rating response'])

display(rating_missing_summary.round(2))

## Cell 81 (markdown)
### Missing-value overlap in rating features

Students with missing responses in each pair of rating features
are counted to examine how often unanswered fields occur together.

## Cell 82 (code)
rating_missing_indicators = (
    student_data[rating_columns].isna().astype(int)
)

rating_missing_overlap = (
    rating_missing_indicators.T.dot(rating_missing_indicators)
)

rating_missing_overlap

## Cell 83 (markdown)
### Interpretation of missing-value overlap

Missing responses rarely overlap across the six rating features.
The largest pairwise overlap involves three students missing both
`goout` and `Walc`. All other pairs share at most two missing responses.

These counts suggest limited overlap in unanswered ratings.

## Cell 84 (markdown)
---

## Cell 85 (markdown)
### Grade distributions

The three grade features are examined through summary statistics and
frequency counts. Missing values and recorded zeros are counted separately.

## Cell 86 (code)
grade_columns = ['G1', 'G2', 'G3']

display(student_data[grade_columns].describe())

grade_counts = pd.DataFrame({
    column: student_data[column].value_counts()
    for column in grade_columns
}).sort_index()

display(grade_counts)


## Cell 87 (markdown)
### Students with zero grades

Students with a zero in any grading period are examined across all three
periods to identify when zeros occur and whether they persist.

## Cell 88 (code)
zero_grade_students = student_data.loc[
    student_data[grade_columns].eq(0).any(axis=1),
    ['G1', 'G2', 'G3', "absences"]
]

display(zero_grade_students)

## Cell 89 (markdown)
### Grade analysis conclusion

The student with G1 = 0, G2 = 11, and G3 = 11 shows that a zero in the
first period can be followed by positive grades. However, every student
with G2 = 0 also had G3 = 0.

The reason for the recorded zeros remains unknown. The individual student could be retained
because there is insufficient evidence that it is an error.

## Cell 90 (markdown)
---

## Cell 91 (markdown)
## Exploration findings before the family-size scenario

### Dataset structure and completeness

The dataset contains 649 students and 33 analytical features after excluding
the exported row index. No exact duplicate records were identified across
these features.

The variables cover demographic characteristics, family background,
educational support, study habits, social behaviour, health, and academic
performance. Students range from 15 to 22 years old.

Age and all three grade variables are complete. Every other feature contains
missing entries, with particularly high missingness in `failures`
(551 students, 84.9%) and `absences` (260 students, 40.1%). Consequently,
preprocessing decisions for these two features will affect a substantial
proportion of the dataset.

### Family information and questionable combinations

Family size presents the clearest unresolved interpretation problem.
There are 57 students with a recorded family size of zero. Among them,
41 have parents recorded as living together and 53 have a mother or father
as their guardian. A further 31 students have family size one and parents
living together. These groups overlap and should be interpreted separately.

This variant uses the user-supplied definition excluding the student. Size 1 is retained; zero/missing values are examined in the scenario below. Household membership remains uncertain.

### Missing failures and absences

Both `failures` and `absences` contain positive recorded counts and no
explicit zeros. This pattern supports the hypothesis that blanks may
represent zero occurrences.

The adopted preprocessing decision is to replace missing entries in these
two features with zero. This remains an explicit analytical assumption,
as the exploration cannot confirm how the blanks were generated.

### Travel and study time

Travel time has a median of 13 minutes, with recorded values ranging from
0 to 144 minutes. Within both schools, rural students have longer median
journeys than urban students.

There are 29 zero-minute journeys, including 24 among urban students at GP.
This concentration warrants investigation. Very short journeys rounded to
zero and differences in recording practices are possible explanations,
but the available comparisons cannot establish the cause.

Weekly study time has a median of 186 minutes and a mean of approximately
242 minutes. The higher mean and maximum of 1,465 minutes indicate a
distribution extending towards high study times. There are 502 students
reporting positive study times of up to 300 minutes, alongside three
recorded zeros and 14 missing entries.

### Yes/No features

The response counts show that aspirations for higher education, nursery
attendance, and internet access are common. Family educational support is
also frequently reported. School support and paid additional classes are
less common, while participation in extracurricular activities is more
evenly divided.

Missing responses rarely overlap within these eight features. The largest
pairwise overlaps involve two students. This indicates limited shared
missingness across the features examined, although the reason for unanswered
responses remains unknown.

### Rating features

All recorded values in the six rating features fall within the expected
1–5 range. Family relationships are concentrated at ratings 4 and 5,
while free time and going out most frequently receive rating 3.

Workday alcohol consumption is concentrated at rating 1. Weekend consumption
has more responses at higher ratings. Health responses span the full scale,
with rating 5 the most frequent.

Missing-value overlap is also limited across these features. The largest
pairwise overlap involves three students missing both `goout` and `Walc`.
All other pairs share at most two missing responses.

### Academic performance

All three grade features contain 649 observations and range from 0 to 19.
Mean grades increase from approximately 11.40 in G1 to 11.57 in G2 and
11.91 in G3. The medians are 11, 11, and 12 respectively. These summaries
show a modest increase in performance across periods at the dataset level.

There is one zero in G1, seven in G2, and fifteen in G3. The student at
index 0 has G1 = 0, G2 = 11, and G3 = 11, demonstrating that an initial
zero can be followed by positive grades. Every student with G2 = 0 also
has G3 = 0.

The causes of these zeros remain uncertain. They are retained because
the exploration provides insufficient evidence that they are recording
errors.

### Implications for preprocessing and clustering

The exploration identifies differences in feature scales, incomplete
responses, uneven category frequencies, and unresolved values that require
documented preprocessing decisions.

Family-size coding remains an important open issue. The zero-fill treatment
for missing failures and absences must remain documented as an assumption.
Travel-time zeros, high study times, and zero grades require interpretation
consistent with the available evidence.

The findings provide a basis for preparing the data for clustering.
Cluster selection and interpretation will require further analysis of
relationships between features and validation of the resulting groups.

## Cell 92 (markdown)
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


## Cell 93 (markdown)
### Family-size groups and percentages

Create display groups without changing recorded values. `.loc` assigns labels to selected rows; percentages use all students as the denominator.


## Cell 94 (code)
family_groups = pd.Series('2 or more', index=student_data.index)
family_groups.loc[student_data['famsize'].eq(0)] = '0'
family_groups.loc[student_data['famsize'].eq(1)] = '1'
family_groups.loc[student_data['famsize'].isna()] = 'Missing'
family_counts = family_groups.value_counts().reindex(['0', '1', 'Missing', '2 or more'], fill_value=0)
family_summary = pd.DataFrame({'Rows': family_counts, 'Percentage': (100 * family_counts / len(student_data)).round(2)})
assert family_counts.sum() == len(student_data)
family_summary


## Cell 95 (markdown)
### Parental status and guardian by family-size group

`pd.crosstab` counts combinations. Missing labels are for display, not imputed household evidence. Each table must total the number of students.


## Cell 96 (code)
parent_status_labels = student_data['Pstatus'].fillna('Missing')
guardian_labels = student_data['guardian'].fillna('Missing')
family_context_counts = pd.crosstab(
    family_groups, [parent_status_labels, guardian_labels], dropna=False
)
assert family_context_counts.to_numpy().sum() == len(student_data)
family_context_counts


## Cell 97 (markdown)
### Medu across family-size groups

Compare recorded education, retaining literal `None` separately from missing entries. These counts do not identify household residents.


## Cell 98 (code)
pd.crosstab(family_groups, student_data['Medu'].fillna('Missing'))


## Cell 99 (markdown)
### Fedu across family-size groups

Compare recorded education, retaining literal `None` separately from missing entries. These counts do not identify household residents.


## Cell 100 (code)
pd.crosstab(family_groups, student_data['Fedu'].fillna('Missing'))


## Cell 101 (markdown)
### Inspect positive-size comparison groups

Use sizes of at least 1 as candidate donors, including valid size-1 records. `.agg` shows support and spread; a small group or wide range weakens confidence in its median.


## Cell 102 (code)
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


## Cell 103 (markdown)
### Estimate a candidate family size

Join medians to each student using recorded grouping keys. `.fillna` implements the stated fallback order. Add 0.5 and take the floor to round positive half-values upward. The original table stays unchanged.


## Cell 104 (code)
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


## Cell 105 (markdown)
### Review changes before adoption

Compare recorded and candidate distributions and the number of affected students. Only zero/missing values are targets; education and guardian values are not inferred from family size.


## Cell 106 (code)
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


## Cell 107 (markdown)
### Next teaching step

Inspect donor counts, ranges, and proposed changes. Explain why a median is an
estimate rather than a recovered count. Review the zero-as-unknown assumption,
fallback order, rounding, and sensitivity before adopting this scenario for modelling.
The companion `data_preprocessing_famsize.ipynb` applies the same candidate rule
and exports a separate dataset and audit trail.

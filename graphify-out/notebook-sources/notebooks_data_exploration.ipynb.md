# Notebook source notebooks/data_exploration.ipynb


## Cell 0 (markdown)

# Data exploration

Inspect recorded values, distributions, missingness, and relationships.
Missing entries remain visible in the analysis.

Run this notebook from the `notebooks/` directory with Python and pandas installed. The input is `../data/raw/student_data.csv`. Each notebook loads the input independently. The previous user environment used Python 3.14.10 and pandas 3.1.1. Execution outputs below record the validation runtime.


## Cell 1 (markdown)

### Environment check

The Python interpreter, version, working directory, and pandas version
are displayed to record the execution environment.


## Cell 2 (code)

```python
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```


## Cell 3 (markdown)

### Data loading and initial dimensions

The CSV is loaded into the DataFrame `data`.
The loading options preserve the literal education category "None"
while treating empty fields as missing values.

A table of student variables is created by excluding the exported row index.


## Cell 4 (code)

```python
data = pd.read_csv(
    '../data/raw/student_data.csv',
    keep_default_na=False,
    na_values=['']
)
```


## Cell 5 (code)

```python
student_data = data.drop(columns=['Unnamed: 0'])

student_data.shape
```


## Cell 6 (markdown)

---


## Cell 7 (markdown)

### Duplicate records

Records are checked for identical values across the student variables.
The exported row index is excluded because its unique values could
hide otherwise identical records.


## Cell 8 (code)

```python
duplicate_count = student_data.duplicated().sum()

duplicate_count
```


## Cell 9 (markdown)

---


## Cell 10 (markdown)

### Missing-value analysis

Missing values are counted for each column to assess data completeness.
The distribution of recorded values is also inspected, including missing
entries, to support later preprocessing decisions.


## Cell 11 (code)

```python
missing_counts = student_data.isna().sum()
missing_percentages = (missing_counts / len(student_data) * 100).round(2)

missing_summary = pd.DataFrame({
    'Missing count': missing_counts,
    'Missing (%)': missing_percentages
})

missing_summary
```


## Cell 12 (markdown)

### Column types and structure

Inspect each column's stored data type and number of non-missing
values before reviewing variable roles and distributions.


## Cell 13 (code)

```python
student_data.info()
```


## Cell 14 (markdown)

### Numerical summary

Summary statistics are inspected to understand the distribution and
range of numerical columns and identify values requiring investigation.


## Cell 15 (code)

```python
student_data.describe()
```


## Cell 16 (markdown)

### Categorical summary

Categorical columns are inspected to identify the number of distinct
categories, the most frequent category, and its frequency.


## Cell 17 (code)

```python
student_data.describe(include=['str']).T
```


## Cell 18 (markdown)

---


## Cell 19 (markdown)

### Correlation between numerical features

A Pearson correlation matrix is calculated for the numerical features
to examine the direction and strength of linear relationships.

Each coefficient uses students with recorded values for both features.
The number of observations can therefore differ between comparisons.


## Cell 20 (code)

```python
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
```


## Cell 21 (markdown)

### Correlation between binary and rating features

Yes/No responses are represented numerically as 1 and 0 in a separate
analysis copy. The rating features retain their existing 1–5 values.

Spearman correlations examine associations between these features.
Missing responses are excluded separately for each pair.


## Cell 22 (markdown)

### Correlation between Yes/No features

Yes/No responses are encoded as 1 and 0 in a separate analysis copy.
Pearson correlations examine associations between the binary features.
Missing responses are excluded separately for each pair.


## Cell 23 (code)

```python
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
```


## Cell 24 (markdown)

### Correlation between rating features

Spearman correlations examine associations between the ordered
1–5 ratings. Missing responses are excluded separately for each pair.


## Cell 25 (code)

```python
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
```


## Cell 26 (markdown)

### Distribution of categorical features

The percentage of students in each category is displayed for every
categorical feature. Missing responses are included in the percentages.


## Cell 27 (code)

```python
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

rating_columns = [
    'famrel', 'freetime', 'goout',
    'Dalc', 'Walc', 'health'
]

categorical_columns = student_data.select_dtypes(
    include=['str', 'object']
).columns

remaining_columns = categorical_columns.drop(yes_no_columns)
```


## Cell 28 (code)

```python
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
```


## Cell 29 (markdown)

### Rating percentages

The percentage of students selecting each rating is displayed alongside
the percentage with missing responses.


## Cell 30 (code)

```python
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
```


## Cell 31 (markdown)

### Remaining categorical percentages

The remaining categorical features are displayed with one row per feature
and one column per category. Empty cells indicate categories that do not
apply to that feature.


## Cell 32 (code)

```python
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
```


## Cell 33 (markdown)

---


## Cell 34 (markdown)

### Parental education and occupation

Parental education and occupation are examined together to identify
common combinations and records requiring further investigation.


## Cell 35 (code)

```python
mother_education_job = pd.crosstab(
    student_data['Medu'].fillna('Missing'),
    student_data['Mjob'].fillna('Missing')
)

mother_education_job
```


## Cell 36 (code)

```python
father_education_job = pd.crosstab(
    student_data['Fedu'].fillna('Missing'),
    student_data['Fjob'].fillna('Missing')
)

father_education_job
```


## Cell 37 (markdown)

### Parental status and guardian

Parental living arrangements are compared with the recorded guardian.


## Cell 38 (code)

```python
parental_status_guardian = pd.crosstab(
    student_data['Pstatus'].fillna('Missing'),
    student_data['guardian'].fillna('Missing')
)

parental_status_guardian
```


## Cell 39 (markdown)

### Family size and parental status

Family-size values are compared with parental living arrangements.


## Cell 40 (code)

```python
family_size_parental_status = pd.crosstab(
    student_data['famsize'].astype('string').fillna('Missing'),
    student_data['Pstatus'].fillna('Missing')
)

family_size_parental_status
```


## Cell 41 (markdown)

### Family size and guardian

Family-size values are compared with the recorded guardian.


## Cell 42 (code)

```python
family_size_guardian = pd.crosstab(
    student_data['famsize'].astype('string').fillna('Missing'),
    student_data['guardian'].fillna('Missing')
)

family_size_guardian
```


## Cell 43 (markdown)

### Family-size 0 consistency checks

Family size 0 is examined alongside parental status and guardian information
to identify and count combinations requiring further investigation.


## Cell 44 (code)

```python
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
```


## Cell 45 (markdown)

### Questionable family-size combinations

Several combinations raise questions about the meaning of `famsize`.

- **Family size 0 with parents living together — 41 records.**
  A family containing the student and both parents would contain three or at
  least two people, if they share the household and are included
  in the count.

- **Family size 0 with a parent as guardian — 53 records.**
  The recorded family size excludes everyone, despite identifying
  a mother or father as responsible for the student.

- **Family size 1 with parents living together — 31 records.**
  This count is too small to include the student or only both parents
  if they live in the same household.

Parental status and guardianship do not establish household membership,
but these combinations make the family-size values questionable.


## Cell 46 (markdown)

---


## Cell 47 (markdown)

### Analysis of failures and absences

The distributions of previous failures and absences are inspected,
including missing entries, to investigate recorded values and the
possible meaning of blanks before deciding on a treatment.


## Cell 48 (code)

```python
student_data['failures'].value_counts(dropna=False).sort_index()
```


## Cell 49 (code)

```python
student_data['absences'].value_counts(dropna=False).sort_index()
```


## Cell 50 (markdown)

### Interpretation of missing failures and absences

`failures` contains 551 missing values (84.9%), while `absences`
contains 260 (40.1%). Both columns contain only positive recorded
counts, with no explicit zeros.

This pattern suggests that NaN may represent zero previous failures
or absences. We can adopt this interpretation and replace missing entries
with zero during preprocessing.


## Cell 51 (markdown)

---


## Cell 52 (markdown)

### Travel time, residence, and school

Travel-time distributions are compared across residence types and
schools. Zero-duration journeys are inspected to identify patterns
requiring clarification.


## Cell 53 (code)

```python
travel_summary = student_data.groupby(
    ['school', 'address'],
    dropna=False
)['traveltime'].describe()

travel_summary
```


## Cell 54 (markdown)

### Zero travel times

Zero-duration journeys are counted by school and residence type.


## Cell 55 (code)

```python
zero_travel = student_data.loc[
    student_data['traveltime'] == 0,
    ['school', 'address', 'traveltime']
]

zero_travel.groupby(
    ['school', 'address'],
    dropna=False
).size()
```


## Cell 56 (markdown)

### Interpretation of zero travel times

There are 29 recorded zero-minute journeys, including 24 among urban
students at GP, 1 among urban students at MS, 3 among rural students,
and 1 with missing residence information.

The concentration among urban GP students is compatible with very short journeys rounded to zero or a school-specific practice where students live in the same building. At GP it could be an error in data recording. Should be analysed further. #(!)#


## Cell 57 (markdown)

---


## Cell 58 (markdown)

### Study-time distribution

Weekly study time is inspected to identify zero values and unusually
high observations requiring further investigation.


## Cell 59 (code)

```python
student_data['studytime'].describe()
```


## Cell 60 (markdown)

### Study-time intervals

Zero and missing study times are counted separately.
Positive study times are grouped into 100-minute intervals
to inspect their distribution.


## Cell 61 (code)

```python
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

```


## Cell 62 (markdown)

---


## Cell 63 (markdown)

### Yes/No variables

Response frequencies are inspected for educational support,
activities, aspirations, internet access, and personal background.
Missing responses are included to assess completeness.


## Cell 64 (code)

```python
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
```


## Cell 65 (markdown)

### Students with missing rating responses

Students with at least one missing response across the six rating
features are counted, together with their percentage of the dataset.


## Cell 66 (code)

```python
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
```


## Cell 67 (markdown)

### Missing-value overlap in Yes/No features

Students with missing responses in each pair of Yes/No features
are counted to examine how often unanswered fields occur together.


## Cell 68 (code)

```python
yes_no_columns = [
    'schoolsup', 'famsup', 'paid', 'activities',
    'nursery', 'higher', 'internet', 'romantic'
]

missing_indicators = student_data[yes_no_columns].isna().astype(int)

missing_overlap = missing_indicators.T.dot(missing_indicators)

missing_overlap
```


## Cell 69 (markdown)

### Interpretation of missing-value overlap

Missing responses in the Yes/No features rarely occur together.
Of the 140 students missing at least one response, 135 are missing
exactly one and 5 are missing two or more.

The largest pairwise overlaps involve only two students, between
`schoolsup` and `paid`, and between `famsup` and `nursery`.
This suggests that missing responses are mostly scattered across
students.


## Cell 70 (markdown)

---


## Cell 71 (markdown)

### Rating-value counts

Responses from 1 to 5 and missing entries are counted for each
rating feature to examine their distributions and completeness.


## Cell 72 (code)

```python
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
```


## Cell 73 (markdown)

### Students with missing rating responses

Students with at least one missing response across the six rating
features are counted, together with their percentage of the dataset.


## Cell 74 (code)

```python
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
```


## Cell 75 (markdown)

### Missing-value overlap in rating features

Students with missing responses in each pair of rating features
are counted to examine how often unanswered fields occur together.


## Cell 76 (code)

```python
rating_missing_indicators = (
    student_data[rating_columns].isna().astype(int)
)

rating_missing_overlap = (
    rating_missing_indicators.T.dot(rating_missing_indicators)
)

rating_missing_overlap
```


## Cell 77 (markdown)

### Interpretation of missing-value overlap

Missing responses rarely overlap across the six rating features.
The largest pairwise overlap involves three students missing both
`goout` and `Walc`. All other pairs share at most two missing responses.

These counts suggest limited overlap in unanswered ratings.


## Cell 78 (markdown)

---


## Cell 79 (markdown)

### Grade distributions

The three grade features are examined through summary statistics and
frequency counts. Missing values and recorded zeros are counted separately.


## Cell 80 (code)

```python
grade_columns = ['G1', 'G2', 'G3']

display(student_data[grade_columns].describe())

grade_counts = pd.DataFrame({
    column: student_data[column].value_counts()
    for column in grade_columns
}).sort_index()

display(grade_counts)

```


## Cell 81 (markdown)

### Students with zero grades

Students with a zero in any grading period are examined across all three
periods to identify when zeros occur and whether they persist.


## Cell 82 (code)

```python
zero_grade_students = student_data.loc[
    student_data[grade_columns].eq(0).any(axis=1),
    ['G1', 'G2', 'G3', "absences"]
]

display(zero_grade_students)
```


## Cell 83 (markdown)

### Grade analysis conclusion

The student with G1 = 0, G2 = 11, and G3 = 11 shows that a zero in the
first period can be followed by positive grades. However, every student
with G2 = 0 also had G3 = 0.

The reason for the recorded zeros remains unknown. The individual student could be retained
because there is insufficient evidence that it is an error.


## Cell 84 (markdown)

---


## Cell 85 (markdown)

## Final exploration conclusion (REMOVE)

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

If family size includes the student, zero is inconsistent with a count of
family members. Parental status and guardianship provide additional context,
although they do not establish who shares the student's household.
The meaning or recording of `famsize` therefore requires clarification
before selecting a treatment.


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

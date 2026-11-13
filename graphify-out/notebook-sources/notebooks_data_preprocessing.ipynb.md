# Notebook source notebooks/data_preprocessing.ipynb


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

```python
import sys
import os
import pandas as pd

print(sys.executable)
print(sys.version)
print(os.getcwd())
print(pd.__version__)
```


## Cell 3 (markdown)

### Data loading and initial dimensions

The CSV is loaded into the DataFrame `data`.
The loading options preserve the literal education category "None"
while treating empty fields as missing values.

The imported dataset contains 649 rows and 34 columns.
One column is an exported row index, so these are not 34 analytical features.


## Cell 4 (code)

```python
data = pd.read_csv(
    '../data/raw/student_data.csv',
    keep_default_na=False,
    na_values=['']
)

data.shape
```


## Cell 5 (markdown)

### Missing values before preprocessing

Missing counts and percentages are recorded before applying the selected treatment.


## Cell 6 (code)

```python
missing_counts = data.isna().sum()
missing_percentages = (missing_counts / len(data) * 100).round(2)

missing_summary = pd.DataFrame({
    'Missing count': missing_counts,
    'Missing (%)': missing_percentages
})

missing_summary
```


## Cell 7 (markdown)

### Treatment of missing absences and failures

A working copy of the dataset is created for preprocessing.
Missing absences and previous failures are replaced with zero,
assuming that blanks represent no absences or failures.
This interpretation remains subject to source confirmation.


## Cell 8 (code)

```python
student_data_clean = student_data.copy()

student_data_clean['absences'] = student_data_clean['absences'].fillna(0)
student_data_clean['failures'] = student_data_clean['failures'].fillna(0)
```


## Cell 9 (markdown)

### Validation of zero replacement

Before-and-after counts verify the replacement of missing absences and failures with zero.


## Cell 10 (code)

```python
replacement_check = pd.DataFrame({
    'Missing before': student_data[['absences', 'failures']].isna().sum(),
    'Missing after': student_data_clean[['absences', 'failures']].isna().sum(),
    'Zeros after': student_data_clean[['absences', 'failures']].eq(0).sum()
})

replacement_check
```


## Cell 11 (markdown)

### Row preservation and remaining missing values

Row counts and order are checked after filling. Remaining missing values
are displayed for later preprocessing decisions.


## Cell 12 (code)

```python
assert student_data_clean.shape == student_data.shape
assert student_data_clean.index.equals(student_data.index)
assert student_data_clean[['absences', 'failures']].isna().sum().sum() == 0

student_data_clean.isna().sum()
```


## Cell 13 (markdown)

### Working dataset

The prepared table is available as `student_data_clean` in this notebook.
Missing failures and absences are interpreted as zero by user decision.
The source meaning of those blanks remains unconfirmed. Further treatments
require an explicit decision. Duplicate records are evaluated above.

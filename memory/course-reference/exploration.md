# Exploration code patterns

Use this reference when proposing or reviewing exploration cells. Read the [core baseline](../course-baseline.md) for teaching rules and the exact source map. Citations such as P1 cells 42 refer to zero-based indexes in that map. Examples below adapt the lab patterns to the student dataset. They are independent teaching steps, with a short Markdown cell placed above each code cell in the notebook.

## Load and establish dimensions

Lab evidence is P1 cells 8, 10, 21 and P1S cell 5. The labs introduce imports, loading, then inspection in separate steps.

Purpose is to create the input DataFrame and establish its dimensions. Input is the supplied CSV, with the kernel working directory set to `notebooks/`.

```python
import pandas as pd

data = pd.read_csv(
    '../data/raw/student_data.csv',
    keep_default_na=False,
    na_values=['']
)

data.shape
```

Explain `import ... as ...`, assignment with `=`, quoted path strings, named arguments, and the distinction between an attribute such as `.shape` and a method such as `.head()`. Expected output is a two-element tuple of rows and columns. The audited source gives `(649, 34)` including the exported index. Verify against the current file before relying on that count. `../` resolves from the kernel's working directory.

The CSV arguments are a project adaptation that preserves literal education `None`. Default parsing in a generic lab loading example is insufficient for this source. Inspect `data.head()` in its own cell when a preview helps. Review individual-level outputs before sharing.

## Select columns and filter rows

Lab evidence is P1 Markdown cell 31, code cells 33, 35, 37, 39, and P1S cells 20–21. P1 cell 94 also demonstrates `.query()`.

```python
student_data = data.drop(columns=['Unnamed: 0'])

zero_family = student_data.loc[
    student_data['famsize'] == 0,
    ['famsize', 'Pstatus', 'guardian']
]

zero_family
```

Input is the loaded DataFrame. Output is a selected DataFrame. Explain `==` as a comparison and `.loc[rows, columns]` as selection. A single column name in brackets yields a Series, while a list of column names yields a DataFrame. Multiple boolean conditions use parentheses and `&` or `|`.

Check that removing the exported index preserves the row count and order. Check each filter's count and inspect whether missing entries were excluded by the condition. A zero family-size filter is an investigation step. Its result supplies no automatic replacement rule.

## Types, missingness, and frequencies

Lab evidence is P1 cells 42, 47, 49, 58 and P2 cells 48–51. Read the relevant explanatory Markdown around those cells when teaching a new method.

```python
missing_counts = student_data.isna().sum()
missing_percentages = (missing_counts / len(student_data) * 100).round(2)

missing_summary = pd.DataFrame({
    'Missing count': missing_counts,
    'Missing (%)': missing_percentages
})

missing_summary
```

`.isna()` produces booleans, `.sum()` counts missing entries per column, `len(...)` supplies the row denominator, and the dictionary supplies named output columns. Expected output has one row per feature. Check counts lie between zero and the row count and percentages between 0 and 100. Run `student_data.info()` separately to inspect stored types and non-null counts.

```python
student_data['Medu'].value_counts(dropna=False)
```

Expected output is a Series of category counts. Explain why `dropna=False` includes missing entries. Check the counts sum to the dataset row count and distinguish the education label `None` from missing data. Numeric storage alone does not establish a variable's measurement role. Ratings are ordinal and the exported index is an identifier.

## Numerical and categorical summaries

Lab evidence is P1 cells 47, 49 and its dtype guidance in Markdown cell 48.

```python
student_data.describe().T
```

```python
student_data.describe(include=['str']).T
```

These are separate cells. `.T` transposes the summary. The first produces count, mean, standard deviation, minimum, quartiles, and maximum for numeric columns. The second produces count, unique, top, and freq for text columns in the verified pandas 3 environment. Explain that counts use observed entries and the mode can have ties.

Check actual dtypes before selecting `str` or `object`. Numeric category codes need explicit inclusion in a categorical analysis. Inspect ranges against the assignment definitions and investigate unusual values before proposing a treatment. A mean above a median suggests asymmetry but should be considered with distribution plots.

## Grouped comparisons

Lab evidence is P1 cells 89, 91 and P1S cell 18.

```python
grade_by_school = student_data.groupby(
    'school',
    dropna=False
)['G3'].agg(['count', 'mean', 'median'])

grade_by_school
```

Input is the recorded table. Output is one summary row per school, including missing school when present. Explain grouping, selected value column, and the list of aggregation names. `count` counts observed G3 values, whereas `.size()` counts rows. Inspect denominators and missing grouping keys before interpreting group differences. Group-level associations support descriptive findings.

## Cross-tabulations as an extension

`pd.crosstab` was not found in the 12 source notebooks. It is a justified extension for the family-variable comparisons already introduced in this project.

```python
parental_status_guardian = pd.crosstab(
    student_data['Pstatus'].fillna('Missing'),
    student_data['guardian'].fillna('Missing')
)

parental_status_guardian
```

Rows represent parental status, columns represent guardian, and cells count joint occurrences. Temporary `Missing` labels retain unanswered categories in the table. Check the table total equals the input row count and confirm a label does not collide with an existing category. For numeric labels, use `.astype('string').fillna('Missing')` for display, as documented in the [preprocessing reference](preprocessing.md).

## Interpretation and completion

For each adopted section, retain its question, observed result, denominator, interpretation, and unresolved issue in short Markdown. Before handing exploration to preprocessing, account for variable roles, ranges, missingness, category validity, duplicates through the preprocessing notebook, relationships, relevant plots, and subgroup counts. Record a treatment as a decision only when the user has chosen it. Use [visualization](visualization.md) for figures and [preprocessing](preprocessing.md) for changes to values.

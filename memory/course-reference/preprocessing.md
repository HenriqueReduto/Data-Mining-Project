# Preprocessing code patterns

Use this reference in `data_preprocessing.ipynb`. Read the [core baseline](../course-baseline.md), current [decisions](../decisions.md), and [data audit](../data-audit.md) first. Source IDs and cell indexes resolve through the core baseline. Each example is a separate teaching step. Place purpose and assumption Markdown above code.

## Create a working copy

Lab evidence is P2 cells 27, 36, 41 and P4 cell 82. The labs name intermediate datasets and compare alternate treatments.

```python
student_data = data.drop(columns=['Unnamed: 0'])
student_data_clean = student_data.copy()
```

Input is the raw-loaded DataFrame. Output is a working DataFrame with the original row index. Explain method calls and assignment. Verify shape, row index, and column order before and after each coherent transformation. Read the current dataframe state before adding a copy cell later in a notebook, since recreating the copy would discard preceding treatments.

## Evaluate duplicates before removing rows

Lab evidence is P2 cells 18, 20. The lab selects duplicate records and illustrates `drop_duplicates`.

```python
duplicate_count = student_data.duplicated().sum()
duplicate_count
```

```python
duplicate_records = student_data.loc[
    student_data.duplicated(keep=False)
]

duplicate_records
```

The default `.duplicated()` flags repeats after the first occurrence. `keep=False` flags every member of a matching set. Explain those distinct counts. Exclude exported row numbers before testing, then inspect whether matching attributes could belong to distinct students. Apply deletion only after the project decision is made, and record row loss and retained identities. The earlier audit found zero duplicates.

## Apply an approved missing-value treatment

Lab evidence is P2 cells 79, 81 and P2S cells 52–54. Those cells demonstrate alternatives including constant, numeric mean, and categorical mode filling. The selected treatment for this project is recorded in `decisions.md`.

```python
student_data_clean['absences'] = student_data_clean['absences'].fillna(0)
student_data_clean['failures'] = student_data_clean['failures'].fillna(0)
```

`.fillna(0)` returns a filled Series and assignment stores it in the named column. The input is the working copy, and output is the same table with those two columns treated. Explain that zero is the user's assumption about blank counts. Source confirmation remains pending.

```python
replacement_check = pd.DataFrame({
    'Missing before': student_data[['absences', 'failures']].isna().sum(),
    'Missing after': student_data_clean[['absences', 'failures']].isna().sum(),
    'Zeros after': student_data_clean[['absences', 'failures']].eq(0).sum()
})

replacement_check
```

Check missing counts reach zero, observed non-missing entries retain their values, and row order/count remain stable. For the audited CSV, absences gains 260 zeros and failures gains 551. Recheck current source counts before stating those expectations.

Median, mode, Unknown categories, and grouped filling elsewhere are candidate methods whose adoption follows current decisions. P2S explicitly describes unknown-category handling as one possible approach. Explain `.mode()` can return multiple values before selecting a tie-breaking rule. Raw education `None` and genuinely missing education have different meanings.

## Replacements and types

Lab evidence is P2 cells 48–51, 56–58, 99 and P2S cells 29, 32, 35, 38, 41. The source demonstrates type inspection, `astype`, replacement, and before/after checks.

```python
family_size_labels = student_data['famsize'].astype('string').fillna('Missing')
family_size_labels.value_counts(dropna=False)
```

This example creates display labels for a table. `astype('string')` converts observed numbers to text and preserves missing entries until filling. Input is a numerical Series and output is a string Series. Check numerical analysis continues to use the numerical column.

Prefer explicit column reassignment when adapting source examples such as `frame['column'].replace(..., inplace=True)`. That source form needs environment-aware review under pandas copy semantics. Inspect dtype and category frequencies after a replacement. A corrected pandas idiom preserves the intended operation while making its target explicit.

## Encoding categorical features

Lab evidence is P2 cells 111–113 and P4 cells 84, 88. P2 uses `pd.get_dummies(..., drop_first=True)`. This option is a source example whose distance consequences require an explicit clustering choice.

After a user-approved feature selection and encoding decision, the pattern is to select named categorical columns, encode them, inspect the resulting names and dtypes, then preserve row identity when combining outputs. For a binary feature, dropping one indicator changes its contribution to Euclidean distance relative to keeping both. Full one-hot encoding also gives equal distances between distinct ordinal levels. Explain those effects before choosing.

Education and ratings have ordered meanings. If mapping is approved, display the mapping and check categories against its keys before applying it. A lab-style `np.where` binary mapping can send unexpected or missing categories into its fallback value. Check those cases explicitly. The source example is P2 cell 107.

## Scaling with preserved row identity

Lab evidence is P2 cells 119–129, P4 cell 17 and P4S cell 19. The labs show both separate fit/transform steps and `fit_transform`.

The following is a pattern template. `numeric_features` must contain the approved numerical model columns, and the selected data must already satisfy the estimator's input requirements.

```python
from sklearn.preprocessing import MinMaxScaler

numeric_data = student_data_clean[numeric_features].copy()
scaler = MinMaxScaler()
scaled_values = scaler.fit_transform(numeric_data)

scaled_data = pd.DataFrame(
    scaled_values,
    columns=numeric_data.columns,
    index=numeric_data.index
)
```

Explain that `.fit` learns scaling parameters, `.transform` applies them, and `.fit_transform` combines those steps. Array outputs lose pandas labels, so reconstruction supplies columns and the original index. Passing the index explicitly corrects the reconstruction pattern in the cited source cells.

Check shape, index, missingness, finite values, and ranges. Constant columns may become zero. Values transformed later can lie outside the fitted range. Keep the scaler with the feature order for inverse transformation. An imputed numeric value and scaling choice both change distances and require methodological justification.

## Derived features and exports

P2 cells 103, 105, 107 and P2S cell 58 demonstrate derived values. The date-based example uses the execution year, and the ratio examples omit a denominator check. For reproducibility, use the documented observation date and inspect zero denominators when adapting those patterns.

A CSV export is a project handoff extension. Once the working dataset is approved, document its destination, column meanings, dtypes, missingness policy, and reload options. CSV can lose types or reinterpret the education label None on reload. Verify shape, identifiers, categories, and selected values after the round trip. The proposed output path is `outputs/student_data_clean.csv`; creating this reference does not itself generate that dataset.

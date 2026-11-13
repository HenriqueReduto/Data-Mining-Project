# Notebook source notebooks/reference/datamining1.ipynb


## Cell 0 (code)

```python
#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```


## Cell 1 (code)

```python
#import data
df = pd.read_csv('student_data.csv')
```


## Cell 2 (code)

```python
#check 5 top rows
df.head()
```


## Cell 3 (code)

```python
#check all columns
df.columns
```


## Cell 4 (code)

```python
#check amount of rows and columns
df.shape
```


## Cell 5 (code)

```python
#check data types of columns and missing data
df.info()
```


## Cell 6 (code)

```python
#statistics
df.describe()
```


## Cell 7 (code)

```python
df.nunique()
```


## Cell 8 (code)

```python
df['school'].value_counts()
```


## Cell 9 (code)

```python
df['school'].unique()
```


## Cell 10 (code)

```python
display(df.describe().T)
```


## Cell 11 (code)

```python
## Preprocessing
```


## Cell 12 (code)

```python
print("Duplicate rows:", df.duplicated().sum())
```


## Cell 13 (code)

```python
missing = df.isnull().sum()
missing[missing>0]
```


## Cell 14 (code)

```python
missing_pct = (df.isnull().sum() / len(df)) * 100
missing_pct[missing_pct>0]
```


## Cell 15 (code)

```python
df = df.drop(columns=['failures'])
```


## Cell 16 (code)

```python
df.columns
```


## Cell 17 (code)

```python
plt.figure(figsize=(7, 3))
sns.boxplot(x=df['absences'], color='skyblue')
plt.title('Распределение прогулов (absences) и выбросы')
plt.xlabel('Количество прогулов')
plt.show()
```


## Cell 18 (code)

```python
#The absences variable displays extreme outliers. 
#Imputing missing values with the median (4) rather than the mean prevents these outliers from distorting the dataset.
```


## Cell 19 (code)

```python
df['absences'] = df['absences'].fillna(df['absences'].median())
```


## Cell 20 (code)

```python
missing_pct = (df.isnull().sum() / len(df)) * 100
missing_pct[missing_pct>0]
```


## Cell 21 (code)

```python

# 1. Select categorical columns
cat_cols = df.select_dtypes(include=['object', 'category']).columns

# 2. Keep only characteristic columns (e.g., fewer than 50 unique values)
characteristic_cols = [col for col in cat_cols if df[col].nunique() < 50]

# 3. Display clean value_counts for each characteristic column
for col in characteristic_cols:
    display(df[col].value_counts(dropna=False).to_frame())
```


## Cell 22 (code)

```python
%pwd
```


## Cell 23 (code)

```python
#multivariate analysis
```


## Cell 24 (code)

```python

```

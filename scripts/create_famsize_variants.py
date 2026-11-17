"""Build separate teaching notebooks for the provisional family-size scenario."""
import copy
import json
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]


def cell(kind, source):
    result = {'cell_type': kind, 'id': uuid4().hex[:8], 'metadata': {},
              'source': source.strip() + '\n'}
    if kind == 'code':
        result.update(execution_count=None, outputs=[])
    return result


def step(title, explanation, code):
    return [cell('markdown', '### ' + title + '\n\n' + explanation), cell('code', code)]


def load(name):
    notebook = json.loads((ROOT / 'notebooks' / name).read_text(encoding='utf-8'))
    for item in notebook['cells']:
        item['source'] = ''.join(item['source'])
        if item['cell_type'] == 'code':
            item.update(execution_count=None, outputs=[])
        item['metadata'] = {}
    return notebook


setup = '''from pathlib import Path
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
data.shape'''

assumptions = '''### Family-size scenario and source boundaries

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
'''

group_steps = []
group_steps += step('Family-size groups and percentages',
    'Create display groups without changing recorded values. `.loc` assigns labels to selected rows; percentages use all students as the denominator.',
    '''family_groups = pd.Series('2 or more', index=student_data.index)
family_groups.loc[student_data['famsize'].eq(0)] = '0'
family_groups.loc[student_data['famsize'].eq(1)] = '1'
family_groups.loc[student_data['famsize'].isna()] = 'Missing'
family_counts = family_groups.value_counts().reindex(['0', '1', 'Missing', '2 or more'], fill_value=0)
family_summary = pd.DataFrame({'Rows': family_counts, 'Percentage': (100 * family_counts / len(student_data)).round(2)})
assert family_counts.sum() == len(student_data)
family_summary''')
group_steps += step('Parental status and guardian by family-size group',
    '`pd.crosstab` counts combinations. Missing labels are for display, not imputed household evidence. Each table must total the number of students.',
    '''parent_status_labels = student_data['Pstatus'].fillna('Missing')
guardian_labels = student_data['guardian'].fillna('Missing')
family_context_counts = pd.crosstab(
    family_groups, [parent_status_labels, guardian_labels], dropna=False
)
assert family_context_counts.to_numpy().sum() == len(student_data)
family_context_counts''')
for column in ['Medu', 'Fedu']:
    group_steps += step(column + ' across family-size groups',
        'Compare recorded education, retaining literal `None` separately from missing entries. These counts do not identify household residents.',
        f"pd.crosstab(family_groups, student_data['{column}'].fillna('Missing'))")

donor_code = '''family_donors = student_data.loc[
    student_data['famsize'].ge(1), ['famsize', 'Pstatus', 'guardian']
].copy()
family_donors['Pstatus'] = family_donors['Pstatus'].fillna('Missing')
family_donors['guardian'] = family_donors['guardian'].fillna('Missing')
family_donor_summary = family_donors.groupby(['Pstatus', 'guardian'])['famsize'].agg(
    ['count', 'median', 'min', 'max']
)
assert len(family_donors) + student_data['famsize'].eq(0).sum() + student_data['famsize'].isna().sum() == len(student_data)
family_donor_summary'''
group_steps += step('Inspect positive-size comparison groups',
    'Use sizes of at least 1 as candidate donors, including valid size-1 records. `.agg` shows support and spread; a small group or wide range weakens confidence in its median.', donor_code)

candidate_steps = step('Estimate a candidate family size',
    'Join medians to each student using recorded grouping keys. `.fillna` implements the stated fallback order. Add 0.5 and take the floor to round positive half-values upward. The original table stays unchanged.',
    '''import numpy as np

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
family_candidates.loc[family_target].groupby(['Pstatus', 'guardian', 'Proposed', 'Method']).size().rename('Rows').to_frame()''')
candidate_steps += step('Review changes before adoption',
    'Compare recorded and candidate distributions and the number of affected students. Only zero/missing values are targets; education and guardian values are not inferred from family size.',
    '''family_audit = pd.DataFrame({
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
family_distribution.sort_index()''')

exploration = load('data_exploration.ipynb')
exploration['cells'][0] = cell('markdown', '''# Data exploration — family-size retention scenario

Inspect recorded values and evaluate a candidate correction while retaining family size.
This separate variant preserves the existing exploration notebook. Run from the
project root or `notebooks/`. Requires pandas, NumPy, Matplotlib and Seaborn.
Assistant execution, if recorded, does not verify the selected VS Code kernel.
''')
exploration['cells'][4]['source'] = setup
for item in exploration['cells']:
    if item['cell_type'] == 'code':
        item['source'] = item['source'].replace("include=['str']", "include=['object', 'string']").replace("'str', 'object'", "'string', 'object'")
    elif 'If family size includes the student' in item['source']:
        start = item['source'].index('If family size includes the student')
        end = item['source'].index('### Missing failures', start)
        item['source'] = item['source'][:start] + 'This variant uses the user-supplied definition excluding the student. Size 1 is retained; zero/missing values are examined in the scenario below. Household membership remains uncertain.\n\n' + item['source'][end:]
    if item['cell_type'] == 'markdown':
        item['source'] = item['source'].replace('## Final exploration conclusion (REMOVE)', '## Exploration findings before the family-size scenario')
exploration['cells'][47] = cell('markdown', '''### Interpretation under the revised family-size definition

The student is excluded from the count. Size 1 is plausible and retained.
Zeros and missing values warrant review, but guardianship and parental status
do not prove co-residence. Earlier counts of size 1 with `Pstatus = T` are
descriptive flags, not confirmed errors. Parental education does not count residents.
''')
exploration['cells'] += [cell('markdown', assumptions)] + copy.deepcopy(group_steps + candidate_steps)
exploration['cells'] += [cell('markdown', '''### Next teaching step

Inspect donor counts, ranges, and proposed changes. Explain why a median is an
estimate rather than a recovered count. Review the zero-as-unknown assumption,
fallback order, rounding, and sensitivity before adopting this scenario for modelling.
The companion `data_preprocessing_famsize.ipynb` applies the same candidate rule
and exports a separate dataset and audit trail.
''')]

preprocessing = load('data_preprocessing.ipynb')
preprocessing['cells'][0] = cell('markdown', '''# Data preprocessing — retain and estimate family size

This independent variant retains `famsize` and applies the provisional scenario
evaluated in `data_exploration_famsize.ipynb`. All other existing treatments are
carried over. Run from the project root or `notebooks/`; requires pandas and NumPy.
Outputs go to `outputs/famsize_scenario/`, separately from the existing pipeline.
Assistant execution does not verify the selected VS Code kernel.
''')
preprocessing['cells'][4]['source'] = setup
family_section = [cell('markdown', assumptions)]
family_section += step('Check duplicate student records',
    'Exclude the exported row index and count duplicate records. This check does not delete students.',
    "duplicate_count = student_data.duplicated().sum()\nprint('Duplicate records:', int(duplicate_count))")
family_section += step('Inspect family-size donors from recorded values',
    'Use the raw-loaded `student_data`, not already filled parental/guardian values, to build comparison groups.', donor_code)
family_section += copy.deepcopy(candidate_steps)
family_section += step('Apply the candidate and validate preservation',
    'Assign only the candidate family-size Series. Check positive recorded sizes, all other features, row identities, completeness and integer counts. This is a scenario export, not final methodological approval.',
    '''before_family_treatment = student_data_clean.copy()
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
student_data_clean.shape''')
preprocessing['cells'][51:55] = family_section
for item in preprocessing['cells']:
    if item['cell_type'] == 'markdown':
        item['source'] = item['source'].replace('`famsize` is excluded because\nof inconsistent values.', '`famsize` is retained with the provisional group-median estimates documented above.')
    if item['cell_type'] == 'code' and "output_path = Path(" in item['source']:
        item['source'] = '''output_folder = project_root / 'outputs/famsize_scenario'
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
print('Family-size estimates:', int(family_target.sum()))'''

for name, notebook in [('data_exploration_famsize.ipynb', exploration),
                       ('data_preprocessing_famsize.ipynb', preprocessing)]:
    explained_cells = []
    for item in notebook['cells']:
        if item['cell_type'] == 'code' and (not explained_cells or explained_cells[-1]['cell_type'] != 'markdown'):
            explained_cells.append(cell('markdown', '### Inspect the next result\n\nRun this small follow-up step using the variables above. Check the resulting counts, categories, or dimensions before interpreting them.'))
        explained_cells.append(item)
    notebook['cells'] = explained_cells
    for index, item in enumerate(notebook['cells']):
        if item['cell_type'] == 'code':
            compile(item['source'], name, 'exec')
            assert index > 0 and notebook['cells'][index - 1]['cell_type'] == 'markdown'
    (ROOT / 'notebooks' / name).write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(name, len(notebook['cells']), 'cells')

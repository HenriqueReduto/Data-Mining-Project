# Class coding baseline

Reviewed on 2026-11-12 from source and explanatory cells of all 12 supplied notebooks inside four lab ZIPs. The user confirmed this expanded guide after a grilling interview. Source review establishes demonstrated patterns. Execution and compatibility need checks in the selected environment.

## Read the relevant branch

Before proposing or reviewing notebook code, read this core guide, the applicable reference, and its relevant source lab cells.

| Task | Detailed reference |
| --- | --- |
| Loading, selection, types, missingness, summaries, relationships | [Exploration](course-reference/exploration.md) |
| Duplicate evaluation, filling, replacement, encoding, scaling, exports | [Preprocessing](course-reference/preprocessing.md) |
| Distributions, category counts, scatterplots, heatmaps, subplot loops | [Visualization](course-reference/visualization.md) |
| Features, fitting, candidate comparisons, profiles, hierarchical/categorical methods | [Modelling](course-reference/modelling.md) |

The references provide purpose, inputs, output, syntax to teach, checks, source citations, and adaptations. Short examples use student columns when doing so preserves the agreed methodology. Examples requiring an unapproved model choice retain lab variables and identify prerequisites. Code blocks are teaching steps or pattern templates, with their dependencies explained in surrounding text.

## Instruction and evidence roles

- AGENTS.md supplies project boundaries and teaching rules. Current preprocessing decisions live in [decisions.md](decisions.md), data findings in [data-audit.md](data-audit.md), and active task status in [PLAN.md](../PLAN.md).
- A lab citation establishes what was demonstrated. A project adaptation explains a necessary change. An extension introduces a method absent from the inspected notebooks and requires an explanation and appropriate validation.
- Lab thresholds, selected features, cluster counts, drop rules, and imputation examples remain source-specific choices. Apply the project's approved decisions when adapting them.
- Keep historical experiment reports and their verification status in [prior-experiments.md](prior-experiments.md).

## Teaching sequence for each small step

1. Read the current notebook and identify its available variables, row population, and saved outputs.
2. State the question and purpose in a short English Markdown cell above the code.
3. Introduce the smallest needed syntax, identifying input and expected output type. Explain unfamiliar syntax before combining it with other new operations.
4. Let the user attempt the cell by default. Give the complete code on request or when the user is stuck. Edit notebook code directly when explicitly requested.
5. Review actual results using counts, shape, ranges, categories, index alignment, or the rendered plot as applicable.
6. Record the supported interpretation and unresolved decisions in adjacent Markdown. Move to the next coherent step after the user understands the code and result.

P1 cells 19–21 teach the shape attribute before execution. P1 Markdown cell 31 introduces selection syntax. P1E/P2E/P3E/P4E contain short prompts and learner completion cells. P2 cells 56–58 bracket a replacement with before-and-after counts. These examples support the sequence above.

## Preferred code form

- Use small sequential cells, explicit column lists, named intermediate variables, and short comments explaining a decision or non-obvious operation.
- Use `pd`, `np`, `plt`, and `sns` as the familiar aliases. Import a package when it is needed and record relevant versions.
- Teach Series versus DataFrame selection, assignment `=`, comparison `==`, `.loc[rows, columns]`, methods with `()`, attributes without `()`, named arguments, and lists as each appears.
- Use copies for independently evaluated alternatives and preserve the row index through filtering, scaling, encoding, and label assignment.
- Loops, list comprehensions, lambda expressions, and simple functions can be introduced when their purpose is clear. Source examples include P2S cell 44, P3 cell 21, and P4 cell 84.
- Build a single understood operation before generalizing it. Reusable helpers belong in `src/` when repetition and an explained interface justify them.
- For modelling, follow explicit feature selection, preparation, construction, fit, inspection, label attachment, and original-unit profiling.

## Correctness and reproducibility adaptations

| Source pattern | Adaptation and review trigger |
| --- | --- |
| Colab mounts and personal Drive paths, e.g. P1 cell 7 and P4 cell 7 | Use documented project-relative loading and verify kernel working directory. |
| Generic file parsing | Preserve the literal education None category using the audited CSV options. Check counts after loading. |
| Object-only categorical selection, P1 cell 49 and P4 cell 76 | Inspect inferred dtypes. Use pandas 3 string selection as needed and identify numeric-coded categories explicitly. |
| Series-level inplace replacement, P2 cell 57 and P2S cells 29–41 | Prefer explicit column reassignment and check frequencies and dtypes. |
| Reconstructed scaled DataFrames without an index, P2 cell 129, P4 cell 17, P4S cell 19 | Pass both original columns and index, then check label alignment. |
| Unseeded elbow fits, P4 cell 26 and P4S cell 23 | Record random_state and explicit n_init consistently across comparable fits. |
| Broad warning suppression, P2 cell 7 and P4 cell 6 | Inspect and address relevant warnings while validating the code. |
| Current-year age derivation, P2 cell 103 | Use the documented observation/reference date when deriving a time-dependent feature. |
| Ratios without denominator checks, P2 cell 105 and P2S cell 58 | Inspect zeros and define the treatment before dividing. |
| Binary fallback mappings, P2 cell 107 | Verify missing and unexpected categories before mapping. |
| Summing transaction indicators versus maximum, P3 cells 30–32 and P3S cells 17–19 | Choose counts or binary presence according to the intended grain and meaning. |
| Series access following sorting, P3S cell 31 | Use explicit positional or label indexing consistent with the intended access. |

Explain a departure when it changes syntax, behavior, reproducibility, or interpretation. Source risks above are findings from inspection. Confirm their actual effect against the selected package versions and inputs. A correction does not require copying a source error into the project first.

## Methods and scope

| Lab | Demonstrated work |
| --- | --- |
| Practical 1 | Pandas loading, inspection, selection, aggregation, and Seaborn/Matplotlib visualization |
| Practical 2 | Copies, types, duplicates, missingness alternatives, replacements, outlier investigation, derived values, get_dummies, MinMax scaling, and correlations |
| Practical 3 | Transaction preparation, indicator aggregation, loops/lambda/set operations, Apriori, and association-rule evaluation |
| Practical 4 | K-means, inertia/elbow, SciPy linkage/dendrogram, original-unit profiles and centroids, KModes, and KPrototypes |

The notebook sources provide simplified examples. P4S Markdown cells 2 and 53 explicitly discuss limitations. Use the assignment and project brief for final evaluation, stability, robustness, and educational interpretation requirements. See the modelling reference for methods absent from these notebook sources and how to introduce extensions.

## Source citation convention

References use source IDs below followed by zero-based cell indexes, such as `P1 cells 42, 47`. These indexes count both Markdown and code cells. They are independent of execution counts and printed Step numbers. Read the named ZIP member through `zipfile` and parse its JSON without executing or modifying it. If an archive changes, recheck its member names and indexes before trusting a citation.

| ID | ZIP under `labs/` | Exact notebook member | Cells |
| --- | --- | --- | ---: |
| P1 | `Practical 1 - Data Understanding  Visualization.zip` | `Practical 1 - Data Understanding & Visualization/1 - Data Exploration and Visualization/Introduction_to_Pandas.ipynb` | 121 |
| P1E | `Practical 1 - Data Understanding  Visualization.zip` | `Practical 1 - Data Understanding & Visualization/2 - Application Exercise/Data Understanding - Application Exercise.ipynb` | 25 |
| P1S | `Practical 1 - Data Understanding  Visualization.zip` | `Practical 1 - Data Understanding & Visualization/2 - Application Exercise/Data Understanding - Application Exercise_solved.ipynb` | 26 |
| P2 | `Practical 2 - Data Preprocessing.zip` | `Practical 2 - Data Preprocessing/1- Data Preprocessing/Data_Preprocessing.ipynb` | 143 |
| P2E | `Practical 2 - Data Preprocessing.zip` | `Practical 2 - Data Preprocessing/2 - Application Exercise/Data Preprocessing - Exercise.ipynb` | 28 |
| P2S | `Practical 2 - Data Preprocessing.zip` | `Practical 2 - Data Preprocessing/2 - Application Exercise/Data_Preprocessing_Exercise_solved.ipynb` | 59 |
| P3 | `Practical 3 - Association Rules.zip` | `Practical 3 - Association Rules/1 - Association Rules/Association Rules.ipynb` | 78 |
| P3E | `Practical 3 - Association Rules.zip` | `Practical 3 - Association Rules/2 - Application Exercise/Association Rules - Exercise.ipynb` | 30 |
| P3S | `Practical 3 - Association Rules.zip` | `Practical 3 - Association Rules/2 - Application Exercise/Association Rules - Exercise_solved.ipynb` | 32 |
| P4 | `Practical 4 - KMeans.zip` | `KMeans/K_Means.ipynb` | 93 |
| P4E | `Practical 4 - KMeans.zip` | `Application Exercise/Application_Exercise.ipynb` | 29 |
| P4S | `Practical 4 - KMeans.zip` | `Application Exercise/Application_Exercise_solved.ipynb` | 54 |

The two lab PDFs are available reference material. This expanded baseline derives from the notebook sources.

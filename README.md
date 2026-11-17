# Data Mining I - Student segmentation

Coursework project exploring academic performance, engagement and contextual profiles among students at two Portuguese secondary schools. The workspace also supports guided Python learning through small notebook cells and explanations based on the supplied labs.

Read [the project brief](docs/project-brief.md) for requirements, [PLAN.md](PLAN.md) for recorded progress and pending decisions, and [AGENTS.md](AGENTS.md) for project working rules. Some older plan and memory entries describe previous layouts. The paths below reflect the workspace inspected on 15 November 2026.

## Current notebooks

New family-size retention variants (17 November): [exploration](notebooks/data_exploration_famsize.ipynb) and [preprocessing](notebooks/data_preprocessing_famsize.ipynb). These preserve positive recorded sizes and evaluate a provisional group-median treatment for zero/missing counts under the user-supplied definition excluding the student. Both load raw input independently and accept the project root or `notebooks/` as the working directory. Preprocessing exports separately to `outputs/famsize_scenario/`, including a per-row audit. Existing notebooks remain unchanged. Review correction assumptions and rerun in the selected VS Code kernel before adoption. This variant changes the earlier exclusion direction; the historical descriptions below may refer to the earlier pipeline.

| Notebook | Purpose and status |
| --- | --- |
| [data_exploration.ipynb](notebooks/data_exploration.ipynb) | Working exploration of distributions, missingness, family comparisons, grades and relationships. |
| [data_preprocessing.ipynb](notebooks/data_preprocessing.ipynb) | Earlier preprocessing notebook. Currently references `student_data` without defining it, so fresh-session execution needs correction. |
| [GroupXX_DMI_2627_Preprocessing.ipynb](notebooks/aitest/GroupXX_DMI_2627_Preprocessing.ipynb) | Standalone preprocessing draft with documented assumptions, before/after checks and prepared CSV export. |
| [GroupXX_DMI_2627_Modelling.ipynb](notebooks/aitest/GroupXX_DMI_2627_Modelling.ipynb) | Executed model experiments covering K-means, Ward hierarchical clustering, DBSCAN, SOM and RFM applicability. Includes profiles and sensitivity comparisons. |
| [GroupXX_DMI_2627_EDA.ipynb](notebooks/reference/GroupXX_DMI_2627_EDA.ipynb) | Earlier combined EDA/preprocessing version. Contains conflicting treatments and a loader assigning `df` while printing `data.shape`. Review before reuse. |

The two `aitest/` notebooks are reviewable experimental drafts. Family-size exclusion and several imputation and modelling choices remain provisional. Their location does not establish final submission status.

## Running the notebooks

Open the project root in VS Code and select the intended Python kernel. The notebook paths currently assume the kernel working directory is `D:\IMS\Data Mining Project\notebooks`, including the drafts stored under `notebooks/aitest/`.

Check the kernel working directory before running. If VS Code starts a draft kernel in `notebooks/aitest/`, its current `../data/` and `../outputs/` paths resolve incorrectly. Configure execution from `notebooks/` or adapt those paths before a fresh run. The relocated notebooks have not been validated in the selected VS Code kernel.

Use this execution sequence for the experimental pipeline.

1. Run `GroupXX_DMI_2627_Preprocessing.ipynb` from a fresh kernel.
2. Confirm `outputs/student_data_preprocessed.csv` is generated.
3. Run `GroupXX_DMI_2627_Modelling.ipynb` from a fresh kernel.
4. Review results and methodological assumptions before selecting the final solution.

The raw input is `data/raw/student_data.csv`. From the documented notebook working directory, its relative path is `../data/raw/student_data.csv`. Preserve the literal education category `None` when loading by using `keep_default_na=False` and `na_values=['']`.

The CSV has 649 rows and 34 imported columns, including an exported row index. Excluding that index leaves 33 analytical features. The preprocessing draft excludes family size and exports 32 features with a separate source row identifier.

## Preprocessing decisions

- Missing `failures` and `absences` become zero under the user-confirmed assumption that blanks represent zero occurrences. Source confirmation remains pending.
- Missing Yes/No responses become `Unknown`. At least one such response is missing for 140 students, representing 21.57% of rows. A separate mode-filled scenario supports later comparisons.
- Recorded grades, including zero grades, are retained in the standalone preprocessing draft.
- Family-size exclusion, education mode filling, grouped time medians and rating medians are documented draft choices requiring review.

See [decision memory](memory/decisions.md), [the data audit](memory/data-audit.md), and the current notebook explanations. The earlier reference notebook contains superseded or conflicting treatments.

## Models and current findings

The modelling draft compares K-means and Ward cuts at 2-5 groups, a DBSCAN neighborhood-parameter grid, and 3x3, 4x4 and 5x5 SOM maps. It evaluates candidate separation, sizes, original-unit profiles, initialization sensitivity, and Unknown-versus-mode sensitivity. RFM applicability is explained because the current dataset lacks dated events and a suitable value measure.

The working two-group K-means baseline has silhouette approximately 0.083 and strongly reflects school membership. The selected DBSCAN candidate has groups of 486 and 5 students, plus 158 noise observations. The provisional 4x4 SOM has topographic error approximately 0.55. These are exploratory findings. Final educational profiles and model selection require further validation.

## Generated outputs

| Location | Contents and use |
| --- | --- |
| `outputs/student_data_preprocessed.csv` | Prepared input consumed by the modelling notebook. Recreated by preprocessing. |
| `outputs/modelling/` | Candidate evaluation tables, exploratory assignments, sensitivity results and validation figures. |
| [Final report PDF](outputs/reports/GroupXX_DMI_2627_Final_Report.pdf) | Nine-page analytical report with profiles, interventions, practical support framework and limitations. Group details and final validation remain outstanding. |
| [Model-selection review PDF](outputs/reports/model_selection_review.pdf) | Detailed review of candidate solutions and required follow-up checks. |
| `outputs/reports/*preview/` | Rendered page images used for PDF layout checks. |
| `outputs/graphify-runtime/` | Isolated Graphify environment, approximately 168 MB at inspection. |
| `outputs/modelling-runtime/` | Isolated modelling/PDF environment, approximately 199 MB at inspection. |
| [graphify-out/graph.html](graphify-out/graph.html) | Interactive project knowledge graph. Loads its visualization library from the internet. |
| [graphify-out/GRAPH_REPORT.md](graphify-out/GRAPH_REPORT.md) | Knowledge-graph audit report. The graph reflects the 13 November source snapshot and can be stale after edits or moves. |

The runtime folders contain installed third-party packages. They support assistant execution and can be recreated when needed. Keep runtime environments outside coursework submission bundles. Generated data, notebook outputs and graph content require review before public sharing.

## Environment and validation

The recorded user notebook environment used Python 3.14.10 and pandas 3.1.1. The experimental modelling run recorded NumPy 2.5.4, scikit-learn 1.9.1, SciPy 1.18.1, Matplotlib 3.11.2, Seaborn 0.13.2 and MiniSom 2.3.6. Preprocessing needs pandas. Modelling additionally uses NumPy, scikit-learn, SciPy, Matplotlib, Seaborn and MiniSom. PDF generation used ReportLab and PyMuPDF in the isolated runtime.

On 14 November, the standalone preprocessing draft passed all 13 code cells in a fresh assistant IPython namespace. Checks covered row alignment, preserved observations, completeness, raw-data integrity and CSV export/reload. The modelling draft passed all 19 code cells with saved outputs, and its four generated figures were visually inspected. Both PDFs were rendered and visually checked.

These checks precede the notebooks' relocation to `notebooks/aitest/`. A fresh top-to-bottom run in the selected VS Code kernel remains pending. The project has no consolidated dependency manifest or verified automated analysis test suite. An interactive dashboard has yet to be implemented.

## Workspace helper

From the project root, run the read-only standard-library check with the following command.

```powershell
python scripts/check_workspace.py
```

On 15 November 2026, it reported missing historical paths and a broken memory link. It still expects `data/raw/private/student_data.csv`, both old `datamining1.ipynb` locations and an old ignore entry. `memory/course-baseline.md` also links to an absent `prior-experiments.md`. The helper needs reconciliation with the current layout before a clean result is meaningful.

For terminal interpreter identification, use `python --version`. The VS Code notebook kernel may use a different interpreter.

## Folder responsibilities

| Folder | Purpose |
| --- | --- |
| `data/raw/` | Supplied immutable CSV input. |
| `notebooks/` | Working analysis notebooks and experimental/reference subfolders. |
| `docs/` | Project brief and local reference documents. |
| `memory/` | Decisions, verified findings and course coding references. |
| `labs/` | Supplied course notebooks and PDFs. |
| `scripts/` | Workspace maintenance and validation helpers. |
| `src/`, `tests/`, `skills/` | Reserved for reusable implementation, checks and project-specific skills. |
| `outputs/` | Regenerable datasets, results, reports and isolated runtimes. |
| `graphify-out/` | Generated project knowledge graph, cache and audit files. |

## Version control and submission

Git is initialized. At inspection, `data/raw/student_data.csv` is tracked. Current ignore rules exclude `outputs/`, `labs/`, private reference documents, environment files and common generated files. Raw data and `graphify-out/` have no matching ignore rule. Ignore rules do not remove files already tracked or erase history.

Confirm redistribution permissions before making the repository public. Saved notebook outputs can expose individual student records and local computer paths. A previous local screening found no recognizable secrets in the patterns checked, which provides limited screening evidence rather than a guarantee.

The assignment requires an executed notebook or notebook ZIP with the final group identifier and member information. This PDF report supplements the notebook deliverable. Include required data or clear loading instructions, record dependencies and assumptions, and complete final validation and the chosen practical outcome before submission.

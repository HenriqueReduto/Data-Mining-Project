# Data Mining I project

Student clustering coursework and guided Python learning in VS Code/Jupyter. Begin with the [project brief](docs/project-brief.md), follow [PLAN.md](PLAN.md), and use [AGENTS.md](AGENTS.md) for agent boundaries and the teaching workflow.

## Open the workspace
Open the whole `D:\IMS\Data Mining Project` folder in VS Code using File > Open Folder. This is the workspace root; Git has not been initialized. Run terminal commands from this root so paths and responsibilities remain consistent.

## Folder responsibilities
| Path | Contents and ownership |
| --- | --- |
| `AGENTS.md` | Durable agent rules; user approves consequential methodology and direct notebook edits. |
| `PLAN.md` | One active execution plan, progress, validation, and the next learning step. |
| `notebooks/` | Notebook deliverables and future working analysis. The supplied `datamining1.ipynb` remains a protected original until a working copy is chosen. |
| `notebooks/reference/` | The second original notebook, relocated from the project root, unchanged. |
| `src/` | Reserved for reusable Python/dashboard source when justified; implementation has not started. |
| `tests/` | Reserved for meaningful checks of later reusable code; no test framework selected yet. |
| `docs/` | Project brief, methodological explanations, and submission documentation. |
| `docs/references/private/` | Local assignment PDF, original Word notes, and excluded Loop archive; unchanged content, ignored by Git. |
| `scripts/` | Workspace and maintenance helpers; separate from analysis code. |
| `memory/` | Confirmed decisions, verified data findings, and the class coding baseline. |
| `skills/` | Project-specific agent skills if needed later; see its README. |
| `data/raw/private/` | Immutable supplied student CSV; local input, ignored by Git. |
| `outputs/` | Generated figures, tables, exports, and dashboard/submission bundles; ignored by default. |
| `logs/` | Generated local logs; `.log` files are ignored. |
| `labs/` | Unchanged supplied course PDFs and lab ZIPs, used as the coding baseline; local reference material, ignored by default. |

The reserved source/test folders are intentionally empty. Populate them when implementation requires them; the project remains notebook-led.

## Commands and verification status
The following commands are for a PowerShell terminal opened at the workspace root.

```powershell
python scripts/check_workspace.py
```

This dependency-free helper checks required folders, protected reference paths, documented file links, ignore entries, and notebook identity. It reads metadata and hashes, prints no student rows, and does not run analysis. Verified during the workspace update using the available system Python; this does not verify the notebook kernel.

To display the terminal interpreter version:

```powershell
python --version
```

This does not necessarily identify the interpreter selected in a VS Code notebook. Check the notebook kernel selector before running project cells.

`code .` is an optional way to open the root; the VS Code command was found on PATH, but launching it was not tested. No analysis, dashboard, dependency-install, or automated test command is documented as working yet. Record each command here with its working directory, prerequisites, and validation evidence when it becomes available.

## Raw input and notebook execution
The active working notebooks are [data_exploration.ipynb](notebooks/data_exploration.ipynb) and [data_preprocessing.ipynb](notebooks/data_preprocessing.ipynb). Exploration contains missingness analysis, summaries, family comparisons, travel-time checks, and study-time checks on recorded values. Preprocessing evaluates duplicates and fills missing absences and failures with zero under the approved assumption. Each loads `../data/raw/student_data.csv` independently and should run with its working directory set to `notebooks/`. The current CSV is at `data/raw/student_data.csv`; older private-path references below describe the previous layout.

`notebooks/student_clustering.ipynb` is retained as the combined reference snapshot. On 2026-11-12 both new notebooks were run sequentially in separate IPython namespaces using the assistant runtime, and their outputs were saved. This checked all 21 exploration and 7 preprocessing code cells. Jupyter kernel execution and visual inspection in VS Code remain pending because nbformat/nbclient/nbconvert are unavailable in that runtime. In VS Code, select the project kernel and use Restart Kernel and Run All for each notebook.

The supplied input is now `data/raw/private/student_data.csv`. The original notebooks are retained unchanged, including their historical `pd.read_csv('student_data.csv')` cell; that cell must be adapted in the future working copy before execution.

Use project-relative paths with a documented working directory. From a notebook executing in the project root, the CSV path is `data/raw/private/student_data.csv`; from inside `notebooks/`, it is `../data/raw/private/student_data.csv`. Establish the actual working directory before selecting one. Preserve the literal education category `None` separately from blanks; see [the data audit](memory/data-audit.md).

On 2026-11-10, user-run diagnostic output in `notebooks/student_clustering.ipynb` confirmed Python 3.14.10 at `C:\Users\henri\AppData\Local\Programs\Python\Python314\python.exe`, with working directory `D:\IMS\Data Mining Project\notebooks`. Use `../data/raw/private/student_data.csv` from that directory. Analysis package availability/versions and fresh-kernel execution of the analysis remain unverified; the diagnostic does not establish those.

## Tracking and private material
Saved working-notebook output inspected on 2026-11-10 confirms `import pandas as pd` succeeded and `print(pd.__version__)` returned 3.1.1 in the user's kernel. Other analysis packages and full analysis execution remain unverified.

The minimum ignore rules are installed in `.gitignore`, with additional exclusions for local course references, private project documents, and generated outputs. Keep raw inputs immutable and write derived material to `outputs/`. Keep credentials, API keys, local `.env` files, virtual environments, databases, and generated logs out of version control. A safe `.env.example` can be tracked if configuration is introduced; none is needed now.

Private PDFs, raw data, and large generated outputs should be included in version control only when the project explicitly requires it. Document any exception and review its contents first. Ignore rules do not untrack files already tracked in an existing repository. Notebook outputs can also contain student-level data; review them before sharing or committing.

This local workspace currently contains the supplied data. A clone that excludes private paths will need those files restored to the documented locations before analysis can run. Final coursework packaging must still contain required inputs or clear loading instructions; Git exclusions do not decide submission requirements.

## Workspace changes
The authorized organization moved root raw data into `data/raw/private/`, reference documents into `docs/references/private/`, and the root notebook into `notebooks/reference/`. File contents were preserved and their SHA-256 hashes checked. Existing teaching and direct-edit boundaries continue to apply. No Git initialization, package installation, or analysis/dashboard implementation was performed.

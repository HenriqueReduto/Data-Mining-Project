# Decisions

Entries are current unless marked otherwise. Setup entries are dated 2026-11-10; later decisions carry explicit dates. Evidence is the user's decisions and inspected source files where specified.

## Missing failures and absences become zero
- Date/status: 2026-11-12; current, explicitly reconfirmed by the user.
- Decision: Replace missing `failures` and `absences` with 0 in the working dataset used for analysis and clustering.
- Reason: The user selected the interpretation that blank entries represent no previous failures or absences.
- Scope: These two columns in the working dataset. Apply the rule consistently in subsequent preprocessing and interpretations.
- Evidence: User stated, "We will keep the missing failures and absences as 0", after reviewing background experiments that used a different treatment, then requested inclusion in agent files.
- Qualification: This is an adopted methodological assumption. Confirmation of the source/export meaning of blanks remains pending. The attached experiments' unresolved-count treatment is superseded for the current working approach.

## Separate exploration and preprocessing notebooks
- Date/status: 2026-11-12; current, explicitly requested by the user.
- Decision: Use `notebooks/data_exploration.ipynb` for analysis and `notebooks/data_preprocessing.ipynb` for filling missing values and evaluating duplicate records.
- Scope: Both load `../data/raw/student_data.csv` independently from `notebooks/`. Exploration uses recorded values, including original missing counts. Preprocessing applies the zero-fill decision to failures and absences.
- Evidence: User requested dividing the combined working notebook into these two named files with those responsibilities.
- Preservation: The combined notebook remains a reference snapshot. Original source cells were accounted for in the split; a malformed zero-family filter was corrected in exploration.

## Expanded class baseline for code agents
- Date/status: 2026-11-12; current, confirmed after the grilling interview.
- Decision: Keep core rules and an exact lab-source index in `course-baseline.md`, with separate exploration, preprocessing, visualization, and modelling references under `course-reference/`.
- Reason: Give code agents task-specific patterns, concise syntax explanations, expected outputs, validation checks, and exact zero-based source-cell citations.
- Scope: Prefer short student-data adaptations. Retain lab examples where student adaptation would require an unapproved methodological choice. Explain corrections and newer syntax, and distinguish source patterns, project adaptations, and extensions.
- Evidence: User answered yes to all four interview choices and confirmed the final five-file structure before implementation.

## Guided learning is a project objective
- Decision: Teach Python coding through small explanations, user attempts, and review. Provide full solutions on request or when the user is stuck.
- Reason: The user has model experience and specifically wants to understand the code and programming basics.
- Scope: Analysis, notebook work, and later dashboard development. Explain relevant syntax and outputs rather than assuming programming fluency.
- Evidence: User stated the learning objective, accepted the teaching recommendation, and confirmed the project brief.

## User writes notebook code by default
- Decision: The agent may inspect material and maintain project documentation directly. It proposes notebook changes for user implementation; direct notebook code edits require an explicit request. Consequential methodology choices go to the user.
- Reason: Preserve user participation and understanding.
- Scope: Ongoing project work. Approval of setup documentation is not permission to implement the project.
- Evidence: User agreed to the proposed agent boundaries and confirmed the brief.

## Environment and class baseline
- Decision: Use Jupyter notebooks in VS Code and follow the supplied lab notebooks' explicit, sequential coding and teaching patterns. Adapt Colab setup to VS Code and explain necessary departures.
- Reason: Notebooks are the assignment's required code deliverable; the user selected VS Code and asked to match class style.
- Scope: Notebook structure, code examples, and review. Lab algorithms and parameters are not automatically approved analysis choices.
- Evidence: User supplied `labs/`, requested its use as baseline, and confirmed the resulting rule. Notebook submission requirements: assignment PDF page 7. Source index: `course-baseline.md`.

## Start with data understanding and preprocessing
- Decision: Make auditing/completing exploration and preprocessing the first objective while retaining the whole assignment in the brief.
- Reason: Existing work contains unverified cleaning assumptions and incomplete exploration.
- Scope: First active plan in `../PLAN.md`.
- Evidence: User accepted the proposed first milestone; `data-audit.md` records the supporting findings.

## Dashboard as Knowledge in Action
- Decision: Deliver a dashboard. Defer exact features, technology, packaging, and hosting decisions to after initial exploration, before finalizing clustering, with the user owning approval.
- Reason: The user explicitly selected a dashboard; the assignment allows it as one practical outcome.
- Scope: Full project; no dashboard implementation or publishing is part of setup.
- Evidence: User said "Then lets do a dashboard" and confirmed the brief. Assignment PDF page 4 permits the approach.

## Preserve supplied material
- Decision: Preserve all supplied source files, original notebooks, and labs; exclude `Loop paragraph.loop` as a source. Use `notebooks/` as the notebook directory.
- Reason: Retain existing group work and class references while validating assumptions.
- Scope: Inputs and reference work. Choose the working notebook before new code; keep both original copies available.
- Evidence: User agreed to preservation, excluded the Loop file, and confirmed they had renamed the notebook folder.

## Deferred project details
- Decision: Resolve kernel and working-notebook choice before first project execution/editing; methodological decisions at their evidence-based analysis steps; dashboard scope at the trigger above; group identity and defense scheduling before submission preparation.
- Reason: These do not block documentation setup, but affect later implementation and delivery.
- Scope/owner: See the full decision/impact/owner/trigger table in `../docs/project-brief.md`.
- Evidence: Confirmed brief. No unprovided group number, student identities, kernel, or defense date has been assumed.

## Workspace organization amendment
- Date/status: 2026-11-10; current.
- Decision: Adopt the user-supplied workspace structure and minimum .gitignore; add README and command evidence; separate raw/private data, reference documents, reusable source, tests, maintenance scripts, skills, and generated outputs. Preserve original file contents while relocating them into these areas.
- Reason: Make ownership, navigation, private inputs, outputs, and commands explicit for humans and agents.
- Scope: Project workspace and shared red-project-setup skill/templates. Supersedes the original setup restriction on reorganization only for these requested content-preserving relocations. Existing teaching and direct-notebook-edit boundaries remain current.
- Evidence: User explicitly requested updates to both the project and skill and supplied section 10 Workspace setup, its directory tree, and minimum ignore entries. New paths are documented in ../README.md.
- Validation: source hashes preserved; workspace helper and documentation links checked; skill validator passed.

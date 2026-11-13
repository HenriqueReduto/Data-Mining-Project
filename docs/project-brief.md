# Project brief

Confirmed: 10 November 2026. The user confirmed the brief and the class-notebook coding baseline in the setup conversation before file creation.

## Objective and users
Discover meaningful profiles of students from two Portuguese secondary schools using academic performance, engagement, and contextual variables. Compare and validate clustering solutions, interpret the profiles, and propose realistic educational support strategies. Findings describe associations and groupings, not causes or diagnoses.

The project also teaches the user to understand and write Python code. The user already has model experience; coding comprehension is the learning priority. The analysis is coursework for the student group and assessors. The practical dashboard should demonstrate usefulness to a school or educational coordinator.

## Scope and first milestone
The full project includes data understanding, justified preprocessing and feature design, comparison and evaluation of appropriate clustering methods, cluster interpretation, intervention strategies, a dashboard for Knowledge in Action, and a presentation.

The first milestone is to audit and complete data understanding and preprocessing. Revisit the supplied notebook's assumptions before modelling. Work through small coding steps with the user, documenting observations separately from decisions.

The intended learning journey is: understand a question, learn the relevant syntax, attempt a small cell, inspect its result, and explain what it establishes. The agent reviews and guides. Complete examples are available on request or when the user is stuck.

## Assignment deliverables and requirements
The source assignment is `docs/references/private/Project_DMI_2026_2027.pdf`, reviewed in full during setup. This summary makes the project usable without that PDF attached to a future conversation.

### Notebook submission
- Submit one Jupyter notebook or a ZIP containing multiple notebooks, named `GroupXX_DMI_2627.ipynb` or `GroupXX_DMI_2627.zip`; replace XX with the actual group number before submission.
- Begin with Markdown listing all group members' names and student numbers.
- Include exploration, preprocessing, modelling, interpretation, and the practical outcome's relevant explanation and evidence.
- Save executed cells and ensure a fresh top-to-bottom run reproduces the reported results.
- Use relative paths or clear data-loading instructions; document required files, versions, and assumptions.
- Use readable, commented code and Markdown to justify important decisions. Distinguish exploratory/discarded alternatives from the final solution.
- Produce the final tables and figures used in the presentation. Keep the notebook succinct and execution time practical.
- Cite material used beyond the supplied course/project materials. The assignment cautions against plagiarism and excessive AI-generated content; all members must understand and explain the work.

### Analysis and practical outcome
- Investigate distributions, inconsistencies, missing values, duplicates, unusual values, relationships, and educationally relevant subgroups.
- Justify numerical, ordinal, binary, and categorical treatment, scaling, transformations, engineered features, and variable inclusion/exclusion.
- Compare appropriate clustering alternatives or parameters. Explain the number of clusters, distinctness, stability, robustness, and educational meaning.
- Name and describe final clusters using supporting statistics and visualizations.
- Propose proportionate support offers; clustering must not punish students or deny opportunities.
- Deliver a dashboard as the selected Knowledge in Action component. It should accurately communicate final profiles, indicators, and practical support options; exact interactions and technology are deferred.

### Presentation and defense
- Prepare a maximum 10-minute presentation, followed by a 30-minute technical defense in a 40-minute slot.
- Communicate the problem, key insights, final clustering approach, profiles, interventions, dashboard, and main limitations.
- Every member must be prepared to explain the whole project. The defense is mandatory and in person.
- The stated project deadline is December 21 at 18:00 (planned as 2026 from the course context). Presentation materials are due two days before the defense; the defense date is not supplied.
- The PDF permits up to three days of late submission with a one-point-per-day penalty, then no acceptance. This is not the working delivery target.

### Evaluation priorities
The page 8 rubric assigns: notebook clarity/reproducibility 10%, preprocessing 20%, exploration 20%, clustering methodology/evaluation 25%, interpretation/interventions 10%, Knowledge in Action 10%, and presentation 5%. The presentation is listed as one point there but two points in the page 10 heading. Use the complete rubric as the provisional planning basis and ask the instructor if that discrepancy affects submission planning.

## Constraints and ownership
- Use Jupyter notebooks in VS Code. Dependencies, interpreter, and versions remain to be verified.
- Preserve supplied inputs, original notebooks, and labs. The Loop file is excluded as a source by user choice.
- Use the class coding baseline in `memory/course-baseline.md`; adapt examples to the student data and explain necessary departures.
- The agent may inspect material and maintain operating documents. The user writes notebook code by default; direct agent code edits require an explicit request.
- The user approves consequential methodological choices and the dashboard scope. The agent does not assume authority to decide for other group members.

## Acceptance criteria
1. The user can explain the purpose, syntax, inputs, outputs, and checks for each adopted code step.
2. The first milestone produces documented data-quality findings and justified preprocessing choices, preserving raw inputs and distinguishing literal education `None` from blanks.
3. The final notebook submission executes from a fresh kernel with the documented environment and reproduces reported outputs using portable loading instructions.
4. Clustering alternatives, cluster count, stability, distinctness, and practical interpretation are evaluated rather than assumed from class examples.
5. The dashboard presents the final analysis consistently and supports realistic educational decisions with stated limitations.
6. The submission and presentation cover the required content, group identification, sources, and deadlines.

## Setup boundaries
The initial setup created operating documentation. On 2026-11-10 the user additionally authorized the workspace structure, root README, minimum .gitignore, documented commands, and separation of raw/private inputs, references, source, tests, scripts, skills, memory, and generated outputs. This authorizes relocating supplied files with content-preservation checks and updating their references. See `../README.md` for the resulting map. Setup still excludes analysis/dashboard implementation, slides, dependency installation, Git initialization, commits, and publishing.

## Confirmed decisions and reasons
- Begin with data understanding/preprocessing because existing cleaning assumptions require verification.
- Use a dashboard for Knowledge in Action because the user explicitly selected it from the permitted practical outcomes.
- Preserve the supplied work as reference and use class notebooks as the coding baseline to support continuity and learning.
- Teach through user attempts and code review rather than default direct notebook edits, matching the user's coding-learning objective.

## Deferred decisions
| Decision | Impact | Owner | Resolve by |
| --- | --- | --- | --- |
| Working notebook name and treatment of identical originals | Avoid editing the wrong copy or losing reference work | User, with agent recommendation | Before the first notebook edit; prefer a separate working copy if preserving both originals |
| VS Code kernel, Python version, and required packages | Determines runnable code and compatible syntax | User with agent inspection/guidance | Before the first project execution or environment change |
| Specific preprocessing, features, and clustering alternatives | Determines validity and interpretability | User, with group agreement as applicable | At the relevant analysis step, using observed evidence |
| Dashboard features, technology, packaging, and whether any hosting is needed | Determines implementation scope and notebook integration | User, with group agreement as applicable | After initial exploration, before finalizing clustering; no publishing is authorized by setup |
| Group number, names/student numbers, defense date, and any updated instructor instructions | Determines final naming, title cell, and presentation schedule | User/group | Before preparing submission materials; defense date when announced |

These are scheduled decisions, not blockers to documentation setup. The active milestone and next action are maintained in `PLAN.md`.

## Workspace organization amendment (2026-11-10)

The user explicitly supplied the workspace structure and minimum ignore rules. Raw input is `data/raw/private/student_data.csv`; local source documents are in `docs/references/private/`; the former root notebook is in `notebooks/reference/`. These are content-preserving relocations, not new analysis. Git exclusions apply to private/raw data, reference materials, local environments, credentials, logs, databases, checkpoints, and generated outputs; an explicit project requirement may justify a documented exception. Existing labs and notebook-led teaching remain in place. `src/`, `tests/`, and `skills/` are reserved for later justified work.

# Graph Report - Data-Mining-Project  (2026-11-17)

## Corpus Check
- Corpus is ~38,731 words - fits in a single context window. You may not need a graph.

## Summary
- 512 nodes · 640 edges · 12 communities (11 shown, 1 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.93)
- Token cost: unavailable; agent tools do not expose usage. Zero placeholders are not measured usage.

## Community Hubs (Navigation)
- Historical reference workflow
- Family-size scenario exploration
- Cleaning decisions and assumptions
- Project governance and delivery
- Recorded student exploration
- Family-size scenario preprocessing
- Clustering experiments and evaluation
- Historical preprocessing and exclusions
- Course patterns and evidence
- Maintenance and runtime helpers
- Data audit and modelling handoff
- Candidate preservation checks

## God Nodes (most connected - your core abstractions)
1. `notebooks/reference/GroupXX_DMI_2627_EDA.ipynb` - 116 edges
2. `notebooks/aitest/data_exploration_famsize.ipynb` - 66 edges
3. `notebooks/data_exploration.ipynb` - 55 edges
4. `notebooks/aitest/data_preprocessing_famsize.ipynb` - 54 edges
5. `notebooks/data_preprocessing.ipynb` - 49 edges
6. `notebooks/aitest/GroupXX_DMI_2627_Modelling.ipynb` - 35 edges
7. `notebooks/aitest/GroupXX_DMI_2627_Preprocessing.ipynb` - 26 edges
8. `notebooks/clustering.ipynb` - 10 edges
9. `Student dataset 649 rows 33 analytical features` - 8 edges
10. `Literal education None parsing` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Family-size median correction provisional` --conceptually_related_to--> `One-hot and numeric distance weighting`  [INFERRED]
  memory/decisions.md → graphify-out/notebook-sources/notebooks_aitest_GroupXX_DMI_2627_Modelling.ipynb.md
- `Prepare model matrices` --implements--> `Scaling with preserved row identity`  [INFERRED]
  graphify-out/notebook-sources/notebooks_aitest_GroupXX_DMI_2627_Modelling.ipynb.md → memory/course-reference/preprocessing.md
- `Inspect positive-size comparison groups` --implements--> `Grouped comparisons`  [INFERRED]
  graphify-out/notebook-sources/notebooks_aitest_data_exploration_famsize.ipynb.md → memory/course-reference/exploration.md
- `Parental status and guardian by family-size group` --implements--> `Cross-tabulations as an extension`  [INFERRED]
  graphify-out/notebook-sources/notebooks_aitest_data_exploration_famsize.ipynb.md → memory/course-reference/exploration.md
- `K-means candidate solutions` --implements--> `Fit K-means explicitly`  [INFERRED]
  graphify-out/notebook-sources/notebooks_aitest_GroupXX_DMI_2627_Modelling.ipynb.md → memory/course-reference/modelling.md

## Import Cycles
- 1-file cycle: `scripts/check_workspace.py -> scripts/check_workspace.py`
- 1-file cycle: `scripts/create_famsize_variants.py -> scripts/create_famsize_variants.py`
- 1-file cycle: `scripts/validate_famsize_variants.py -> scripts/validate_famsize_variants.py`

## Hyperedges (group relationships)
- **Family-size retention and correction review** — memory_decisions_family_size_retention_confirmed, memory_decisions_family_size_median_correction_provisional, graphify_out_notebook_sources_notebooks_aitest_data_exploration_famsize_ipynb_notebooks_aitest_data_exploration_famsize_ipynb, graphify_out_notebook_sources_notebooks_aitest_data_preprocessing_famsize_ipynb_notebooks_aitest_data_preprocessing_famsize_ipynb [EXTRACTED 1.00]
- **Unknown responses and clustering sensitivity** — memory_decisions_unknown_yes_no_category, graphify_out_notebook_sources_notebooks_data_exploration_ipynb_missing_value_overlap_in_yes_no_features, graphify_out_notebook_sources_notebooks_aitest_groupxx_dmi_2627_modelling_ipynb_sensitivity_to_unknown_versus_mode_for_yes_no_responses [INFERRED 0.95]
- **Aligned student identities across preprocessing and models** — graphify_out_notebook_sources_notebooks_data_preprocessing_ipynb_notebooks_data_preprocessing_ipynb, graphify_out_notebook_sources_notebooks_clustering_ipynb_notebooks_clustering_ipynb, graphify_out_notebook_sources_notebooks_aitest_groupxx_dmi_2627_preprocessing_ipynb_notebooks_aitest_groupxx_dmi_2627_preprocessing_ipynb, graphify_out_notebook_sources_notebooks_aitest_groupxx_dmi_2627_modelling_ipynb_notebooks_aitest_groupxx_dmi_2627_modelling_ipynb [INFERRED 0.95]

## Communities (12 total, 1 thin omitted)

### Community 0 - "Historical reference workflow"
Cohesion: 0.02
Nodes (113): 1.1 Educational Problem & Context, 1.2 Core Objectives, 1. Core Data Science & Scientific Libraries, 2. Data Visualization Libraries, 3.1 Data Overview, 3.2 Q1 – Who are the students?, 3.3 Q2 – How do students perform academically?, 3.4 Q3 – How do the two schools differ? (+105 more)

### Community 1 - "Family-size scenario exploration"
Cohesion: 0.04
Nodes (52): Academic performance, Analysis of failures and absences, Categorical summary, Column types and structure, Correlation between binary and rating features, Correlation between numerical features, Correlation between rating features, Correlation between Yes/No features (+44 more)

### Community 2 - "Cleaning decisions and assumptions"
Cohesion: 0.05
Nodes (47): Estimate a candidate family size, Family-size scenario and source boundaries, Estimate a candidate family size, Family-size scenario and source boundaries, Course patterns, Duplicate records, Environment, Family-size treatment for this draft (+39 more)

### Community 3 - "Project governance and delivery"
Cohesion: 0.05
Nodes (42): Coding baseline, Environment and validation, Project instructions, Protected material and layout, Read before working, Teach through the project, Work completion, Acceptance criteria (+34 more)

### Community 4 - "Recorded student exploration"
Cohesion: 0.04
Nodes (46): Academic performance, Analysis of failures and absences, Categorical summary, Column types and structure, Correlation between binary and rating features, Correlation between rating features, Correlation between Yes/No features, Data exploration (+38 more)

### Community 5 - "Family-size scenario preprocessing"
Cohesion: 0.05
Nodes (43): Check duplicate student records, Data loading and initial dimensions, Data preprocessing — retain and estimate family size, Environment check, Missing values before preprocessing, notebooks/aitest/data_preprocessing_famsize.ipynb, Order of remaining treatments, Rating medians (+35 more)

### Community 6 - "Clustering experiments and evaluation"
Cohesion: 0.06
Nodes (39): Academic-feature sensitivity, Agreement and initialization sensitivity, Application of course models, Course evidence and API sources, DBSCAN and neighborhood distances, DBSCAN noise and tiny group, DBSCAN parameter comparison, Environment and parameters (+31 more)

### Community 7 - "Historical preprocessing and exclusions"
Cohesion: 0.05
Nodes (39): Current education unknowns need model representation review, Sensitivity to Unknown versus mode for Yes/No responses, Missing-value overlap in rating features, Missing-value overlap in Yes/No features, Data loading and initial dimensions, Data preprocessing, Environment check, Exclusion of family size (+31 more)

### Community 8 - "Course patterns and evidence"
Cohesion: 0.06
Nodes (30): Inspect positive-size comparison groups, Parental status and guardian by family-size group, Inspect family-size donors from recorded values, Correlation between numerical features, Class coding baseline, Correctness and reproducibility adaptations, Instruction and evidence roles, Methods and scope (+22 more)

### Community 9 - "Maintenance and runtime helpers"
Cohesion: 0.09
Nodes (18): base64, copy, hashlib, io, ipython_core_interactiveshell, ipython_utils_capture, json, matplotlib_pyplot (+10 more)

### Community 10 - "Data audit and modelling handoff"
Cohesion: 0.09
Nodes (22): Import pandas, Load the prepared dataset, Next step, notebooks/clustering.ipynb, Student clustering, Verify dimensions and completeness, Save the prepared dataset, 4.2.3 Grade Recording Error: G1 (+14 more)

## Knowledge Gaps
- **14 isolated node(s):** `Zero family sizes need interpretation`, `Zero travel times uncertain`, `Word notes are hypotheses`, `No exact duplicate rows in audit`, `re` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 417 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `notebooks/reference/GroupXX_DMI_2627_EDA.ipynb` connect `Historical reference workflow` to `Data audit and modelling handoff`, `Project governance and delivery`, `Historical preprocessing and exclusions`?**
  _High betweenness centrality (0.377) - this node is a cross-community bridge._
- **Why does `notebooks/aitest/data_exploration_famsize.ipynb` connect `Family-size scenario exploration` to `Cleaning decisions and assumptions`, `Project governance and delivery`, `Family-size scenario preprocessing`, `Course patterns and evidence`, `Data audit and modelling handoff`, `Candidate preservation checks`?**
  _High betweenness centrality (0.204) - this node is a cross-community bridge._
- **Why does `notebooks/data_exploration.ipynb` connect `Recorded student exploration` to `Cleaning decisions and assumptions`, `Project governance and delivery`, `Family-size scenario preprocessing`, `Historical preprocessing and exclusions`, `Course patterns and evidence`, `Data audit and modelling handoff`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **What connects `Zero family sizes need interpretation`, `Zero travel times uncertain`, `Word notes are hypotheses` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Historical reference workflow` be split into smaller, more focused modules?**
  _Cohesion score 0.017699115044247787 - nodes in this community are weakly interconnected._
- **Should `Family-size scenario exploration` be split into smaller, more focused modules?**
  _Cohesion score 0.038461538461538464 - nodes in this community are weakly interconnected._
- **Should `Cleaning decisions and assumptions` be split into smaller, more focused modules?**
  _Cohesion score 0.04964539007092199 - nodes in this community are weakly interconnected._

## Build scope and limitations
- Rebuilt from 24 current files: 3 Python helpers and 21 documents/source-only notebook extracts; outputs and raw student records were not extracted.
- Notebook extracts map to originals through notebook-source-map.json; locations refer to zero-based cells. Existing unrelated historical extracts may remain on disk but are excluded from this build.
- Agent files now describe retention of family size and the provisional correction scenario. The lab archives and prior-experiments.md are absent in this checkout.
- Token usage/cost is unavailable; benchmark estimates below measure retrieval context, not actual extraction billing.
- Graph health counts: {"dangling_endpoint_edges": 0, "missing_endpoint_edges": 0, "self_loop_edges": 0, "undirected_same_endpoint_collapsed_edges": 17}. Same-endpoint relationships can collapse in the default undirected view; full extraction records are in graph-extraction.json and diagnostics are in graph-health.json.

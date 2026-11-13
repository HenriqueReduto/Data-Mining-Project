# Graph Report - Data Mining Project  (2026-11-13)

## Corpus Check
- Corpus is ~13,768 words - fits in a single context window. You may not need a graph.

## Summary
- 130 nodes · 207 edges · 8 communities
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Project governance and delivery
- Recorded student exploration
- Submission preprocessing decisions
- Course coding and validation
- Current and historical cleaning
- Clustering evidence and robustness
- Data representation and handoff
- Workspace integrity checks

## God Nodes (most connected - your core abstractions)
1. `Recorded-value exploration notebook` - 24 edges
2. `Coursework EDA and preprocessing notebook` - 20 edges
3. `Separate preprocessing notebook` - 7 edges
4. `Fill missing failures and absences with zero` - 7 edges
5. `Processed-data missingness assertion` - 7 edges
6. `Historical clustering metrics await code verification` - 5 edges
7. `Submission CSV parsing` - 5 edges
8. `Original reference notebook` - 5 edges
9. `Cluster stability and robustness requirements` - 4 edges
10. `CSV loading preserving literal education None` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Guided Python learning` --conceptually_related_to--> `Small sequential cells and explicit pandas`  [EXTRACTED]
  AGENTS.md → memory/course-baseline.md
- `Unconfirmed source meaning of count blanks` --conceptually_related_to--> `Cluster stability and robustness requirements`  [INFERRED]
  memory/data-audit.md → docs/project-brief.md
- `Submission count-feature zero filling` --semantically_similar_to--> `Fill missing failures and absences with zero`  [INFERRED] [semantically similar]
  notebooks/GroupXX_DMI_2627_EDA.ipynb → notebooks/data_preprocessing.ipynb
- `Executed notebook or notebook ZIP submission` --references--> `Fresh kernel reproducibility`  [EXTRACTED]
  docs/project-brief.md → AGENTS.md
- `Separate exploration and preprocessing` --conceptually_related_to--> `Exploration delivery copy pending validation`  [EXTRACTED]
  memory/decisions.md → PLAN.md

## Import Cycles
- 1-file cycle: `scripts/check_workspace.py -> scripts/check_workspace.py`

## Hyperedges (group relationships)
- **Recorded data exploration views** — graphify_out_notebook_sources_notebooks_data_exploration_ipynb_student_analytical_table, graphify_out_notebook_sources_notebooks_data_exploration_ipynb_binary_pearson_heatmap, graphify_out_notebook_sources_notebooks_data_exploration_ipynb_rating_spearman_heatmap, graphify_out_notebook_sources_notebooks_data_exploration_ipynb_categorical_percentage_tables [EXTRACTED 1.00]
- **Submission preprocessing flow** — graphify_out_notebook_sources_notebooks_groupxx_dmi_2627_eda_ipynb_submission_df_proc_working_copy, graphify_out_notebook_sources_notebooks_groupxx_dmi_2627_eda_ipynb_submission_count_feature_zero_filling, graphify_out_notebook_sources_notebooks_groupxx_dmi_2627_eda_ipynb_school_and_residence_median_imputation, graphify_out_notebook_sources_notebooks_groupxx_dmi_2627_eda_ipynb_binary_mode_imputation, graphify_out_notebook_sources_notebooks_groupxx_dmi_2627_eda_ipynb_ordinal_median_imputation, graphify_out_notebook_sources_notebooks_groupxx_dmi_2627_eda_ipynb_processed_data_missingness_assertion [EXTRACTED 1.00]
- **Clustering preparation and interpretation** — memory_course_reference_preprocessing_encoding_geometry, memory_course_reference_preprocessing_minmax_index, memory_course_reference_modelling_kmeans, memory_course_reference_modelling_original_unit_profiles, docs_project_brief_cluster_validation [INFERRED 0.85]
- **Reproducible guided notebook workflow** — agents_guided_python_learning, memory_course_baseline_small_cells, agents_fresh_kernel_validation, memory_course_reference_visualization_visual_validation [INFERRED 0.85]
- **Zero fill decision and uncertainty** — memory_decisions_zero_fill_counts, memory_data_audit_count_blank_semantics, memory_course_reference_preprocessing_zero_fill_checks, memory_decisions_current_decisions [INFERRED 0.85]

## Communities (8 total, 0 thin omitted)

### Community 0 - "Project governance and delivery"
Cohesion: 0.11
Nodes (19): Fresh kernel reproducibility, Guided Python learning, User approved methodological choices, Protected source material, Ten minute presentation and thirty minute defense, Proportionate educational support, Student segmentation and educational support, Executed notebook or notebook ZIP submission (+11 more)

### Community 1 - "Recorded student exploration"
Cohesion: 0.11
Nodes (24): Assessment-period grade distributions, Binary missing-response overlap, Binary Pearson heatmap, Binary Yes No features, Categorical percentage tables, Duplicate record evaluation, Family status guardian and size comparisons, Literal None preservation (+16 more)

### Community 2 - "Submission preprocessing decisions"
Cohesion: 0.15
Nodes (21): Binary mode imputation, Coursework EDA and preprocessing notebook, Final-grade-zero dropout hypothesis, Five educational exploration questions, Ordinal median imputation, Parental education mode filling, Processed-data missingness assertion, School and residence comparisons (+13 more)

### Community 3 - "Course coding and validation"
Cohesion: 0.17
Nodes (12): Distinguish lab patterns, adaptations and extensions, Twelve notebook course coding baseline, Small sequential cells and explicit pandas, Zero based lab source cell citations, Family cross tabulation extension, Numeric storage differs from measurement role, Missing count and percentage summaries, Pearson correlation heatmap (+4 more)

### Community 4 - "Current and historical cleaning"
Cohesion: 0.22
Nodes (13): Zero-fill hypothesis for count features, Before and after replacement checks, Fill missing failures and absences with zero, Independent raw input loading, Row shape index and count invariants, Separate preprocessing notebook, Unresolved student_data dependency, Working student_data_clean copy (+5 more)

### Community 5 - "Clustering evidence and robustness"
Cohesion: 0.23
Nodes (10): Cluster stability and robustness requirements, Methods absent from inspected lab notebooks, Explicit reproducible K means fitting, Original unit cluster profiles, Unconfirmed source meaning of count blanks, Reported eighty column all feature encoding, Pending feature and imputation comparisons, Reported ratings only imputation sensitivity (+2 more)

### Community 6 - "Data representation and handoff"
Cohesion: 0.23
Nodes (10): CSV loading preserving literal education None, Hierarchical clustering and Ward geometry, Proposed cleaned CSV handoff, Encoding choices change clustering distances, MinMax scaling with preserved row index, Working copy preserving raw records and identities, Before and after zero fill checks, Education None incorrectly parsed as missing (+2 more)

### Community 7 - "Workspace integrity checks"
Cohesion: 0.38
Nodes (5): hashlib (Python standard library), pathlib (Python standard library), re (Python standard library), main(), sys (Python standard library)

## Knowledge Gaps
- **30 isolated node(s):** `Protected source material`, `User approved methodological choices`, `Selected kernel and visual validation pending`, `Workspace ownership map`, `Dependency free workspace check` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 31 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Recorded-value exploration notebook` connect `Recorded student exploration` to `Current and historical cleaning`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Fill missing failures and absences with zero` (e.g. with `Zero-fill hypothesis for count features` and `Submission count-feature zero filling`) actually correct?**
  _`Fill missing failures and absences with zero` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Protected source material`, `User approved methodological choices`, `Selected kernel and visual validation pending` to the rest of the system?**
  _30 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project governance and delivery` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Why does `Coursework EDA and preprocessing notebook` connect `Submission preprocessing decisions` to `Recorded student exploration`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Should `Recorded student exploration` be split into smaller, more focused modules?**
  _Cohesion score 0.11231884057971014 - nodes in this community are weakly interconnected._
- **Why does `Fill missing failures and absences with zero` connect `Current and historical cleaning` to `Submission preprocessing decisions`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._

## Build scope and limitations

The corpus contains 19 files, including four notebook source extracts. Notebook cell outputs and raw student rows were excluded from semantic extraction. Git-ignored labs, private references and generated outputs were excluded by detection.

Semantic extraction used two host agents. Actual input/output token counts were unavailable from this host. Library counters contain zero placeholders and do not represent zero token use. No separate Gemini API was used.

Integrity checks found no missing or dangling endpoints and no self-loops. One opposite-direction pair collapses to a single connection in the default undirected visualization. The original 208 edge records are retained in graph.json.

The graph records source claims and hypotheses. It does not establish the correctness of preprocessing choices or fresh-kernel notebook execution.

graphify-out/ was written into the Git working tree and is currently unignored. Review its contents before committing or publishing.

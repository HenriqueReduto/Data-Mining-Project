# Modelling code patterns

Use this reference when the project reaches model preparation, fitting, evaluation, and profiles. The [core baseline](../course-baseline.md) resolves source IDs and zero-based indexes. Current features, transformations, cluster counts, and comparison methods require an explicit project decision. The patterns here support teaching and review.

## Prepare features and retain identities

Lab evidence is P4 cells 13–17, 79–84 and P4S cells 13–19. The source selects explicit feature lists, creates copies, checks correlation, and scales selected numeric measurements.

Establish what similarity should mean, which columns define it, and which columns describe profiles afterward. Preserve original-unit data for interpretation and a matching prepared matrix for fitting. Exclude the exported index from distance calculations. Verify missingness, finite values, column order, row index, encoding, and scaling before a model fit. Follow the [preprocessing reference](preprocessing.md) for the array-to-DataFrame reconstruction.

P4S drops a perfectly correlated feature and uses an unemployment threshold in its own exercise. Those choices are examples tied to that source dataset. Grade variables and related family/support variables require project-specific consideration of combined influence.

## Fit K-means explicitly

Lab evidence is P4 cells 40–47 and P4S cell 34. The source separates construction and fit and sets a seed for the final model.

This retains the lab example because adapting its feature set or cluster count would prescribe an unapproved model. `scaled_df_prod` must be the prepared product-feature table from that lab.

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=2, random_state=42, n_init=20)
model.fit(scaled_df_prod)
```

Inputs are the prepared matrix and model parameters. Output is a fitted estimator. Explain constructor arguments, `.fit`, `.labels_`, `.cluster_centers_`, and `.inertia_` separately. `n_init=20` is an explicit reproducibility adaptation to the source, to be recorded and evaluated in the project. The example k=2 remains a lab choice.

Check label count equals the input row count, inspect group sizes, and verify requested versus observed cluster counts. A fixed seed supports repeatability. Stability across seeds and plausible preprocessing alternatives still requires separate evaluation.

## Compare candidate cluster counts

Lab evidence is P4 cells 26, 28 and P4S cell 23. The source creates `ks`, collects inertias in a list, loops over candidates, fits, appends results, and plots.

```python
ks = range(1, 11)
inertias = []

for k in ks:
    candidate_model = KMeans(n_clusters=k, random_state=42, n_init=20)
    candidate_model.fit(scaled_df_prod)
    inertias.append(candidate_model.inertia_)
```

The input is one fixed feature matrix. Output is an inertia list aligned with candidate k values. Explain `range`, list creation, loop indentation, and `.append`. Use a supported candidate range appropriate to the number and distinctness of observations. Retain feature preprocessing and fitting settings across candidates.

The source elbow loops omit seeds and explicit n_init. Adding them supports repeatable comparison. P4 Markdown cell 23 combines elbow evidence with domain knowledge. Inertia alone cannot establish educational usefulness or final model quality.

## Profile in original units

Lab evidence is P4 cells 43–47, 56–63 and P4S cells 39, 42. P4 Markdown cell 43 explicitly motivates original-unit interpretation.

```python
profile_data = df_prod[scaled_df_prod.columns].copy()
profile_data['cluster'] = model.labels_

cluster_sizes = profile_data['cluster'].value_counts().sort_index()
cluster_summary = profile_data.groupby('cluster').describe().T
```

Inputs are the fitted model and original-unit rows in the identical order used for fitting. Outputs are sizes and descriptive profiles. Selecting the model feature columns excludes any label previously attached in the lab. `model` here must be the selected final model, fitted again after any candidate loop if necessary. Check index alignment before assigning an array of labels. Report category percentages with denominators as well as numerical profiles.

```python
original_centroids = scaler.inverse_transform(model.cluster_centers_)
```

The scaler and feature order must match the final fit. Output is a numeric centroid array in the original units of those scaled features. This operation applies to columns transformed by that scaler. P4S Markdown cell 53 illustrates cluster naming, feature meaning, and limitations. Grade differences are descriptive when grades formed part of model input.

## Hierarchical clustering

Lab evidence is P4 cells 32–36 and P4S cell 27. Ward, single, complete, and average appear as source alternatives.

```python
from scipy.cluster.hierarchy import linkage, dendrogram

hierarchical_tree = linkage(scaled_df_prod, method='ward')
dendrogram(hierarchical_tree, truncate_mode='lastp', p=12)
```

Input is the prepared feature matrix. Outputs are a linkage matrix and tree visualization. Explain merges and heights, and that truncation displays a summary of the tree. Verify the method and distance assumptions. The lab covers linkage and dendrograms; deriving a cut into labels and validating those assignments needs an explained extension. Ward is tied to Euclidean geometry.

## Categorical and mixed-data alternatives

P4 cells 70–76 demonstrate KModes with `.fit`, labels, and categorical summaries. P4 cells 79–92 demonstrate KPrototypes, a mixed feature copy, numeric-only scaling, categorical positions, and separate profiles.

The K-Prototypes positional pattern is P4 cell 84.

```python
cat_cols_idx = [
    scaled_df_mixed.columns.get_loc(column)
    for column in ['Gender', 'Education']
]
```

This lab example preserves its original columns. Explain list comprehensions as a repeated operation, `.get_loc` as column-position lookup, and why positions must match the actual matrix supplied to the model. P4 cell 88 passes those positions through `categorical=cat_cols_idx` during fit. Numeric codes can represent categorical variables, so infer roles from the data dictionary and modelling decision.

The source's `.dropna()` complete-case example requires a row-loss check when adapted to student data. KModes/KPrototypes require the kmodes dependency. P4 cell 68 includes a notebook installation command, which is a setup example. Follow the user's environment/install authorization before changing dependencies.

## Association rules as course coverage

Practical 3 concerns item transactions. P3 cells 21, 28–32 convert lists to transactions, create indicators and aggregate. P3 cells 50–64 demonstrate loops, lists, merges, and arithmetic. P3 cells 69–76 use mlxtend Apriori and association rules. P3S cells 17–19 use maximum aggregation for binary presence, and cells 25, 27, 29 compare support, lift, and confidence filters.

Explain lambda expressions, `.explode`, joins, and set operations when those tasks arise. Inspect grain and keys before aggregation. Counts and binary presence answer different questions. P3S cell 31 uses Series indexing after sorting; use explicit `.iloc` for positional access when adapting it. Association-rule examples establish course syntax and methods. Their use in this student-clustering project follows the assignment scope and agreed purpose.

## Extensions and validation gaps

Inspection of the 12 notebook sources found no demonstrated DBSCAN, SOM, PCA, Gower distance, StandardScaler, RobustScaler, silhouette, adjusted Rand index, resampling stability, Pipeline, SimpleImputer, KNNImputer, or OneHotEncoder workflow. This statement covers notebook sources only. It does not establish what the PDFs or other course material cover.

When extending the labs, explain purpose, syntax, inputs, outputs, package/version requirements, and validation. Consult current primary documentation for exact APIs before implementation. Historical project experiment results in `prior-experiments.md` require code verification before adoption. Numeric scores from different encoded feature spaces need contextual interpretation.

Before accepting a model comparison, check candidate settings, fixed input rows, transformations, metrics, group sizes, original-unit profiles, seed sensitivity, and plausible preprocessing alternatives. Record which checks were actually performed. The full assignment's distinctness, stability, robustness, and educational interpretation remain project requirements beyond the simplified lab solution.

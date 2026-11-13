# Prior experiments and verified dataset context

## Provenance and status

Recorded on 2026-11-12 at the user's request to preserve the supplied discussion context in agent files. Source is the attachment `C:/Users/henri/.codex/attachments/1a3cdd6c-b824-4229-94f3-ffe00dbf0579/Pasted text.txt`.

The dataset checks below were independently recalculated from `data/raw/student_data.csv` using a separate assistant Python runtime on 2026-11-12. Clustering metrics and experimental implementations are reported by the attachment and await verification against executable code and outputs. The attachment describes assignment coverage of RFM, hierarchical clustering, K-means, DBSCAN, and SOM. Check the assignment and project brief when establishing requirements.

## Directly rechecked CSV findings

- There are 649 records and 33 recorded features after excluding the exported index.
- Only 37 records are complete across all 33 features. For the six behavioral ratings, 520 records are complete and 129 have at least one missing rating.
- Observed medians are famrel 4, freetime 3, goout 3, Dalc 1, Walc 2, and health 4. These are valid whole-number response levels.
- Medu has 6 literal None values and 27 blanks. Fedu has 7 literal None values and 19 blanks. Loading with `keep_default_na=False, na_values=['']` preserves that distinction.
- Travel-time medians are 11 minutes for Urban and 22 for Rural. The 11 missing travel times comprise 7 Urban and 4 Rural students. School medians are 10.5 minutes for GP and 21 for MS.
- Study-time median is 186 weekly minutes. Pairwise observed Spearman correlations are approximately -0.0144 with travel time, 0.2352 with G1, 0.2266 with G2, and 0.2494 with G3.
- Earlier verified findings, definitions, family cross-checks, and missing counts remain in `data-audit.md` and PLAN.md.

## Historical preprocessing described by the user

- Nominal blanks became Unknown, preserving recorded other/no categories. U/R remained Urban/Rural, so Unknown was spelled out. Nominal features were one-hot encoded. Missing jobs supplied no evidence for unemployment or retirement. Mode imputation for nominal features was untested.
- Parental education was ordinally encoded from no education to higher education. Genuine blanks received Middle School Education, reported as the observed median level for both columns.
- Ratings received observed column medians. Unrounded mean and mode were compared. Rounded-mean imputation was untested.
- Travel-time blanks received residence-specific medians, with an overall-median fallback. School-based filling was discussed as an alternative.
- Study-time blanks received the overall median of 186 weekly minutes.
- In the historical all-feature experiment, failures/absences blanks and famsize zeros/blanks had a separate unresolved state. The current user decision fills missing failures and absences with zero, as recorded in `decisions.md`. Future comparisons must identify which treatment generated each result.
- Removing famsize remains open. Only joint removal with failures and absences was tested in the supplied history.
- Age and all three grades were included in the all-feature run. Grades were also removed together in a sensitivity check. Grade differences between clusters formed using grades are descriptive rather than independent validation.

## Reported ratings-only experiments

The baseline used six ratings, median imputation, and standardization. K-means and Ward compared two through six clusters.

| Experiment | Reported result |
| --- | --- |
| Median K-means, k=2 | Sizes 449/200, silhouette 0.243. Observed weekend-alcohol averages 1.61/3.77 and going-out averages 2.79/4.07. |
| Complete-rating sensitivity | Refit on 520 complete-rating students with scaling recalculated. ARI on those overlapping students 0.915 for median K-means. |
| Mean K-means, k=2 | Silhouette 0.243, complete-rating ARI 0.938. |
| Mode K-means, k=2 | Silhouette 0.246, complete-rating ARI 0.915. |
| Ward, k=2 | Median silhouette 0.178, mean 0.245, mode 0.161. Median baseline sizes 414/235. |
| Median DBSCAN | At 75th-percentile neighbor radius and min_samples=5, sizes 545/6 plus 98 noise points. |
| Median SOM | 5x5 map, all 25 nodes occupied, 12–50 students per node. |

The source preferred median for ordinal ratings because fills remain valid response levels and K-means results were similar across the three treatments. The complete-rating refit is a sensitivity check on overlapping students.

### Ratings one-hot experiment

Each rating became six possible categories including Unknown. This changes missingness treatment and the geometry of observed ratings together. Under one-hot encoding, distinct response levels have equal distance, regardless of their ordinal separation.

- Two-cluster K-means sizes were 440/209, silhouette 0.114 in its encoded space, complete-rating ARI 0.794, and agreement with median K-means ARI 0.464.
- Ward's best tested cut changed from two to three groups.
- DBSCAN at the 75th-percentile neighbor radius and min_samples=5 produced one cluster of 648 and one noise point.
- All 25 SOM nodes remained occupied.

## Reported all-feature experiment

All 33 features and 649 students were represented by 80 encoded columns. Ratings and education retained ordinal structure. Regular numerical/ordinal features used min-max scaling. Nominal one-hot blocks used a factor of 1/sqrt(2), giving a category change within one feature Euclidean distance 1. The custom encoding for famsize, failures, and absences mapped observed counts in order onto a quarter circle and assigned unresolved values an orthogonal state. Its implementation and methodological justification require review before reuse.

| Method | Reported result |
| --- | --- |
| K-means | Best tested k=2 among 2–6, seed 42, n_init=20. Sizes 394/255, silhouette 0.072, average G3 12.76/10.58. Going-out and weekend-alcohol means were nearly identical across groups. |
| Ward | Best tested cut k=2, sizes 366/283, silhouette 0.052. |
| DBSCAN | min_samples 5/10/12 and neighbor-radius percentiles 65/75/85/90/95 all produced one cluster plus noise. Example eps about 2.337, min_samples=5, 580 clustered and 69 noise. |
| SOM | 5x5 map, all 25 nodes occupied, 6–47 students per node. Final segmentation of nodes remained undefined. |

### Reported sensitivity checks

- Removing G1/G2/G3 gave K-means ARI 0.969 against the all-feature two-cluster fit.
- Removing famsize/failures/absences together gave K-means ARI 0.957 and silhouette 0.079 in the reduced space.
- Ward ARIs were about 0.308 after removing grades and 0.281 after removing the three unresolved-count features.
- The effects of removing famsize alone remain untested.
- Mean, mode, and one-hot-rating comparisons were performed on ratings-only data. Repeating them across all features remains open.

## Interpretation and follow-up

The supplied history describes two-cluster K-means as an interpretable exploratory summary with weak separation in the all-feature space. The ratings-only experiment addresses a narrower behavioral question. Silhouettes calculated under different feature spaces and encodings require contextual interpretation.

The source reports no dated events or monetary amounts for standard RFM. Any student-engagement adaptation needs explicit definitions, an observation window, and justified treatment of absences.

Before adopting a reported result, inspect its code, preprocessing, features, seeds, model parameters, and saved outputs. Reconcile the historical unresolved-count encoding with the current zero-fill decision. Preserve the open decisions about famsize alone, nominal imputation, all-feature imputation comparisons, and SOM segmentation.

# Feature roles for clustering: proposal

**Status:** proposal for group discussion, not a final decision.
**Next step it unblocks:** `clustering.ipynb` → "Review the feature roles and decide which variables define student similarity and which describe the resulting groups".

## 1. Approach: perspectives

Instead of putting all variables into one model, students are clustered from **three perspectives**, each answering one question. Putting everything together makes the clusters hard to interpret, and the first test model (all features, silhouette ≈ 0.08) mostly split students by school.

| Perspective | Question | What the school can offer |
|---|---|---|
| **Academic** | What types of students are there, by performance and effort? | Tutoring, study support |
| **Habits & engagement** | What types of students are there, by how they behave outside studying? | Mentoring, prevention, activities |
| **Family context** | What types of students are there, by the support and resources they have at home? | Homework clubs, device/internet access, family outreach |

## 2. Criteria used for each variable

A variable **forms** clusters only if it passes these checks, in order:

1. **Relevant:** it helps answer one perspective's question.
2. **Reliable:** few values imputed or corrected.
3. **Not redundant:** it adds something different from the other variables in the same perspective (one variable per concept).
4. **Indicates a need:** it points to a need or risk the school could support. Fixed personal characteristics (sex, age, school) are not used to form groups; this follows the brief's requirement that clusters guide support, not labels.
5. **Few binaries per perspective:** after scaling, 0/1 variables are always at the extremes and dominate the distance (in a test with 8 Yes/No and 6 ratings, the Yes/No took ~73% of the distance).

Variables that fail a check are kept to **describe** the clusters in the profiling.

## 3. Variables that form the clusters

### Academic
| Variable | Type | Why |
|---|---|---|
| G3 | Numerical | Final performance; G3 is the grade that decides the year (`data_inconsistencies.ipynb`) |
| failures | Numerical | Academic history; not redundant (r = −0.37 with G3 after filling). Assumption: missing = 0 |
| studytime | Numerical | Effort. Extreme values to be treated |
| higher | Binary | Aspiration; the ~10% who do not want higher education are a group worth identifying. Only binary in this perspective |

### Habits & engagement
| Variable | Type | Why |
|---|---|---|
| absences | Numerical | Engagement. Assumption: missing = 0. Extreme values to be treated |
| goout | Ordinal (1–5) | Lifestyle (social vs study-focused); r = 0.38 with Walc, not redundant |
| freetime | Ordinal (1–5) | Lifestyle; the school can offer activities |
| **total_alc** (new) | Ordinal sum (2–10) | Risk behaviour. Dalc + Walc (r = 0.62): same concept, combined so alcohol is not counted twice |
| activities | Binary | Engagement with school life; 48% "yes", so it separates students well. Only binary in this perspective |

### Family context
| Variable | Type | Why |
|---|---|---|
| **parent_edu** (new) | Ordinal (0–4) | Highest education of the two parents (Medu and Fedu, Spearman r = 0.64): how much help with homework there may be at home. Also resolves most "Unknown" values (if one parent is unknown, the other is used) |
| famsup | Binary | Educational support at home; 61% "yes" |
| internet | Binary | Resources at home; 77% "yes" |
| famrel | Ordinal (1–5) | Family climate; the school can offer counselling |

Two of four variables are binary here, the maximum we should allow; their weight should be checked.

## 4. Variables used to describe the clusters

| Variable | Why not used to form clusters |
|---|---|
| G1, G2 | Redundant with G3 (r = 0.83 and 0.92); useful to show how the year evolved |
| schoolsup, paid | Support the student **already receives**. More useful in the profiling: which clusters receive support and which do not (unmet needs). paid is also only ~6% "yes" |
| Dalc, Walc | Combined into total_alc |
| Medu, Fedu | Combined into parent_edu |
| Mjob, Fjob | Nominal with 5 categories → 10 one-hot columns that would dominate the distance; "other" is the most common category; partly captured by parent_edu |
| Pstatus | 88% "together" (very unbalanced); sensitive family situation |
| famsize | About 9% of values were replaced (sizes of 0 set to 1, an assumption), and family size does not indicate a need the school can support |
| guardian | 70% mother; useful in the profiling ("other" guardians) |
| school | Would split students by school (as in the first test model); painted on the clusters afterwards |
| sex, age, address | Fixed personal characteristics; grouping support by them is not appropriate |
| reason, nursery, romantic, health, traveltime | Do not indicate a current need the school can support |

## 5. Correlation check (preprocessed data)

Spearman correlations were computed within each perspective on `data/processed/student_data_preprocessed.csv` (latest version), including the new features `total_alc` and `parent_edu`. Spearman is used because most variables are ordinal (1–5 ratings, parent_edu) or binary. Correlations from the exploration notebook were not reused, because they were computed before missing values were filled (for example, failures–G3 was 0.01 on 98 students and is −0.44 on all 649).

| Perspective | Strongest relationships | Any pair above \|r\| = 0.8? |
|---|---|---|
| Academic | G3–failures −0.44; G3–higher 0.35; failures–higher −0.30 | No |
| Habits | goout–freetime 0.35; goout–total_alc 0.35 | No |
| Family | parent_edu–internet 0.24; all others ≈ 0 | No |

**Conclusion:** no variable is redundant, so the proposal stays as it is. The relationships are moderate and expected. Family variables are only weakly related to each other, which may lead to less distinct family clusters.

## 6. Encoding and scaling

### Encoding
| Variables | Type | Encoding |
|---|---|---|
| G3, failures, studytime, absences | Numerical | Unchanged |
| goout, freetime, famrel, total_alc | Ordinal | Unchanged (already ordered numbers) |
| parent_edu | Ordinal (0–4) | The 2 students with both parents unknown get the median (3) |
| higher, activities, famsup, internet | Binary | yes = 1, no = 0; "Unknown" replaced with the mode (as agreed: yes, no, yes, yes) |

### Scaling: StandardScaler instead of MinMax
The share of the distance taken by each variable after scaling (its variance over the sum of variances):

| Perspective | MinMaxScaler | StandardScaler |
|---|---|---|
| Academic | G3 16%, failures 21%, studytime 14%, **higher 50%** | 25% each |
| Habits | **absences 4%**, goout 17%, freetime 14%, total_alc 12%, **activities 52%** | 20% each |
| Family | parent_edu 14%, famrel 10%, **famsup 44%, internet 33%** | 25% each |

With MinMax, a single binary variable takes about half of each perspective's distance, because 0/1 values always sit at the extremes of the range, while absences is squeezed by a few very high values. The academic clustering would mostly group students by whether they want higher education rather than by their grades. **StandardScaler** (z-scores) gives every variable variance 1, so all variables weigh the same, as in the SOM class (z-scores, each source "an eighth" of the distance).

Side effect: rare values become extreme z-scores. The ~10% of students without higher-education aspirations get z ≈ −3 (acceptable, a group worth identifying), but a student with 32 absences gets z ≈ 6.1. **Extreme values of studytime and absences must therefore be treated before scaling.**

## 7. Extreme values (studytime and absences)

Only studytime and absences need treatment, because traveltime only describes the clusters. Both have long right tails: the gaps between percentiles grow towards the top (studytime: median 186, 90th percentile 510, maximum 1465 minutes; absences: median 2, 90th percentile 10, maximum 32).

| | studytime | absences |
|---|---|---|
| Above the upper whisker (IQR rule) | 53 students (8.2%): a long tail rather than isolated outliers | 20 students (3.1%) |
| Real or errors? | Real: these students get higher grades (G3 13.2 vs 11.8) and have fewer past failures | Real: these students get lower grades (G3 10.7 vs 11.9) and have more past failures |
| Treatment for the clustering | Capped at the upper whisker (547 minutes) | Log-transformed (log1p) |
| Result | Skew 0.85, no student with \|z\| > 3 | Skew 0.25, no student with \|z\| > 3 |

Options compared (skew, and number of students with |z| > 3 after standardising):

| Option | studytime | absences |
|---|---|---|
| Keep | 2.55, 18 | 2.07, 11 |
| Cap at upper whisker | **0.85, 0** | 1.29, 0 |
| Square root | 0.92, 13 | 0.45, 2 |
| log1p | −1.25, 11 | **0.25, 0** |

A log transform was not used for studytime because three students with 0–2 minutes would become new extremes at the bottom (z = −4.7). The transformed versions (`studytime_clip`, `absences_log`) are used only for the clustering; the original values are kept for the profiling.

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
| famsize | Unreliable: 14% of values were corrected |
| guardian | 70% mother; useful in the profiling ("other" guardians) |
| school | Would split students by school (as in the first test model); painted on the clusters afterwards |
| sex, age, address | Fixed personal characteristics; grouping support by them is not appropriate |
| reason, nursery, romantic, health, traveltime | Do not indicate a current need the school can support |

## 5. Implications for the next steps

- **New features to create:** `total_alc = Dalc + Walc` and `parent_edu = max(Medu, Fedu)` (ordinal: None 0, Primary 1, Middle School 2, Secondary 3, Higher 4).
- **Extreme values:** since traveltime only describes clusters, its extremes do not affect the models. The pending treatment only matters for **studytime** and **absences**.
- **"Unknown" values:** as agreed, the main clustering uses the mode for Yes/No variables (one 0/1 column), with the Unknown version as a robustness check.
- **Per perspective:** scale (MinMax), choose k (elbow + dendrogram + silhouette), compare K-means and Ward (crosstab), then profile with original values and the describing variables.

## 6. Open questions for the group

1. Do we agree with the three perspectives and the variables in each?
2. `parent_edu` as the maximum of both parents, or only Medu (slightly more related to G3: 0.28 vs 0.24)?
3. Should `absences` be academic rather than habits?
4. Do we cluster each perspective separately and then cross them (as in the class example), or pick one main perspective?

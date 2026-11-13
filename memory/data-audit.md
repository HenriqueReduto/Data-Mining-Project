# Starting data and notebook audit

Verified on 2026-11-10 through read-only CSV, JSON, DOCX XML, and assignment PDF inspection. Recheck against the current source before relying on exact counts. The supplied notebooks were inspected, not rerun.

## Files and execution state
- `../notebooks/reference/datamining1.ipynb` and `../notebooks/datamining1.ipynb` are byte-identical original notebooks, each with 25 cells. Their SHA-256 is `a6eaac9fed21f86808f15ff7ad4f0f4fbcb9e01f10100821bfb22edd54d9710f`.
- They import pandas, NumPy, Matplotlib, and Seaborn, inspect the data, drop failures, and median-fill absences. Multivariate analysis is only a comment; clustering and final interpretation are absent.
- They contain almost no explanatory Markdown; a preprocessing heading is a code comment. The saved kernel metadata says Python 3.11.14, but this does not establish the user's current VS Code kernel.
- Loading uses `pd.read_csv('student_data.csv')`, which is now a historical path in both preserved originals. New working code must load from the documented raw-data location; the original notebook code was not rewritten during organization. The saved working-directory output refers to a different machine path.
- No project dependency manifest or validated execution command was found during initial inspection. Versions and fresh-kernel execution remain unverified.

## CSV facts
- `../data/raw/private/student_data.csv` has 649 rows and 34 imported columns, including a blank-header exported row index named `Unnamed: 0` by pandas. That index is exactly 0 through 648.
- No exact duplicate rows were found, either with or without the exported index.
- G1, G2, and G3 have no blanks and observed ranges 0-19. They are grades out of 20 according to the assignment.
- The assignment defines family size as a number of people and travel/study time in minutes. Use these project definitions rather than assumptions about another version of a similar dataset.

## Education parsing issue
Read literal categories separately from blank cells. The existing default `read_csv` call interprets the text `None` as missing, inflating the apparent missingness.

| Field | Blank cells | Literal text None | Existing notebook's apparent missing count |
| --- | ---: | ---: | ---: |
| Medu | 27 | 6 | 33 |
| Fedu | 19 | 7 | 26 |

Read-only verification used `pd.read_csv(path, keep_default_na=False, na_values=[''])`. This distinguishes blanks from the literal education category; teach and verify the parameters before adopting the loading cell. The other observed education categories are Primary Education, Middle School Education, Secondary Education, and Higher Education.

## High-impact issues to investigate
Current treatment decision (2026-11-12): the user reconfirmed zero replacement for missing `failures` and `absences` in the working dataset. Apply the decision recorded in `decisions.md`; the source meaning of blanks remains unverified. The table below preserves the original observations and investigation questions.

| Field | Verified observation | Unresolved question |
| --- | --- | --- |
| failures | 551 blanks (84.9%); observed values only 1, 2, 3 | Are blanks genuinely unknown, or do they encode zero in this source? No proof yet. The existing notebook drops the field. |
| absences | 260 blanks (40.1%); observed 1-32, no recorded zero | What do blanks mean? Existing notebook fills them with the observed median, 4; this is not an approved final treatment. |
| famsize | 3 blanks; 57 zeros; observed range 0-9 | What explains zeros and how should they be treated? Of zero-family-size rows, 41 have Pstatus T, 13 A, and 3 blank. |
| traveltime | 11 blanks; 29 zeros; observed range 0-144 minutes | Are zero durations plausible, rounded, or erroneous? |
| studytime | 14 blanks; 3 zeros; observed range 0-1465 weekly minutes | Which values are plausible and whether transformation is warranted? |
| address | 17 blanks | The Word notes say 7; the CSV is the evidence for the observed count. |

Missingness or unusual values alone do not establish a mechanism or justify deleting a feature. Keep hypotheses, observations, and approved treatments distinct; use sensitivity comparisons where uncertainty materially affects conclusions.

## Word notes status
`../docs/references/private/Missing Values Analyses.docx` contains preliminary proposals, not validated requirements. It suggests mapping missing education to None because that category appears absent, but the literal category is actually present in the raw CSV. Unknown parental employment cannot establish unemployment or retirement. The notes also propose revisiting family size, parental status, and travel time; these remain investigation items.

## Assignment clarification
The evaluation table on page 8 gives presentation 5% / one point, whereas the page 10 presentation heading says two points. This is an observed source inconsistency, not a resolved instructor clarification. The full grading breakdown and delivery requirements are retained in `../docs/project-brief.md`.

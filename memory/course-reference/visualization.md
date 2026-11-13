# Visualization code patterns

Use this reference for charts in exploration and later model interpretation. Resolve source IDs and zero-based cell indexes through the [core baseline](../course-baseline.md). Read actual source cells before adapting a chart. Plotting packages and user-kernel execution need verification before promising rendered results.

## Plotting setup and teaching sequence

Lab evidence is P1 cells 100, 102, P1S cell 2 and P4 cell 9.

```python
import matplotlib.pyplot as plt
import seaborn as sns
```

Explain aliases once. Each plot cell should follow a Markdown question/purpose, use named columns, label units, and be followed by an interpretation of the actual output. The labs vary colors and sizes. They establish no universal project palette.

## Numerical distribution

Lab evidence is P1 cells 107, 109 and P2 cell 87.

```python
sns.histplot(data=student_data, x='studytime', bins=20)
plt.title('Recorded weekly study time')
plt.xlabel('Weekly study time (minutes)')
plt.ylabel('Students')
plt.show()
```

Input is the recorded student table. Output is a histogram of observed study times. Explain `data`, `x`, `bins`, and `plt.show()`. The 20 bins are an illustrative display setting, which may be adjusted after viewing the distribution. Check missing-count coverage, the upper tail, and whether binning obscures values near zero. Report the observed denominator alongside the interpretation.

```python
sns.boxplot(data=student_data, x='traveltime')
plt.title('Recorded home-to-school travel time')
plt.xlabel('Travel time (minutes)')
plt.show()
```

A boxplot displays median, quartiles, whiskers, and separately plotted extremes according to its settings. Inspect the extreme records. Source P2 Markdown cell 92 warns about subjective outlier removal and information loss. A boxplot flag supplies an investigation lead, so treatment still needs domain evidence and a user decision.

## Category counts

Lab evidence is P1 cell 119, which uses `countplot`, `hue`, and an explicit category order.

```python
sns.countplot(data=student_data, x='school')
plt.title('Students by recorded school')
plt.xlabel('School')
plt.ylabel('Students')
plt.show()
```

Output is a count bar for each observed category. Missing categories generally require explicit handling to appear. Compare plotted totals with frequency tables. When using `hue`, inspect subgroup counts as well as totals. Ordered ratings need the intended 1–5 order and retain their rating meaning. Only show meaningful zero-count categories deliberately.

## Relationship between two measurements

Lab evidence is P1 cells 112, 116 and P1S cells 23, 25.

```python
sns.scatterplot(data=student_data, x='studytime', y='G3', hue='school')
plt.title('Study time and final grade by school')
plt.xlabel('Weekly study time (minutes)')
plt.ylabel('Final grade (0–20)')
plt.show()
```

Explain axes and `hue` as a third displayed variable. Rows with missing plotted values may be omitted. Check the complete-pair count and possible overplotting. High study time with low grades can be plausible. Describe the association visible in the chart and consider subgroup distributions before giving it educational meaning.

## Correlation heatmap

Lab evidence is P2 cells 139–140 and P4S cell 16.

```python
grade_correlation = student_data[['G1', 'G2', 'G3']].corr()

plt.figure(figsize=(6, 4))
sns.heatmap(grade_correlation, annot=True, vmin=-1, vmax=1, center=0)
plt.title('Correlation between assessment-period grades')
plt.tight_layout()
plt.show()
```

Input is a deliberately selected set of numeric columns. Output is a pairwise correlation matrix and figure. Explain `.corr()`, annotation, and fixed color limits. Inspect missingness and constants. The default Pearson coefficient describes linear association. Zero correlation can coexist with a nonlinear relationship. P2 Markdown cell 138 discusses Pearson and Spearman, including ordinal suitability. Adding a Spearman code calculation extends the shown heatmap implementation and should state the selected method and purpose.

## Multiple features and loops

Lab evidence is P2S cell 44, which uses `ceil`, `plt.subplots`, `zip`, `axes.flatten`, and a `for` loop to draw boxplots.

Teach the single-feature plot first. Introduce loops when repeating the same well-understood operation across an explicit feature list. Explain the loop variable, iterable, colon, and indentation. For subplots, explain the figure and axes array before flattening it. Ensure all requested features receive an axis and hide unused axes deliberately. Use units and scales appropriate to each feature.

Avoid handing the learner a grid-building framework before they understand one plot. Conversely, loops and list comprehensions are established course syntax and may be introduced when repetition warrants them.

## Model figures

P4 cell 28 demonstrates an elbow curve with explicit k ticks. P4 cell 36 demonstrates a truncated dendrogram. P4 cells 53, 63 and P4S cells 45, 48–51 demonstrate original-unit cluster comparisons, labeled histograms with transparency, and centroid markers.

For comparisons, keep feature definitions, axes, bin edges, and label meanings consistent. Cluster labels are arbitrary identifiers. Only plot centroids in original units after inverse-transforming them with the matching scaler and feature order. Add titles, units, legends, and group sizes where needed to interpret the figure.

## Visual check before completion

Execute the chart cell and inspect the rendered output at normal reading size. Check labels, missing groups, legend overlap, clipped axes, plotted population, and consistency with its table. A successful code run alone does not verify readability. Keep plots in notebook outputs for reproducibility. Export additional figures when the presentation or submission needs them.

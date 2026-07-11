## The Problem: One Metric Does Not Fit All

When monitoring deployed ML systems, the temptation is to track a single metric like accuracy and call it done. But this approach is dangerously incomplete. Different types of ML systems require different metrics, and even within a single system, multiple metrics are needed to understand true performance.

Consider a fraud detection system with 99% accuracy. Sounds great, right? But if only 1% of transactions are fraudulent, a model that predicts "not fraud" for everything achieves 99% accuracy while catching zero fraud. This illustrates why accuracy alone is insufficient for imbalanced classification.

Similarly, for a regression model predicting house prices, knowing the average error tells you one story. But knowing the root mean squared error (which penalizes large errors more heavily) tells you whether the model occasionally makes catastrophic predictions.

For ranking systems like search or recommendations, neither classification nor regression metrics apply. What matters is whether relevant items appear near the top of the list.

Effective ML monitoring requires selecting the right metrics for your system type.

---

## Classification Metrics

Binary classification predicts one of two classes, typically labeled 0 (negative) and 1 (positive). The fundamental building blocks for classification metrics are the four cells of the confusion matrix:

**True Positives (TP)**: Model predicted positive, actual was positive. These are correct positive predictions.

**True Negatives (TN)**: Model predicted negative, actual was negative. These are correct negative predictions.

**False Positives (FP)**: Model predicted positive, actual was negative. These are false alarms, also called Type I errors.

**False Negatives (FN)**: Model predicted negative, actual was positive. These are missed detections, also called Type II errors.

From these four quantities, we derive the standard classification metrics:

---

### Accuracy

Accuracy measures the overall fraction of correct predictions:

$$
\text{accuracy} = \frac{TP + TN}{TP + TN + FP + FN} = \frac{\text{correct predictions}}{\text{total predictions}}
$$

**When accuracy is useful**: When classes are balanced (roughly equal numbers of positives and negatives) and both types of errors are equally costly.

**When accuracy is misleading**: With imbalanced data. If 99% of samples are negative, predicting all negatives gives 99% accuracy while being useless.

---

### Precision

Precision measures the quality of positive predictions: of all samples the model labeled positive, how many actually were positive?

$$
\text{precision} = \frac{TP}{TP + FP}
$$

**When precision matters**: When false positives are costly. For spam filters, low precision means legitimate emails end up in spam. For medical diagnoses, low precision means unnecessary treatments.

**Edge case**: If the model never predicts positive (TP = 0, FP = 0), precision is undefined (0/0). By convention, return 0.0 in this case.

---

### Recall (Sensitivity)

Recall measures the coverage of actual positives: of all samples that were actually positive, how many did the model catch?

$$
\text{recall} = \frac{TP}{TP + FN}
$$

**When recall matters**: When false negatives are costly. For fraud detection, low recall means fraudulent transactions slip through. For disease screening, low recall means missing sick patients.

**Edge case**: If there are no actual positives (TP = 0, FN = 0), recall is undefined. By convention, return 0.0.

---

### F1 Score

The F1 score is the harmonic mean of precision and recall, providing a single metric that balances both:

$$
\text{F1} = \frac{2 \times \text{precision} \times \text{recall}}{\text{precision} + \text{recall}} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}
$$

The harmonic mean (rather than arithmetic mean) is used because it penalizes extreme imbalances. If either precision or recall is very low, F1 will be low.

**When F1 matters**: When you need a single number that reflects both precision and recall, and you care about both false positives and false negatives.

**Edge case**: If both precision and recall are 0, F1 is undefined (0/0). Return 0.0.

---

## Regression Metrics

Regression models predict continuous values. The key question is: how far off are the predictions from the actual values?

---

### Mean Absolute Error (MAE)

MAE is the average of the absolute differences between predictions and actual values:

$$
\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|
$$

where $y_i$ is the actual value and $\hat{y}_i$ is the predicted value.

**Properties of MAE**:
- Same units as the target variable (if predicting dollars, MAE is in dollars)
- Treats all errors equally regardless of size
- Robust to outliers compared to RMSE
- Intuitive interpretation: "on average, predictions are off by X"

---

### Root Mean Squared Error (RMSE)

RMSE is the square root of the average of squared differences:

$$
\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}
$$

**Properties of RMSE**:
- Same units as the target variable
- Penalizes large errors more than small errors (due to squaring)
- Sensitive to outliers
- If you care about avoiding big mistakes, RMSE is more appropriate than MAE

**Relationship between MAE and RMSE**: RMSE is always greater than or equal to MAE. The gap indicates how much variation exists in error magnitudes. If RMSE is much larger than MAE, there are some predictions with very large errors.

---

## Ranking Metrics

Ranking systems produce an ordered list of items. The goal is to place relevant items (those the user wants) near the top. Traditional classification metrics do not apply because we care about position, not just binary correctness.

---

### Precision at K

Precision at K measures the fraction of relevant items among the top K positions:

$$
\text{precision@K} = \frac{\text{relevant items in top K}}{K}
$$

For example, if you show 3 search results and 2 are relevant, precision@3 = 2/3 = 0.667.

**When precision@K matters**: When you have limited screen real estate or attention. Users often only look at the first few results, so getting those right is crucial.

---

### Recall at K

Recall at K measures the fraction of all relevant items that appear in the top K positions:

$$
\text{recall@K} = \frac{\text{relevant items in top K}}{\text{total relevant items}}
$$

**When recall@K matters**: When you want to ensure users can find most of what they are looking for within the top results.

**Relationship to precision@K**: There is a natural tension. Increasing K typically increases recall (more chances to include relevant items) but may decrease precision (more irrelevant items sneak in).

**Edge case**: If there are no relevant items at all (total relevant = 0), recall@K is undefined. By convention, return 0.0.

---

## Computing Ranking Metrics

To compute precision@K and recall@K:

**Step 1**: Pair each prediction score with its corresponding relevance label (typically 0 for irrelevant, 1 for relevant).

**Step 2**: Sort all pairs by predicted score in descending order (highest scores first).

**Step 3**: Take the top K items after sorting.

**Step 4**: Count how many of those K items have relevance = 1.

**Step 5**: Divide by K for precision@K.

**Step 6**: Divide by total number of relevant items for recall@K.

---

## A Comprehensive Example

**Classification System (Fraud Detection)**

Given predictions and actuals for 10 transactions:
- Predictions: [1, 1, 0, 1, 0, 0, 1, 0, 0, 0]
- Actuals:     [1, 0, 0, 1, 1, 0, 0, 0, 1, 0]

Computing the confusion matrix:
- Position 1: pred=1, actual=1 -> TP
- Position 2: pred=1, actual=0 -> FP
- Position 3: pred=0, actual=0 -> TN
- Position 4: pred=1, actual=1 -> TP
- Position 5: pred=0, actual=1 -> FN
- Position 6: pred=0, actual=0 -> TN
- Position 7: pred=1, actual=0 -> FP
- Position 8: pred=0, actual=0 -> TN
- Position 9: pred=0, actual=1 -> FN
- Position 10: pred=0, actual=0 -> TN

Totals: TP=2, TN=4, FP=2, FN=2

Metrics:
- Accuracy = (2+4)/(2+4+2+2) = 6/10 = 0.60
- Precision = 2/(2+2) = 0.50
- Recall = 2/(2+2) = 0.50
- F1 = 2 * 0.50 * 0.50 / (0.50 + 0.50) = 0.50

---

**Regression System (Price Prediction)**

Given predictions and actuals for 5 houses (in thousands):
- Predictions: [250, 300, 180, 420, 350]
- Actuals:     [260, 290, 200, 400, 355]

Differences:
- House 1: |250-260| = 10, (250-260)^2 = 100
- House 2: |300-290| = 10, (300-290)^2 = 100
- House 3: |180-200| = 20, (180-200)^2 = 400
- House 4: |420-400| = 20, (420-400)^2 = 400
- House 5: |350-355| = 5, (350-355)^2 = 25

MAE = (10+10+20+20+5)/5 = 65/5 = 13.0 (thousand dollars)
RMSE = sqrt((100+100+400+400+25)/5) = sqrt(1025/5) = sqrt(205) = 14.32 (thousand dollars)

---

**Ranking System (Search Results)**

Given 8 items with predicted relevance scores and true relevance:
- Scores:    [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
- Relevance: [1,   0,   1,   0,   1,   0,   0,   1]

Top 3 items (by score): positions 1, 2, 3 with relevance [1, 0, 1]

Total relevant items: 4 (positions 1, 3, 5, 8)

Precision@3 = 2/3 = 0.667 (2 relevant in top 3)
Recall@3 = 2/4 = 0.50 (2 out of 4 total relevant items in top 3)

---

## Handling Division by Zero

In all metrics involving division, edge cases can produce 0/0 situations:

- **Precision**: If TP + FP = 0 (no positive predictions), return 0.0
- **Recall**: If TP + FN = 0 (no actual positives), return 0.0
- **F1**: If precision + recall = 0, return 0.0
- **Recall@K**: If total relevant = 0, return 0.0

The convention of returning 0.0 (rather than raising an error) ensures that monitoring pipelines continue running even with edge case data.

---

## Where Metric Selection Shows Up

**Model Development**: Data scientists choose evaluation metrics based on business objectives and class balance during training.

**Production Monitoring**: MLOps teams configure dashboards with metrics appropriate for each deployed model type.

**A/B Testing**: Experiment platforms track multiple metrics to understand the full impact of model changes.

**SLA Definitions**: Business stakeholders define acceptable performance thresholds in terms of specific metrics.

**Alerting**: Monitoring systems trigger alerts when metrics fall below thresholds, using the right metric for each model type.
## What Is Calibration?

A model is **well-calibrated** if its predicted probabilities match actual frequencies. When the model says "80% confident," it should be correct 80% of the time.

**Example of good calibration:**
- Among predictions with 90% confidence: 90% are correct
- Among predictions with 70% confidence: 70% are correct
- Among predictions with 50% confidence: 50% are correct

**Example of poor calibration:**
- Among predictions with 90% confidence: only 60% are correct (overconfident)
- Among predictions with 30% confidence: actually 70% are correct (underconfident)

A model can have high accuracy but poor calibration. It might correctly classify 95% of items but assign 99% confidence to everything, making it overconfident.

---

## Why Calibration Matters

**Decision making:**
If a medical model says "90% chance of disease," a doctor needs to trust that probability. If the model is overconfident, patients get unnecessary treatments.

**Ensemble methods:**
Combining predictions from multiple models works best when probabilities are meaningful.

**Uncertainty quantification:**
In safety-critical applications, we need to know when the model is uncertain.

**Selective prediction:**
Systems that can "abstain" when uncertain need calibrated confidence scores.

---

## The Expected Calibration Error Formula

ECE measures the average gap between predicted confidence and actual accuracy, weighted by how many samples fall in each confidence range.

$$
\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{n} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|
$$

where:
- $M$ is the number of bins
- $B_m$ is the set of samples in bin $m$
- $|B_m|$ is the number of samples in bin $m$
- $n$ is the total number of samples
- $\text{acc}(B_m)$ is the accuracy of samples in bin $m$
- $\text{conf}(B_m)$ is the average confidence of samples in bin $m$

---

## The Binning Process

**Step 1: Choose the number of bins**

Typically $M = 10$ or $M = 15$. More bins give finer resolution but may have sparse bins.

**Step 2: Define bin boundaries**

For $M = 10$: bins are [0, 0.1), [0.1, 0.2), ..., [0.9, 1.0]

**Step 3: Assign each prediction to a bin**

A prediction with confidence 0.73 goes in bin [0.7, 0.8).

**Step 4: For each bin, compute accuracy and average confidence**

---

## Worked Example

100 predictions with $M = 5$ bins: [0, 0.2), [0.2, 0.4), [0.4, 0.6), [0.6, 0.8), [0.8, 1.0]

**Bin 1 [0, 0.2):** 5 samples, avg confidence = 0.15, accuracy = 0.20

**Bin 2 [0.2, 0.4):** 10 samples, avg confidence = 0.30, accuracy = 0.30

**Bin 3 [0.4, 0.6):** 25 samples, avg confidence = 0.52, accuracy = 0.48

**Bin 4 [0.6, 0.8):** 35 samples, avg confidence = 0.71, accuracy = 0.60

**Bin 5 [0.8, 1.0):** 25 samples, avg confidence = 0.92, accuracy = 0.76

**Computing ECE:**

Bin 1: $(5/100) \times |0.20 - 0.15| = 0.05 \times 0.05 = 0.0025$

Bin 2: $(10/100) \times |0.30 - 0.30| = 0.10 \times 0.00 = 0.0000$

Bin 3: $(25/100) \times |0.48 - 0.52| = 0.25 \times 0.04 = 0.0100$

Bin 4: $(35/100) \times |0.60 - 0.71| = 0.35 \times 0.11 = 0.0385$

Bin 5: $(25/100) \times |0.76 - 0.92| = 0.25 \times 0.16 = 0.0400$

**ECE = 0.0025 + 0.0000 + 0.0100 + 0.0385 + 0.0400 = 0.091**

The model has 9.1% calibration error. Bins 4 and 5 show the model is overconfident at high confidence levels.

---

## Interpreting ECE

**ECE = 0:** Perfect calibration. Predicted probabilities exactly match observed frequencies.

**ECE close to 0 (e.g., 0.01-0.03):** Well calibrated.

**ECE moderate (e.g., 0.05-0.10):** Some calibration issues. May need temperature scaling.

**ECE high (e.g., > 0.15):** Poorly calibrated. Probabilities are not trustworthy.

---

## Reliability Diagrams

A reliability diagram visualizes calibration:

**X-axis:** Average predicted confidence per bin

**Y-axis:** Actual accuracy per bin

**Perfect calibration:** Points fall on the diagonal line $y = x$

**Overconfident:** Points below the diagonal (accuracy < confidence)

**Underconfident:** Points above the diagonal (accuracy > confidence)

The gap between each point and the diagonal, weighted by bin size, gives ECE.

---

## Bin Weighting

ECE weights each bin by its sample count $|B_m|/n$. This makes sense because:
- Bins with more samples contribute more to overall error
- Sparse bins with few samples have less impact
- The weighting reflects the distribution of model confidence

---

## Maximum Calibration Error (MCE)

An alternative metric that looks at the worst-case bin:

$$
\text{MCE} = \max_m \left| \text{acc}(B_m) - \text{conf}(B_m) \right|
$$

MCE is useful when you care about worst-case miscalibration, not average miscalibration.

---

## Handling Multi-Class Problems

For multi-class classification:
- Use the confidence of the predicted class (max probability)
- A prediction is "correct" if the predicted class matches the true class
- The rest of the ECE calculation is identical

---

## Common Calibration Issues

**Overconfidence (most common):**
Modern neural networks are typically overconfident. They assign high probabilities even when wrong.

**Underconfidence:**
Some models, especially after certain regularization, may be underconfident.

**Non-monotonic miscalibration:**
Overconfident at some ranges, underconfident at others.

---

## Fixing Calibration

**Temperature scaling:**
Divide logits by a learned temperature $T$ before softmax. $T > 1$ softens probabilities (fixes overconfidence).

**Platt scaling:**
Fit a logistic regression on the logits to map to calibrated probabilities.

**Isotonic regression:**
Non-parametric calibration using isotonic regression on a held-out set.

**Histogram binning:**
Directly adjust probabilities based on observed bin accuracies.

All these methods are applied post-training and require a calibration dataset.

---

## Limitations of ECE

**Bin sensitivity:**
Different numbers of bins give different ECE values. There is no "correct" number of bins.

**Sparse bins:**
Bins with few samples have unreliable accuracy estimates.

**Assumes binning is appropriate:**
ECE assumes calibration errors are well-captured by discrete bins.

**Does not measure sharpness:**
A model predicting 50% for everything is perfectly calibrated but useless. ECE does not penalize this.
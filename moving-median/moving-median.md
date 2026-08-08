## What Is a Moving Median?

A moving median is the median of the most recent $w$ observations in a time series. It is a robust smoothing technique that resists outliers better than moving averages.

$$
\text{MM}_t(w) = \text{median}(y_{t-w+1}, y_{t-w+2}, ..., y_t)
$$

where $w$ is the window size.

---

## The Formula

For a time series $y_1, y_2, ..., y_T$, the moving median at time $t$ with window $w$ is:

$$
\text{MM}_t = \text{median}\{y_{t-w+1}, y_{t-w+2}, ..., y_t\}
$$

**Odd window size:** Median is the middle value.

**Even window size:** Median is the average of two middle values.

---

## Worked Example

**Time series:** [10, 15, 12, 100, 14, 13, 16]

**Window size:** $w = 3$

**Calculations:**

**$t=3$:** Median of {10, 15, 12}

Sorted: [10, 12, 15] → Median = 12

**$t=4$:** Median of {15, 12, 100}

Sorted: [12, 15, 100] → Median = 15

**$t=5$:** Median of {12, 100, 14}

Sorted: [12, 14, 100] → Median = 14

**$t=6$:** Median of {100, 14, 13}

Sorted: [13, 14, 100] → Median = 14

**$t=7$:** Median of {14, 13, 16}

Sorted: [13, 14, 16] → Median = 14

**Result:** [NaN, NaN, 12, 15, 14, 14, 14]

**Note:** Outlier 100 has minimal impact on median values.

---

## Comparison with Moving Average

**Same data with moving average ($w=3$):**

**$t=3$:** $(10+15+12)/3 = 12.33$

**$t=4$:** $(15+12+100)/3 = 42.33$ (heavily influenced by outlier)

**$t=5$:** $(12+100+14)/3 = 42.00$

**$t=6$:** $(100+14+13)/3 = 42.33$

**$t=7$:** $(14+13+16)/3 = 14.33$

**Observation:** Moving average distorted by outlier for multiple periods. Moving median remains stable.

---

## Robustness to Outliers

**Breakdown point:** Proportion of outliers that can be tolerated.

**Moving median:** Approximately 50% breakdown point.

Up to half of values in window can be outliers without severely affecting result.

**Moving average:** 0% breakdown point.

Single extreme outlier can arbitrarily distort average.

**Application:** Use moving median when data contains outliers, spikes, or measurement errors.

---

## Computational Complexity

**Naive approach:**

For each position, extract window, sort, find median.

Time: $O(w \log w)$ per position, $O(Tw \log w)$ total.

**Efficient approach:**

Maintain sorted structure (balanced tree or specialized median heap).

Time: $O(\log w)$ per update, $O(T \log w)$ total.

**Comparison to moving average:** $O(T)$ for moving average vs $O(T \log w)$ for moving median.

**Trade-off:** Slower but more robust.

---

## Window Size Selection

**Small window (e.g., $w=3$):**

- Responsive to changes
- Follows data closely
- Less smoothing

**Large window (e.g., $w=25$):**

- More smoothing
- Better outlier resistance
- Less responsive (lag)

**General guidance:**

- For outlier removal: $w \geq 5$
- For trend extraction: $w \geq 10$
- Odd $w$ preferred (unique median without averaging)

---

## Edge Handling

**At the start ($t < w$):**

Cannot compute full moving median.

**Options:**

1. Leave as NaN (most common)
2. Use expanding window: Median of all values from 1 to $t$
3. Pad with initial value or median of available data

**Most implementations:** Return NaN for first $w-1$ values.

---

## Median Filtering in Signal Processing

**Median filter:** Moving median applied to remove noise.

**Advantage over linear filters:**

Preserves edges and sharp transitions.

**Application:**

- Image processing: Remove salt-and-pepper noise
- Audio processing: Remove clicks and pops
- Sensor data: Remove measurement spikes

**Example:** Camera sensor dead pixels. Median filter replaces with neighbor median.

---

## Properties of Median

**Location measure:** Estimates central tendency.

**Robust:** Not affected by extreme values.

**50th percentile:** Half of values below, half above.

**For symmetric distributions:** Median equals mean.

**For skewed distributions:** Median differs from mean.

---

## Smoothness and Discontinuities

**Moving average:** Produces smooth curve.

**Moving median:** Can produce piecewise constant segments.

**Example:** [1, 2, 3, 4, 5, 6, 7] with $w=3$

Medians: [2, 3, 4, 5, 6]

Smooth progression.

**Example with repeated values:** [1, 2, 2, 2, 2, 3, 4] with $w=3$

Medians: [2, 2, 2, 2, 3]

Flat segments where middle value persists.

---

## Temporal Smoothing for Trend Extraction

**Goal:** Separate trend from noise.

**Method:**

1. Apply moving median to remove outliers
2. Apply moving average to smooth further

**Two-stage approach:**

$$
\text{Trend}_t = \text{MA}(\text{MM}(y_t, w_1), w_2)
$$

**Advantage:** Robust to outliers (from median) and smooth (from average).

---

## Hybrid Median-Mean Filter

**Trimmed mean:** Remove extreme values, then average.

**Winsorized mean:** Replace extreme values with less extreme values, then average.

**Alpha-trimmed mean filter:**

1. Sort window values
2. Remove $\alpha$ proportion from each tail
3. Average remaining values

**Example:** 10% trimmed mean with $w=10$: Remove smallest and largest value, average middle 8.

**Compromise:** More robust than mean, smoother than median.

---

## Running Median for Streaming Data

**Streaming context:** Data arrives sequentially, cannot store all history.

**Sliding window:** Maintain only last $w$ values.

**Data structure:** Use two heaps (max-heap for lower half, min-heap for upper half).

**Efficiency:** $O(\log w)$ per update.

**Application:** Real-time anomaly detection, online signal processing.

---

## Median Absolute Deviation

**MAD:** Robust measure of variability.

$$
\text{MAD} = \text{median}(|y_i - \text{median}(y)|)
$$

**Moving MAD:**

$$
\text{MAD}_t = \text{median}(|y_{t-w+1} - \text{MM}_t|, ..., |y_t - \text{MM}_t|)
$$

**Use case:** Robust confidence bands around moving median.

**Outlier detection:**

$$
|y_t - \text{MM}_t| > k \cdot \text{MAD}_t
$$

Typical: $k \approx 3$ for anomaly flagging.

---

## Seasonality and Moving Median

**Seasonal adjustment:**

Use window size equal to seasonal period.

**Monthly data with yearly seasonality:** $w = 12$

**Centered moving median:**

$$
\text{CMM}_t = \text{median}(y_{t-6}, ..., y_t, ..., y_{t+6})
$$

**Effect:** Removes seasonal pattern, preserves trend.

**Note:** Requires future values (non-causal), suitable for historical analysis only.

---

## Quantile Extensions

**Moving percentiles:**

Generalization of moving median to other percentiles.

**25th percentile (Q1):**

$$
Q1_t = \text{P}_{25}(y_{t-w+1}, ..., y_t)
$$

**75th percentile (Q3):**

$$
Q3_t = \text{P}_{75}(y_{t-w+1}, ..., y_t)
$$

**Interquartile range:**

$$
\text{IQR}_t = Q3_t - Q1_t
$$

**Application:** Robust confidence bands, volatility estimation.

---

## Mode vs Median

**Mode:** Most frequent value in window.

**Median:** Middle value in sorted window.

**For continuous data:** Mode often undefined (no repeated values).

**For discrete data:** Mode can be useful.

**Example:** [1, 2, 2, 3, 2, 5] → Mode = 2, Median = 2

**Moving mode:** Less common than moving median, but useful for categorical time series.

---

## Weighted Median

**Standard median:** Equal weight to all observations.

**Weighted median:** Assign weights, find value where cumulative weight = 50%.

$$
\text{WM}_t = \arg\min_m \sum_{i=t-w+1}^{t} w_i |y_i - m|
$$

**Application:** Give more importance to recent observations.

**Example weights:** Exponentially decaying weights $w_i = \alpha^{t-i}$.

---

## Residual Analysis

**Detrended series:**

$$
r_t = y_t - \text{MM}_t
$$

**Analysis:**

- Plot residuals to check for patterns
- Residuals should be approximately symmetric around zero
- Large residuals indicate outliers or structural breaks

**Use case:** Identify anomalies after removing baseline trend.

---

## Comparison to Percentile Filters

**Minimum filter:** 0th percentile (moving minimum).

**Maximum filter:** 100th percentile (moving maximum).

**Median filter:** 50th percentile (moving median).

**Range filter:** Difference between max and min.

**Applications:**

- Minimum: Lower envelope
- Maximum: Upper envelope
- Range: Local volatility measure

---

## Non-Uniform Weighting

**Time-weighted median:**

Recent observations weighted more heavily.

**Implementation:**

Replicate recent values in window before computing median.

**Example:** Weight pattern [1, 2, 3] with $w=6$

Replicate: [value1, value2, value2, value3, value3, value3]

Compute median of replicated window.

**Effect:** Biases median toward recent values.

---

## Edge Preservation

**Key advantage:** Preserves sharp transitions.

**Example:** Step function $y_t = \begin{cases} 0 & t < 50 \\ 10 & t \geq 50 \end{cases}$

**Moving average:** Gradual transition (ramp) around $t=50$.

**Moving median:** Sharp transition maintained (step remains step).

**Application:** Financial data (price jumps), industrial processes (regime changes).

---

## Iterative Median Filtering

**Single pass:** Apply moving median once.

**Multiple passes:** Apply moving median repeatedly.

$$
y^{(k+1)}_t = \text{median}(y^{(k)}_{t-w+1}, ..., y^{(k)}_t)
$$

**Effect:** Progressively flattens data, removes finer structures.

**Convergence:** Eventually converges to root signal (minimal changes).

**Application:** Severe noise removal, extracting dominant patterns.

---

## Median for Categorical Data

**Ordinal categories:** Natural ordering exists.

**Example:** Ratings (1 star, 2 star, ..., 5 star).

**Moving median rating:** Median of last $w$ ratings.

**Advantage:** Robust to extreme positive or negative reviews.

**Nominal categories:** No natural ordering.

**Use mode instead:** Most frequent category in window.

---

## Computational Optimizations

**Sorted buffer approach:**

Maintain sorted list of window values.

**Insert/remove:** $O(w)$ to find position, $O(w)$ to shift elements.

**Median lookup:** $O(1)$ from middle of sorted list.

**Heap-based approach:**

Two heaps (max-heap for lower half, min-heap for upper half).

**Insert/remove:** $O(\log w)$

**Median lookup:** $O(1)$ from heap tops.

**Order statistic tree:**

Balanced BST augmented with subtree sizes.

**Insert/remove:** $O(\log w)$

**Median lookup:** $O(\log w)$

**Trade-offs depend on implementation details and typical window sizes.**

---

## Asymmetric Windows

**Standard:** Symmetric window around $t$.

**Causal (trailing):** Only past values.

$$
\text{MM}_t = \text{median}(y_{t-w+1}, ..., y_t)
$$

**Non-causal (centered):**

$$
\text{CMM}_t = \text{median}(y_{t-k}, ..., y_t, ..., y_{t+k})
$$

where $w = 2k+1$.

**Centered advantages:** No lag, better for historical smoothing.

**Causal advantages:** Suitable for real-time and forecasting.

---

## Variance and Standard Error

**Sample variance of median:** Difficult to compute analytically.

**Bootstrap approach:**

1. Resample window values with replacement
2. Compute median of each bootstrap sample
3. Estimate variance from bootstrap distribution

**Asymptotic variance:**

For large $n$, approximately:

$$
\text{Var}(\text{Median}) \approx \frac{1}{4nf(m)^2}
$$

where $f(m)$ is probability density at median $m$.

**Practical:** Variance higher than mean for normal data, lower for heavy-tailed data.

---

## Median Crossovers

**Similar to moving average crossovers:**

**Golden cross:** Fast median (small $w$) crosses above slow median (large $w$).

**Death cross:** Fast median crosses below slow median.

**Interpretation:** Trend change signal.

**Advantage over MA crossovers:** Less sensitive to outliers.

**Example strategy:** Long position when fast > slow, short when fast < slow.

---

## Seasonal Decomposition

**Trend extraction with moving median:**

$$
\text{Trend}_t = \text{MM}_t(w = s)
$$

where $s$ is seasonal period.

**Detrended:**

$$
D_t = y_t - \text{Trend}_t
$$

**Seasonal component:** Average $D_t$ for each season.

**Remainder:** $y_t - \text{Trend}_t - \text{Seasonal}_t$

**Robust STL decomposition:** Uses moving median instead of moving average for robustness.

---

## Multi-Scale Analysis

**Pyramid approach:**

Apply moving median at multiple window sizes.

**Small window:** Captures high-frequency variations.

**Medium window:** Captures mid-frequency trends.

**Large window:** Captures low-frequency baseline.

**Interpretation:** Decompose signal into components at different scales.

**Application:** Multi-resolution analysis, wavelet-like decomposition using medians.

---

## Practical Considerations

**Data type:** Works with any orderable data (numeric, ordinal categorical).

**Window size:** Odd preferred for unique median, even requires averaging.

**Computational cost:** Slower than moving average but faster than many robust alternatives.

**Outlier definition:** Depends on context. Median identifies values different from local neighborhood.

**Implementation:** Most libraries provide built-in functions (pandas, scipy, R).
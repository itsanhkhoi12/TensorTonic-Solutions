## What Is a Seasonal Average?

A seasonal average is the mean value for each season (period within a cycle) across multiple cycles. It captures recurring patterns that repeat at regular intervals.

$$
\bar{y}_s = \frac{1}{n} \sum_{i=1}^{n} y_{s + (i-1) \cdot m}
$$

where $s$ is the season index (1 to $m$), $m$ is the number of seasons per cycle, and $n$ is the number of cycles.

---

## The Formula

For a time series with seasonal period $m$, the seasonal average for season $s$ is:

$$
\bar{y}_s = \frac{1}{n} \sum_{j=1}^{n} y_{s,j}
$$

where $y_{s,j}$ is the value for season $s$ in cycle $j$, and $n$ is the total number of cycles.

**Example:** Monthly data (12 seasons).

Average for January: Mean of all January values across years.

$$
\bar{y}_{\text{Jan}} = \frac{y_{\text{Jan},2020} + y_{\text{Jan},2021} + y_{\text{Jan},2022}}{3}
$$

---

## Worked Example

**Monthly sales data over 3 years:**

Year 1: [120, 110, 130, 140, 150, 160, 170, 165, 155, 145, 135, 200]

Year 2: [125, 115, 135, 145, 155, 165, 175, 170, 160, 150, 140, 210]

Year 3: [130, 120, 140, 150, 160, 170, 180, 175, 165, 155, 145, 220]

**Seasonal averages:**

January (month 1): $\frac{120 + 125 + 130}{3} = 125$

February (month 2): $\frac{110 + 115 + 120}{3} = 115$

March (month 3): $\frac{130 + 135 + 140}{3} = 135$

...

December (month 12): $\frac{200 + 210 + 220}{3} = 210$

**Result:** [125, 115, 135, 145, 155, 165, 175, 170, 160, 150, 140, 210]

---

## Interpretation

**High seasonal average:** Season typically has high values.

**Low seasonal average:** Season typically has low values.

**Pattern:** Identifies which seasons are strong vs weak.

**Example:** Retail sales high in December (holiday shopping), low in January (post-holiday).

**Use case:** Budgeting, inventory planning, staffing.

---

## Seasonal Indices

**Normalize seasonal averages to overall mean:**

$$
\text{SI}_s = \frac{\bar{y}_s}{\bar{y}_{\text{overall}}}
$$

**Interpretation:**

- $\text{SI}_s = 1.2$: Season 20% above average
- $\text{SI}_s = 0.8$: Season 20% below average
- $\text{SI}_s = 1.0$: Season at average

**Example:**

Overall mean: 150

December average: 210

December index: $\frac{210}{150} = 1.4$ (40% above average)

---

## Additive vs Multiplicative Seasonality

**Additive model:**

$$
y_t = \text{Trend}_t + \text{Seasonal}_s + \text{Error}_t
$$

Seasonal component: $\text{Seasonal}_s = \bar{y}_s - \bar{y}_{\text{overall}}$

**Multiplicative model:**

$$
y_t = \text{Trend}_t \times \text{Seasonal}_s \times \text{Error}_t
$$

Seasonal component: $\text{Seasonal}_s = \frac{\bar{y}_s}{\bar{y}_{\text{overall}}}$

**Choose additive when:** Seasonal variation constant in magnitude.

**Choose multiplicative when:** Seasonal variation proportional to level (common in business data).

---

## Seasonal Decomposition

**Classical decomposition:**

1. Compute trend (moving average with period $m$)
2. Detrend: $y_t - \text{Trend}_t$ (additive) or $y_t / \text{Trend}_t$ (multiplicative)
3. Compute seasonal averages from detrended data
4. Center seasonal components (sum to zero or product to $m$)
5. Remainder: $\text{Remainder}_t = y_t - \text{Trend}_t - \text{Seasonal}_s$

**Result:** Separates trend, seasonality, and noise.

---

## Worked Decomposition Example

**Data:** [10, 15, 12, 16, 20, 18, 22, 30, 25, 28, 35, 32] (quarterly over 3 years)

**Step 1: Compute trend** (4-quarter moving average)

Centered MA: [NaN, NaN, 13.25, 15.75, 17.00, 19.00, 22.50, 23.75, 26.25, 28.75, 30.00, NaN]

**Step 2: Detrend** (multiplicative)

Ratios: [NaN, NaN, 0.906, 1.016, 1.176, 0.947, 0.978, 1.263, 0.952, 0.974, 1.167, NaN]

**Step 3: Seasonal averages**

Q1: 0.906, 0.978 → Average 0.942

Q2: 1.016, 1.263 → Average 1.140

Q3: 1.176, 0.952 → Average 1.064

Q4: 0.947, 0.974, 1.167 → Average 1.029

**Step 4: Normalize** (ensure product = 4)

Product = 1.173, adjust by dividing each by $(1.173/4)^{1/4} = 1.040$

**Final seasonal indices:** [0.906, 1.096, 1.023, 0.989]

---

## Forecasting with Seasonal Averages

**Naive seasonal forecast:**

$$
\hat{y}_{t+h} = \bar{y}_s
$$

where $s = ((t+h-1) \mod m) + 1$

**Example:** Forecast next January using average of past Januaries.

**Improved forecast (trend + seasonal):**

$$
\hat{y}_{t+h} = \text{Trend}_{t+h} + \bar{y}_s
$$

or

$$
\hat{y}_{t+h} = \text{Trend}_{t+h} \times \text{SI}_s
$$

**Trend extrapolation:** Linear, exponential, or model-based.

---

## Seasonal Adjustment

**Remove seasonality to reveal underlying trend:**

**Additive:**

$$
y_{t,\text{adj}} = y_t - \text{Seasonal}_s
$$

**Multiplicative:**

$$
y_{t,\text{adj}} = \frac{y_t}{\text{SI}_s}
$$

**Use case:** Compare values across seasons fairly, analyze trend without seasonal noise.

**Example:** Unemployment rate seasonally adjusted to remove predictable variations.

---

## X-12-ARIMA and X-13-ARIMA-SEATS

**Official methods used by government agencies:**

Advanced seasonal adjustment procedures.

**Features:**

- Handles trading day effects
- Holiday adjustments
- Outlier detection
- ARIMA modeling of irregular component

**Software:** U.S. Census Bureau provides implementation.

**Application:** Official economic statistics (GDP, CPI, unemployment).

---

## Centered Moving Average for Detrending

**Symmetric moving average:**

$$
\text{CMA}_t = \frac{1}{m} \sum_{i=-k}^{k} y_{t+i}
$$

where $m = 2k+1$ for odd $m$.

**For even $m$ (e.g., $m=12$):**

$$
\text{CMA}_t = \frac{1}{2m} \left(y_{t-m/2} + 2\sum_{i=-m/2+1}^{m/2-1} y_{t+i} + y_{t+m/2}\right)
$$

**Purpose:** Removes seasonality while preserving trend.

**Note:** Requires data on both sides (not causal).

---

## Seasonality Tests

**Visual inspection:**

Plot data and look for repeating patterns.

**Autocorrelation function (ACF):**

Significant peaks at lags $m, 2m, 3m, ...$ indicate seasonality.

**Seasonal subseries plot:**

Plot all values for each season. If means differ substantially, seasonality exists.

**Formal tests:**

- QS test (Maravall)
- OCSB test (Osborn-Chui-Smith-Birchenhall)
- Kruskal-Wallis test

---

## Dealing with Changing Seasonality

**Problem:** Seasonal pattern evolves over time.

**Example:** Air conditioning sales seasonality changes with climate trends.

**Solutions:**

**1. Moving seasonal averages:**

Compute seasonal averages using only recent cycles.

$$
\bar{y}_{s,t} = \frac{1}{k} \sum_{j=t-km+1}^{t} y_{s,j}
$$

Use last $k$ cycles instead of all history.

**2. STL decomposition:**

Seasonal-Trend decomposition using Loess.

Allows seasonal component to change gradually.

**3. State space models:**

Time-varying seasonal parameters.

---

## Seasonal Dummies in Regression

**Indicator variables for each season:**

$$
y_t = \beta_0 + \sum_{s=1}^{m-1} \beta_s D_{s,t} + \epsilon_t
$$

where $D_{s,t} = 1$ if observation $t$ is in season $s$, 0 otherwise.

**Interpretation:** $\beta_s$ is difference between season $s$ and reference season.

**Advantage:** Incorporate seasonality in regression framework.

**Example:** Quarterly data with Q4 as reference.

Q1, Q2, Q3 dummy variables capture seasonal effects.

---

## Fourier Seasonality

**Represent seasonality with sine and cosine terms:**

$$
y_t = \beta_0 + \sum_{k=1}^{K} \left[\alpha_k \sin\left(\frac{2\pi k t}{m}\right) + \gamma_k \cos\left(\frac{2\pi k t}{m}\right)\right] + \epsilon_t
$$

**Advantage:** Smooth seasonal pattern, parsimonious (fewer parameters than dummies).

**Disadvantage:** Assumes smooth periodic pattern.

**Use when:** Long seasonal period (e.g., $m=52$ for weekly data).

---

## Calendar Adjustments

**Trading day effects:**

Number of weekdays in month varies.

**Solution:** Adjust for trading days.

$$
y_{t,\text{adj}} = y_t \times \frac{\text{Avg days}}{\text{Actual days}}
$$

**Holiday effects:**

Easter, Thanksgiving, Chinese New Year dates vary.

**Approach:** Include holiday dummy variables or use specialized methods (X-13).

**Length-of-month adjustment:**

February has fewer days.

**Per-day rate:** $\frac{y_t}{\text{Days in month}_t}$

---

## Seasonal Subseries Plot

**Method:**

Plot all observations for each season in separate panels.

**Example:** Monthly data.

12 panels, each showing all January values, all February values, etc.

**Horizontal line:** Seasonal average for that season.

**Interpretation:**

- Variation within season shows volatility
- Trend within season shows evolution
- Difference across panels shows seasonal pattern

---

## Holt-Winters Seasonal Smoothing

**Triple exponential smoothing:**

**Level:** $\ell_t = \alpha(y_t - s_{t-m}) + (1-\alpha)(\ell_{t-1} + b_{t-1})$

**Trend:** $b_t = \beta(\ell_t - \ell_{t-1}) + (1-\beta)b_{t-1}$

**Seasonal:** $s_t = \gamma(y_t - \ell_t) + (1-\gamma)s_{t-m}$

**Forecast:**

$$
\hat{y}_{t+h} = \ell_t + hb_t + s_{t+h-m\lfloor (h-1)/m \rfloor}
$$

**Advantage:** Adaptive to changing patterns, all components updated each period.

---

## Seasonal ARIMA Models

**SARIMA(p,d,q)(P,D,Q)$_m$:**

Combines non-seasonal and seasonal components.

**Non-seasonal:** AR($p$), Differences($d$), MA($q$)

**Seasonal:** AR($P$) at lag $m$, Differences($D$) at lag $m$, MA($Q$) at lag $m$

**Example:** SARIMA(1,1,1)(1,1,1)$_{12}$ for monthly data.

**Seasonal differencing:**

$$
\nabla_m y_t = y_t - y_{t-m}
$$

Removes seasonal pattern.

---

## Periodogram and Spectral Analysis

**Periodogram:**

$$
I(\omega) = \frac{1}{T} \left|\sum_{t=1}^{T} y_t e^{-i\omega t}\right|^2
$$

**Peaks at frequencies:** Indicate periodicity.

**Seasonal frequency:** $\omega = \frac{2\pi}{m}$

**Example:** Monthly data ($m=12$).

Peak at $\omega = \frac{\pi}{6}$ indicates yearly seasonality.

**Use:** Detect multiple seasonal patterns (weekly and yearly).

---

## Multiple Seasonality

**Complex patterns:** Multiple seasonal cycles.

**Example:** Hourly electricity demand.

- Daily pattern (24 hours)
- Weekly pattern (7 days)
- Yearly pattern (365 days)

**TBATS model:**

Trigonometric, Box-Cox, ARMA, Trend, Seasonal.

Handles multiple seasonalities with different periods.

**STR (Seasonal-Trend decomposition with Regression):**

Decomposes series with multiple seasonal patterns.

---

## Seasonal Breaks

**Structural changes in seasonal pattern:**

Pattern shifts at specific point.

**Example:** Retail sales seasonality changes after major policy change.

**Detection:** CUSUM tests, Chow tests on seasonal dummies.

**Modeling:** Allow seasonal parameters to differ before/after breakpoint.

**Dummy variables:**

$$
D_{s,t} \times \mathbb{1}_{t > \tau}
$$

where $\tau$ is breakpoint.

---

## Interpolation of Missing Seasonal Values

**Missing observations in specific seasons:**

**Approach 1:** Use seasonal average.

$$
\hat{y}_t = \bar{y}_s
$$

**Approach 2:** Interpolate using seasonal pattern.

$$
\hat{y}_t = \text{Trend}_t + \bar{y}_s
$$

**Approach 3:** Kalman filter with seasonal state space model.

**Choice depends on:** Amount of missing data, pattern complexity.

---

## Seasonal Adjustment Quality Metrics

**F-tests:** Compare variance explained by seasonal component to residual variance.

**M-statistics:** Suite of diagnostics for seasonal adjustment quality.

**Spectral diagnostics:** Check if seasonal frequencies removed from adjusted series.

**Revision history:** Assess stability of adjustments over time.

**Residual seasonality tests:** Verify no remaining seasonal pattern after adjustment.

---

## Business Applications

**Retail:** Plan inventory based on seasonal demand patterns.

**Tourism:** Staff hotels and attractions according to seasonal peaks.

**Agriculture:** Predict harvest yields accounting for planting seasons.

**Energy:** Forecast electricity/gas demand with seasonal temperature effects.

**Finance:** Adjust earnings for seasonal patterns (Q4 typically strongest).

**HR:** Anticipate seasonal hiring needs (retail holiday season).

---

## Seasonal Averages for Outlier Detection

**Comparison to seasonal norm:**

$$
\text{Deviation}_t = y_t - \bar{y}_s
$$

**Flag outliers:** $|\text{Deviation}_t| > k \sigma_s$

where $\sigma_s$ is standard deviation for season $s$.

**Example:** Unusually high sales in February (typically low season) may indicate special event.

**Application:** Quality control, anomaly detection.

---

## Visualization Techniques

**Seasonal plot:**

Overlay multiple years, each season on x-axis.

**Polar (circular) plot:**

Angle represents season, radius represents value.

**Heatmap:**

Rows = years, columns = seasons, color = value.

**Box plots by season:**

Distribution of values for each season.

**All aid in:** Identifying seasonal patterns visually.

---

## Challenges with Short Time Series

**Few cycles:** Seasonal averages unreliable.

**Rule of thumb:** Need at least 2-3 full cycles for stable seasonal estimates.

**Solutions:**

1. Use external seasonal indices (industry benchmarks)
2. Pool data across similar entities
3. Use domain knowledge to set seasonal pattern
4. Employ Bayesian methods with informative priors

**Example:** New product with only 1 year of data. Use category-level seasonal pattern.

---

## Comparison to Moving Averages

**Seasonal average:** Average across cycles for same season.

**Moving average:** Average across consecutive observations.

**Purpose:**

- Seasonal average: Extract seasonal pattern
- Moving average: Smooth noise, extract trend

**Complementary:** Often used together in decomposition.

**Example:** Detrend with MA, compute seasonal averages from detrended series.

---

## Seasonal Co-Movement

**Cross-sectional seasonality:**

Multiple series share seasonal pattern.

**Example:** All retail categories peak in December.

**Factor models:** Extract common seasonal factors.

**Application:** Forecasting related series, portfolio diversification.

**Correlation by season:** Correlation may vary across seasons.
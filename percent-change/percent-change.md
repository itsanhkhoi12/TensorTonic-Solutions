## What Is Percent Change?

Percent change measures the relative change between consecutive observations in a time series, expressed as a percentage. It shows how much a value has increased or decreased relative to its previous value.

$$
\text{PC}_t = \frac{y_t - y_{t-1}}{y_{t-1}} \times 100\%
$$

where $y_t$ is the current value and $y_{t-1}$ is the previous value.

---

## The Formula

For a time series $y_1, y_2, ..., y_T$:

$$
\text{PC}_t = \frac{y_t - y_{t-1}}{y_{t-1}} \times 100\%
$$

**Without percentage:** Drop the 100 factor to get decimal form.

$$
r_t = \frac{y_t - y_{t-1}}{y_{t-1}}
$$

**Alternative form:**

$$
\text{PC}_t = \left(\frac{y_t}{y_{t-1}} - 1\right) \times 100\%
$$

---

## Worked Example

**Time series:** [100, 105, 102, 110, 108]

**Period 2:**

$$
\text{PC}_2 = \frac{105 - 100}{100} \times 100\% = \frac{5}{100} \times 100\% = 5\%
$$

**Period 3:**

$$
\text{PC}_3 = \frac{102 - 105}{105} \times 100\% = \frac{-3}{105} \times 100\% = -2.857\%
$$

**Period 4:**

$$
\text{PC}_4 = \frac{110 - 102}{102} \times 100\% = \frac{8}{102} \times 100\% = 7.843\%
$$

**Period 5:**

$$
\text{PC}_5 = \frac{108 - 110}{110} \times 100\% = \frac{-2}{110} \times 100\% = -1.818\%
$$

**Result:** [NaN, 5%, -2.857%, 7.843%, -1.818%]

---

## Interpretation

**Positive percent change:** Value increased.

**Example:** +5% means value grew by 5% from previous period.

**Negative percent change:** Value decreased.

**Example:** -3% means value declined by 3% from previous period.

**Zero percent change:** No change.

**Magnitude:** Larger absolute value indicates larger relative change.

---

## Comparison to Absolute Change

**Absolute change:**

$$
\Delta y_t = y_t - y_{t-1}
$$

**Percent change:**

$$
\text{PC}_t = \frac{\Delta y_t}{y_{t-1}} \times 100\%
$$

**Example:** Stock price increases from $10 to $11 vs $100 to $101.

Absolute change: Both +$1

Percent change: +10% vs +1%

**Percent change provides scale-independent comparison.**

---

## Lag-k Percent Change

**One-period lag (standard):**

$$
\text{PC}_t = \frac{y_t - y_{t-1}}{y_{t-1}} \times 100\%
$$

**k-period lag:**

$$
\text{PC}_t(k) = \frac{y_t - y_{t-k}}{y_{t-k}} \times 100\%
$$

**Example applications:**

- $k=1$: Daily change
- $k=5$: Weekly change (for daily data)
- $k=12$: Year-over-year change (for monthly data)

---

## Year-Over-Year Example

**Monthly sales data:** [100, 105, 110, 95, 102, 108, 115, 120, 112, 118, 125, 130]

**Year-over-year percent change ($k=12$):**

Not defined until month 13.

**Month 13 (year 2, month 1):** Sales = 110

$$
\text{YoY} = \frac{110 - 100}{100} \times 100\% = 10\%
$$

**Interpretation:** Sales in month 13 are 10% higher than same month previous year.

---

## Compounding Effects

**Percent changes do not add:**

If value increases 10% then decreases 10%, final value is NOT original value.

**Example:**

Start: $100

After +10%: $100 \times 1.10 = $110

After -10%: $110 \times 0.90 = $99

**Lost 1% overall, not 0%.**

**Compounding formula:**

$$
y_t = y_0 \prod_{i=1}^{t} (1 + r_i)
$$

---

## Log Returns Alternative

**Problem:** Percent changes are asymmetric.

+50% followed by -50% does not return to original value.

**Log returns:**

$$
\ell_t = \ln\left(\frac{y_t}{y_{t-1}}\right) = \ln(1 + r_t)
$$

**Advantage:** Log returns are additive.

$$
\sum_{i=1}^{t} \ell_i = \ln\left(\frac{y_t}{y_0}\right)
$$

**Approximation:** For small $r_t$, $\ell_t \approx r_t$

**Finance:** Log returns preferred for modeling and aggregation.

---

## Stationarity

**Non-stationary series:** Mean and variance change over time (e.g., stock prices).

**Percent change series:** Often stationary.

**Transformation:** Converting levels to percent changes can induce stationarity.

**Application:** Many time series models (ARIMA) require stationary data. Percent changes often satisfy this.

**Example:** Stock prices have unit root (non-stationary). Returns are stationary.

---

## Percent Change and Volatility

**Volatility:** Measured as standard deviation of percent changes.

$$
\sigma = \sqrt{\frac{1}{T-1} \sum_{t=2}^{T} (r_t - \bar{r})^2}
$$

**High volatility:** Large swings in percent changes.

**Low volatility:** Small, stable percent changes.

**Application:** Risk assessment in finance. Higher volatility means higher risk.

---

## Handling Zero and Negative Values

**Division by zero:**

If $y_{t-1} = 0$, percent change undefined.

**Negative values:**

Percent change still defined but interpretation complex.

**Example:** Change from -10 to -5.

$$
\text{PC} = \frac{-5 - (-10)}{-10} \times 100\% = \frac{5}{-10} \times 100\% = -50\%
$$

**Confusing:** Value improved (less negative) but percent change is negative.

**Solution:** Use absolute change for series with zero or negative values.

---

## Seasonality Detection

**Seasonal patterns visible in percent changes:**

Compare percent changes at same seasonal period.

**Example:** Monthly retail sales.

December often shows large positive percent change (holiday shopping).

January often shows large negative percent change (post-holiday).

**Analysis:** Consistent patterns in percent changes indicate seasonality.

---

## Moving Average of Percent Changes

**Smooth percent change series:**

$$
\text{MA}(\text{PC}_t) = \frac{1}{w} \sum_{i=0}^{w-1} \text{PC}_{t-i}
$$

**Interpretation:** Average rate of change over recent periods.

**Application:** Identify sustained trends vs temporary spikes.

**Example:** Average percent change over last 12 months indicates overall growth rate.

---

## Cumulative Percent Change

**Cumulative effect of percent changes:**

$$
y_t = y_0 \prod_{i=1}^{t} (1 + r_i)
$$

**Cumulative percent change:**

$$
R_{\text{cum}} = \frac{y_t - y_0}{y_0} \times 100\% = \left(\prod_{i=1}^{t} (1 + r_i) - 1\right) \times 100\%
$$

**Example:** Daily returns of +2%, -1%, +3%

$$
R_{\text{cum}} = (1.02 \times 0.99 \times 1.03 - 1) \times 100\% = (1.04 - 1) \times 100\% = 4\%
$$

---

## Growth Rate Interpretation

**Percent change as growth rate:**

$$
g_t = \frac{y_t - y_{t-1}}{y_{t-1}}
$$

**Continuous compounding approximation:**

$$
y_t \approx y_{t-1} e^{g_t}
$$

**Long-term growth:**

If growth rate is constant $g$:

$$
y_t = y_0 (1 + g)^t
$$

**Doubling time:**

$$
t_{\text{double}} \approx \frac{\ln(2)}{\ln(1+g)} \approx \frac{0.693}{g}
$$

**Example:** 7% annual growth doubles in approximately 10 years.

---

## Outlier Detection

**Percent change highlights anomalies:**

Sudden large percent changes indicate unusual events.

**Threshold method:**

Flag $|\text{PC}_t| > k \sigma$ where $\sigma$ is standard deviation of percent changes and $k=3$ typically.

**Example:** Stock price jumps 20% in one day (earnings surprise, merger announcement).

**Application:** Anomaly detection, event study analysis.

---

## Forecasting with Percent Changes

**Naive forecast:**

$$
\hat{\text{PC}}_{t+1} = \bar{\text{PC}}
$$

Use historical average percent change.

**Level forecast:**

$$
\hat{y}_{t+1} = y_t (1 + \hat{\text{PC}}_{t+1})
$$

**Multi-step:**

$$
\hat{y}_{t+h} = y_t (1 + \hat{\text{PC}})^h
$$

Assumes constant growth rate.

**Better models:** ARIMA on percent changes, exponential smoothing on levels.

---

## Symmetric Percent Change

**Standard percent change asymmetry:**

Change from 100 to 150: +50%

Change from 150 to 100: -33.3%

**Different magnitudes for same absolute change.**

**Symmetric percent change:**

$$
\text{SPC}_t = \frac{y_t - y_{t-1}}{(y_t + y_{t-1})/2} \times 100\%
$$

**Denominator:** Average of current and previous values.

**Example:**

100 to 150: $\frac{50}{125} \times 100\% = 40\%$

150 to 100: $\frac{-50}{125} \times 100\% = -40\%$

**Now symmetric in magnitude.**

---

## Annualized Percent Change

**Convert to annual rate:**

$$
r_{\text{annual}} = \left(1 + r_{\text{period}}\right)^{n} - 1
$$

where $n$ is number of periods per year.

**Example:** Monthly return of 1%

$$
r_{\text{annual}} = (1.01)^{12} - 1 = 1.1268 - 1 = 0.1268 = 12.68\%
$$

**Interpretation:** If 1% monthly growth continues, annual growth is 12.68%.

---

## Percent Change in Indexes

**Index construction:**

Set base period to 100.

$$
I_t = \frac{y_t}{y_0} \times 100
$$

**Percent change in index:**

$$
\text{PC}_t = \frac{I_t - I_{t-1}}{I_{t-1}} \times 100\%
$$

**Same as percent change in original series.**

**Advantage of indexing:** Easy comparison across multiple series with different units.

---

## Percent Change and Correlation

**Correlation of levels vs returns:**

Levels may be spuriously correlated due to trends.

**Returns often have different correlation structure.**

**Example:** Two stock prices both trending upward (high correlation in levels).

Daily returns may be uncorrelated (price movements independent).

**Analysis:** Compute correlation of percent changes to assess true relationship.

---

## Differencing vs Percent Change

**First difference:**

$$
\Delta y_t = y_t - y_{t-1}
$$

**Percent change:**

$$
r_t = \frac{\Delta y_t}{y_{t-1}}
$$

**Differencing:** Additive model (absolute changes).

**Percent change:** Multiplicative model (relative changes).

**Use differencing when:** Variance is constant in levels.

**Use percent change when:** Variance proportional to level (heteroscedasticity).

---

## Percentage Point vs Percent Change

**Percentage point:** Absolute difference in percentages.

**Example:** Interest rate changes from 5% to 7%.

Change is 2 percentage points.

**Percent change:** Relative change.

$$
\frac{7 - 5}{5} \times 100\% = 40\% \text{ increase}
$$

**Critical distinction:** Often confused in media and reports.

---

## Reversion to Base Value

**Asymmetric recovery:**

Decrease of 50% requires 100% increase to return to original.

**Example:**

Start: 100

After -50%: 50

To return to 100: $\frac{100-50}{50} \times 100\% = 100\%$ increase needed.

**Implication:** Losses are harder to recover in percentage terms.

---

## Volatility Clustering

**Financial returns:** Large percent changes tend to cluster.

**High volatility period:** Consecutive large percent changes.

**Low volatility period:** Consecutive small percent changes.

**ARCH/GARCH models:** Capture volatility clustering.

$$
\sigma_t^2 = \alpha_0 + \alpha_1 r_{t-1}^2 + \beta \sigma_{t-1}^2
$$

**Application:** Risk management, option pricing.

---

## Real vs Nominal Percent Change

**Nominal percent change:**

$$
r_{\text{nominal}} = \frac{P_t - P_{t-1}}{P_{t-1}}
$$

**Inflation adjustment:**

$$
r_{\text{real}} = \frac{1 + r_{\text{nominal}}}{1 + \pi} - 1
$$

where $\pi$ is inflation rate.

**Approximation:**

$$
r_{\text{real}} \approx r_{\text{nominal}} - \pi
$$

**Example:** Nominal return 10%, inflation 3%.

Real return $\approx 7\%$.

**Interpretation:** Purchasing power increase.

---

## Geometric vs Arithmetic Mean

**Arithmetic mean of percent changes:**

$$
\bar{r}_a = \frac{1}{T} \sum_{t=1}^{T} r_t
$$

**Geometric mean:**

$$
\bar{r}_g = \left(\prod_{t=1}^{T} (1 + r_t)\right)^{1/T} - 1
$$

**Relationship:** $\bar{r}_g < \bar{r}_a$ unless all $r_t$ equal.

**Use geometric for:** Compounding returns over time.

**Use arithmetic for:** Average single-period return.

---

## Percent Change Distribution

**Empirical observation:**

Financial returns (percent changes) approximately normal with fat tails.

**Stylized facts:**

- Mean close to zero
- Positive or negative skewness possible
- Excess kurtosis (leptokurtic)

**Implications:**

Standard normal assumption underestimates extreme events.

Use Student-t or other heavy-tailed distributions for better fit.

---

## Time Aggregation

**Daily to monthly percent change:**

Cannot simply average daily percent changes.

**Correct method:**

$$
r_{\text{monthly}} = \prod_{d=1}^{D} (1 + r_d) - 1
$$

where $D$ is number of days in month.

**Example:** Daily returns of 1%, 2%, -1%.

$$
r = 1.01 \times 1.02 \times 0.99 - 1 = 1.0198 - 1 = 1.98\%
$$

**Not** $(1 + 2 - 1)/3 = 0.67\%$.

---

## Confidence Intervals

**For normal returns:**

$$
\text{CI} = \bar{r} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{T}}
$$

**Example:** Average daily return 0.05%, standard deviation 1.5%, 100 observations.

95% CI: $0.05\% \pm 1.96 \times \frac{1.5\%}{10} = 0.05\% \pm 0.294\%$

**Interpretation:** Plausible range for true mean return.

---

## Signal-to-Noise in Percent Changes

**Efficient market hypothesis:**

Asset returns are unpredictable (high noise, low signal).

**Autocorrelation test:**

If $\text{Corr}(r_t, r_{t-1}) \approx 0$, returns are unpredictable.

**Momentum vs mean reversion:**

Positive autocorrelation: Momentum (trends persist)

Negative autocorrelation: Mean reversion (reversals)

**Empirical:** Stock returns show weak autocorrelation, volatility shows strong autocorrelation.
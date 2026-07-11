## What Is a One-Sample t-Test?

The one-sample t-test determines whether the mean of a sample is significantly different from a known or hypothesized population mean.

It answers the question: "Is the observed sample mean different from what we would expect under the null hypothesis?"

Developed by William Sealy Gosset under the pseudonym "Student" in 1908.

---

## When to Use the One-Sample t-Test

Use this test when:

- You have a single sample of continuous data
- You want to compare the sample mean to a known value
- The population standard deviation is unknown
- Data is approximately normally distributed (or sample is large)

**Examples:**
- Is the average height of students different from the national average?
- Is the mean response time different from 100ms?
- Is the average test score different from 75?

---

## The Hypotheses

**Null hypothesis ($H_0$):**

The population mean equals the hypothesized value.

$$
H_0: \mu = \mu_0
$$

**Alternative hypothesis ($H_1$):**

**Two-tailed:** $H_1: \mu \neq \mu_0$ (mean is different)

**Left-tailed:** $H_1: \mu < \mu_0$ (mean is less than)

**Right-tailed:** $H_1: \mu > \mu_0$ (mean is greater than)

---

## The t-Statistic

The test statistic measures how many standard errors the sample mean is from the hypothesized mean:

$$
t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}
$$

where:
- $\bar{x}$ = sample mean
- $\mu_0$ = hypothesized population mean
- $s$ = sample standard deviation
- $n$ = sample size
- $s / \sqrt{n}$ = standard error of the mean

---

## Understanding the t-Statistic

**Large $|t|$:** Sample mean is far from $\mu_0$ in terms of standard errors. Evidence against $H_0$.

**Small $|t|$:** Sample mean is close to $\mu_0$. Consistent with $H_0$.

**Sign of $t$:**
- Positive: $\bar{x} > \mu_0$
- Negative: $\bar{x} < \mu_0$

---

## The t-Distribution

Under $H_0$, the t-statistic follows a **t-distribution** with $n-1$ degrees of freedom.

**Properties of t-distribution:**
- Symmetric around 0
- Bell-shaped like Normal
- Heavier tails than Normal (more probability in extremes)
- Approaches Normal as $df \to \infty$

**Why heavier tails?**

We estimate $\sigma$ with $s$, introducing additional uncertainty. Heavier tails account for this.

---

## Degrees of Freedom

$$
df = n - 1
$$

We lose one degree of freedom because we estimate the mean from the data.

**Effect of df:**
- Small df: Wider, heavier-tailed distribution
- Large df: Approaches standard Normal
- df $\geq 30$: t-distribution is very close to Normal

---

## Step-by-Step Procedure

**Step 1:** State hypotheses ($H_0$ and $H_1$)

**Step 2:** Choose significance level $\alpha$ (commonly 0.05)

**Step 3:** Calculate sample mean $\bar{x}$ and standard deviation $s$

**Step 4:** Compute the t-statistic

**Step 5:** Determine p-value or critical value

**Step 6:** Make decision:
- If p-value $< \alpha$, reject $H_0$
- If $|t| > t_{critical}$, reject $H_0$

---

## Worked Example

**Research question:** A company claims batteries last 500 hours on average. A sample of 25 batteries has mean life 490 hours with standard deviation 30 hours. Is the mean different from 500?

**Step 1: Hypotheses**

$H_0: \mu = 500$

$H_1: \mu \neq 500$ (two-tailed)

**Step 2: Significance level**

$\alpha = 0.05$

---

**Step 3: Calculate t-statistic**

$\bar{x} = 490$, $\mu_0 = 500$, $s = 30$, $n = 25$

$$
t = \frac{490 - 500}{30 / \sqrt{25}} = \frac{-10}{30/5} = \frac{-10}{6} = -1.67
$$

**Step 4: Degrees of freedom**

$df = 25 - 1 = 24$

**Step 5: Critical value and p-value**

For two-tailed test at $\alpha = 0.05$ with $df = 24$:

$t_{critical} = \pm 2.064$

p-value $\approx 0.108$ (from t-distribution table or calculator)

**Step 6: Decision**

$|t| = 1.67 < 2.064$ and p-value = 0.108 > 0.05

**Fail to reject $H_0$.** Insufficient evidence that mean battery life differs from 500 hours.

---

## Critical Values

Common critical values for two-tailed tests at $\alpha = 0.05$:

- $df = 10$: $t_{crit} = \pm 2.228$
- $df = 20$: $t_{crit} = \pm 2.086$
- $df = 30$: $t_{crit} = \pm 2.042$
- $df = 60$: $t_{crit} = \pm 2.000$
- $df = \infty$: $t_{crit} = \pm 1.96$ (Normal)

For one-tailed tests, use $\alpha$ instead of $\alpha/2$.

---

## P-Value Interpretation

The p-value is the probability of observing a t-statistic at least as extreme as the calculated value, assuming $H_0$ is true.

**Two-tailed test:**
$$
\text{p-value} = 2 \times P(T > |t|)
$$

**One-tailed test (right):**
$$
\text{p-value} = P(T > t)
$$

**One-tailed test (left):**
$$
\text{p-value} = P(T < t)
$$

---

## Confidence Interval Approach

A $(1-\alpha) \times 100\%$ confidence interval for $\mu$:

$$
\bar{x} \pm t_{\alpha/2, n-1} \times \frac{s}{\sqrt{n}}
$$

If $\mu_0$ is NOT in the interval, reject $H_0$ at level $\alpha$.

**Example:** For the battery data:

$$
CI = 490 \pm 2.064 \times \frac{30}{5} = 490 \pm 12.38 = [477.62, 502.38]
$$

Since 500 is IN the interval, we fail to reject $H_0$ (consistent with our earlier conclusion).

---

## Assumptions

**1. Random sampling**

Observations are randomly selected from the population.

**2. Independence**

Observations are independent of each other.

**3. Normality**

The population is normally distributed, OR the sample size is large ($n \geq 30$, by Central Limit Theorem).

**4. No extreme outliers**

Outliers can distort the mean and inflate standard deviation.

---

## Checking Normality

**Visual methods:**
- Histogram: Should be roughly bell-shaped
- Q-Q plot: Points should follow the diagonal line

**Formal tests:**
- Shapiro-Wilk test
- Kolmogorov-Smirnov test

**Rule of thumb:**
- $n \geq 30$: CLT applies, normality less critical
- $n < 30$: Check normality carefully

---

## Effect Size: Cohen's d

The t-statistic depends on sample size. For effect size, use Cohen's d:

$$
d = \frac{\bar{x} - \mu_0}{s}
$$

**Interpretation:**
- $|d| = 0.2$: Small effect
- $|d| = 0.5$: Medium effect
- $|d| = 0.8$: Large effect

**Example:** $d = (490 - 500)/30 = -0.33$ (small-to-medium effect)

---

## Power of the Test

**Power** = probability of correctly rejecting $H_0$ when $H_1$ is true.

$$
\text{Power} = 1 - \beta
$$

where $\beta$ is the probability of Type II error (false negative).

**Factors affecting power:**
- Larger sample size $\to$ higher power
- Larger effect size $\to$ higher power
- Larger $\alpha$ $\to$ higher power
- Smaller variance $\to$ higher power

---

## Sample Size Determination

To achieve desired power for detecting effect size $d$:

$$
n \approx \frac{2(z_{\alpha/2} + z_{\beta})^2}{d^2}
$$

For 80% power ($z_{\beta} = 0.84$) at $\alpha = 0.05$ ($z_{\alpha/2} = 1.96$):

$$
n \approx \frac{2(1.96 + 0.84)^2}{d^2} = \frac{15.68}{d^2}
$$

For $d = 0.5$: $n \approx 63$

---

## One-Sample t-Test vs Z-Test

**Z-test:**
- Population standard deviation $\sigma$ is known
- Uses standard Normal distribution
- Rarely appropriate in practice

**t-test:**
- Population standard deviation is unknown
- Uses t-distribution
- Almost always the appropriate choice

When $n$ is large, both give nearly identical results.

---

## Relationship to Confidence Intervals

There is a direct correspondence:

- Reject $H_0: \mu = \mu_0$ at level $\alpha$ $\Leftrightarrow$ $\mu_0$ is not in the $(1-\alpha)$ CI

This provides two equivalent ways to test hypotheses.

---

## Common Mistakes

**1. Using z-test when $\sigma$ is unknown**

Always use t-test when estimating $\sigma$ from data.

**2. Ignoring assumptions**

Non-normality with small samples invalidates the test.

**3. Confusing statistical and practical significance**

A small difference can be statistically significant with large $n$.

**4. Multiple comparisons**

Testing many hypotheses inflates Type I error rate.

---

## Alternatives When Assumptions Fail

**Non-normal data with small samples:**
- Wilcoxon signed-rank test (non-parametric)
- Sign test

**Outliers present:**
- Trim outliers or use robust methods
- Consider median-based tests

**Very small samples ($n < 10$):**
- Consider exact tests or bootstrap methods

---

## Applications in Machine Learning

**A/B testing:**
- Compare metric to baseline
- Test if new feature improves performance

**Model evaluation:**
- Is mean error significantly different from zero?
- Is model prediction bias significant?

**Feature analysis:**
- Test if feature mean differs between implementation expectations
## What Is a Poisson Distribution?

The Poisson distribution models the **number of events** occurring in a fixed interval of time or space, when events happen independently at a constant average rate.

It answers questions like: "How many customers will arrive in the next hour?" or "How many defects will be found in a batch?"

Named after French mathematician Siméon Denis Poisson.

---

## When to Use Poisson

The Poisson distribution is appropriate when:

**1. Events occur independently**

One event does not affect the probability of another.

**2. Events occur at a constant average rate**

The rate $\lambda$ is the same throughout the interval.

**3. Two events cannot occur at exactly the same instant**

Events are countable and discrete.

**4. The probability of an event in a small interval is proportional to the interval size**

Doubling the time doubles the expected count.

---

## Real-World Examples

Many phenomena follow a Poisson distribution:

- Number of emails received per hour
- Number of cars passing a checkpoint per minute
- Number of calls to a call center per hour
- Number of typos per page
- Number of accidents at an intersection per month
- Number of mutations in a DNA strand
- Number of photons hitting a detector per second
- Number of website visitors per minute

---

## The Parameter $\lambda$

The Poisson distribution has a single parameter:

$$
\lambda = \text{average rate (expected number of events)}
$$

**Constraints:**
- $\lambda > 0$

$\lambda$ represents both the mean and the variance of the distribution.

---

## The Probability Mass Function (PMF)

The probability of observing exactly $k$ events is:

$$
P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}
$$

where $k \in \{0, 1, 2, 3, ...\}$.

**Components explained:**
- $\lambda^k$: Rate raised to power of count
- $e^{-\lambda}$: Normalization factor ensuring probabilities sum to 1
- $k!$: Factorial accounting for event ordering

---

## Verifying the PMF Sums to 1

$$
\sum_{k=0}^{\infty} P(X = k) = \sum_{k=0}^{\infty} \frac{\lambda^k e^{-\lambda}}{k!} = e^{-\lambda} \sum_{k=0}^{\infty} \frac{\lambda^k}{k!}
$$

The Taylor series for $e^x$ is $\sum_{k=0}^{\infty} \frac{x^k}{k!}$, so:

$$
= e^{-\lambda} \cdot e^{\lambda} = e^0 = 1 \checkmark
$$

---

## Worked Example: Call Center

**Setup:** A call center receives an average of 5 calls per hour ($\lambda = 5$). What is the probability of receiving exactly 3 calls in the next hour?

**Solution:**

$$
P(X = 3) = \frac{5^3 e^{-5}}{3!} = \frac{125 \cdot e^{-5}}{6}
$$

$$
= \frac{125 \cdot 0.00674}{6} = \frac{0.8425}{6} = 0.1404
$$

There is about a 14% chance of exactly 3 calls.

---

## Computing Multiple PMF Values

**Setup:** $\lambda = 4$

$P(X = 0) = \frac{4^0 e^{-4}}{0!} = \frac{1 \cdot 0.0183}{1} = 0.0183$

$P(X = 1) = \frac{4^1 e^{-4}}{1!} = \frac{4 \cdot 0.0183}{1} = 0.0733$

$P(X = 2) = \frac{4^2 e^{-4}}{2!} = \frac{16 \cdot 0.0183}{2} = 0.1465$

$P(X = 3) = \frac{4^3 e^{-4}}{3!} = \frac{64 \cdot 0.0183}{6} = 0.1954$

$P(X = 4) = \frac{4^4 e^{-4}}{4!} = \frac{256 \cdot 0.0183}{24} = 0.1954$

$P(X = 5) = \frac{4^5 e^{-4}}{5!} = \frac{1024 \cdot 0.0183}{120} = 0.1563$

---

## The Cumulative Distribution Function (CDF)

The CDF gives the probability of observing at most $k$ events:

$$
F(k) = P(X \leq k) = \sum_{i=0}^{k} \frac{\lambda^i e^{-\lambda}}{i!}
$$

**Properties:**
- $F(k)$ increases as $k$ increases
- $\lim_{k \to \infty} F(k) = 1$

There is no closed-form expression; it must be computed as a sum or using special functions (incomplete gamma function).

---

## CDF Example

**Setup:** $\lambda = 4$. Find $P(X \leq 3)$.

$$
F(3) = P(X \leq 3) = P(X=0) + P(X=1) + P(X=2) + P(X=3)
$$

$$
= 0.0183 + 0.0733 + 0.1465 + 0.1954 = 0.4335
$$

There is about a 43% chance of 3 or fewer events.

---

## Using CDF for Range Probabilities

**$P(X > k)$:**

$$
P(X > k) = 1 - F(k) = 1 - P(X \leq k)
$$

**$P(X \geq k)$:**

$$
P(X \geq k) = 1 - F(k-1) = 1 - P(X \leq k-1)
$$

**$P(a \leq X \leq b)$:**

$$
P(a \leq X \leq b) = F(b) - F(a-1)
$$

---

## Expected Value and Variance

For the Poisson distribution, a remarkable property is:

$$
E[X] = \lambda
$$

$$
\text{Var}(X) = \lambda
$$

The mean and variance are equal. This property helps identify Poisson-distributed data.

**Standard deviation:**

$$
\sigma = \sqrt{\lambda}
$$

---

## Why Mean Equals Variance

**Derivation of $E[X]$:**

$$
E[X] = \sum_{k=0}^{\infty} k \cdot \frac{\lambda^k e^{-\lambda}}{k!} = \lambda e^{-\lambda} \sum_{k=1}^{\infty} \frac{\lambda^{k-1}}{(k-1)!} = \lambda e^{-\lambda} \cdot e^{\lambda} = \lambda
$$

**Derivation of $\text{Var}(X)$:**

Using $\text{Var}(X) = E[X^2] - (E[X])^2$ and computing $E[X^2]$ similarly gives $\text{Var}(X) = \lambda$.

---

## Mode of the Distribution

The mode (most likely value) is:

$$
\text{mode} = \lfloor \lambda \rfloor
$$

If $\lambda$ is an integer, both $\lambda$ and $\lambda - 1$ are modes.

**Example:** For $\lambda = 4.7$, mode = 4.

---

## Shape of the Distribution

The shape depends on $\lambda$:

**Small $\lambda$ (e.g., 1):**
- Right-skewed
- Mode at 0 or 1
- Rapid decay

**Large $\lambda$ (e.g., 10+):**
- More symmetric
- Approaches Normal distribution
- Mode near $\lambda$

---

## Normal Approximation

For large $\lambda$, the Poisson can be approximated by a Normal distribution:

$$
X \approx N(\lambda, \lambda)
$$

**Rule of thumb:** Approximation is reasonable when $\lambda \geq 10$.

**With continuity correction:**

$$
P(X \leq k) \approx \Phi\left(\frac{k + 0.5 - \lambda}{\sqrt{\lambda}}\right)
$$

---

## Poisson as Limit of Binomial

The Poisson distribution arises as a limit of the Binomial:

If $X \sim \text{Binomial}(n, p)$ with $n \to \infty$, $p \to 0$, and $np = \lambda$ fixed:

$$
\text{Binomial}(n, p) \to \text{Poisson}(\lambda)
$$

This is why Poisson is good for rare events in large populations.

**Example:** Probability of $k$ defects in 1000 items where each has 0.003 defect probability:

$\lambda = np = 1000 \times 0.003 = 3$

Use $\text{Poisson}(3)$ instead of $\text{Binomial}(1000, 0.003)$.

---

## Sum of Independent Poissons

If $X \sim \text{Poisson}(\lambda_1)$ and $Y \sim \text{Poisson}(\lambda_2)$ are independent:

$$
X + Y \sim \text{Poisson}(\lambda_1 + \lambda_2)
$$

**Example:** If department A gets 3 calls/hour and department B gets 5 calls/hour, the total is Poisson(8).

---

## Scaling the Interval

If events occur at rate $\lambda$ per unit time:

- In time $t$, the count follows $\text{Poisson}(\lambda t)$

**Example:** 10 emails/hour means:
- Per minute: $\text{Poisson}(10/60) = \text{Poisson}(1/6)$
- Per 3 hours: $\text{Poisson}(30)$

---

## Relationship to Exponential Distribution

The Poisson process has a dual relationship with the Exponential distribution:

- **Poisson:** Number of events in a fixed time
- **Exponential:** Time between consecutive events

If counts follow $\text{Poisson}(\lambda)$, then inter-arrival times follow $\text{Exponential}(\lambda)$.

---

## Maximum Likelihood Estimation

Given observations $x_1, x_2, ..., x_n$ from $\text{Poisson}(\lambda)$:

$$
\hat{\lambda} = \bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

The MLE is simply the sample mean.

---

## Checking if Data is Poisson

**Mean-variance test:**

For Poisson data, mean $\approx$ variance.

Compute the dispersion index:

$$
D = \frac{\text{Var}(X)}{\bar{X}}
$$

If $D \approx 1$: Consistent with Poisson

If $D > 1$: Overdispersion (consider Negative Binomial)

If $D < 1$: Underdispersion

---

## Applications in Machine Learning

**Count data modeling:**
- Number of clicks, purchases, page views
- Poisson regression for count outcomes

**Text analysis:**
- Word frequency models
- Topic modeling

**Anomaly detection:**
- Unusual event counts (e.g., fraud detection)

**Queuing theory:**
- Server load modeling
- Request arrival patterns
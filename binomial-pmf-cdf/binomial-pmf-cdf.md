## What Is a Binomial Distribution?

The Binomial distribution models the **number of successes** in a fixed number of independent trials, where each trial has the same probability of success.

It answers the question: "If I repeat an experiment $n$ times, each with success probability $p$, what is the probability of getting exactly $k$ successes?"

---

## The Four Conditions

A random variable follows a Binomial distribution if and only if:

**1. Fixed number of trials ($n$)**

The experiment is repeated a predetermined number of times.

**2. Independent trials**

The outcome of one trial does not affect the others.

**3. Two outcomes per trial**

Each trial results in either "success" or "failure."

**4. Constant probability ($p$)**

The probability of success is the same for every trial.

If any condition is violated, the Binomial model may not apply.

---

## Notation and Parameters

We write $X \sim \text{Binomial}(n, p)$ to indicate $X$ follows a Binomial distribution with:

- $n$ = number of trials (positive integer)
- $p$ = probability of success on each trial ($0 \leq p \leq 1$)

The random variable $X$ can take values $0, 1, 2, ..., n$.

---

## The Probability Mass Function (PMF)

The PMF gives the probability of exactly $k$ successes:

$$
P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}
$$

where $k \in \{0, 1, 2, ..., n\}$.

**Components explained:**

- $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ is the binomial coefficient, counting the number of ways to choose which $k$ trials are successes
- $p^k$ is the probability of $k$ successes
- $(1-p)^{n-k}$ is the probability of $n-k$ failures

---

## Understanding the Binomial Coefficient

The term $\binom{n}{k}$ counts the number of ways to arrange $k$ successes among $n$ trials.

**Example:** For $n = 4$ trials and $k = 2$ successes:

$$
\binom{4}{2} = \frac{4!}{2! \cdot 2!} = \frac{24}{2 \cdot 2} = 6
$$

The 6 possible patterns are: SSFF, SFSF, SFFS, FSSF, FSFS, FFSS

Each pattern has probability $p^2(1-p)^2$, and there are 6 of them.

---

## Worked Example: Coin Flips

**Setup:** Flip a fair coin ($p = 0.5$) 5 times. What is the probability of exactly 3 heads?

**Solution:**

$n = 5$, $k = 3$, $p = 0.5$

$$
P(X = 3) = \binom{5}{3} (0.5)^3 (0.5)^2
$$

$$
= \frac{5!}{3! \cdot 2!} \cdot 0.125 \cdot 0.25
$$

$$
= 10 \cdot 0.03125 = 0.3125
$$

There is a 31.25% chance of getting exactly 3 heads.

---

## Computing the Full PMF

**Setup:** $n = 4$, $p = 0.3$

**For each value of $k$:**

$P(X = 0) = \binom{4}{0}(0.3)^0(0.7)^4 = 1 \cdot 1 \cdot 0.2401 = 0.2401$

$P(X = 1) = \binom{4}{1}(0.3)^1(0.7)^3 = 4 \cdot 0.3 \cdot 0.343 = 0.4116$

$P(X = 2) = \binom{4}{2}(0.3)^2(0.7)^2 = 6 \cdot 0.09 \cdot 0.49 = 0.2646$

$P(X = 3) = \binom{4}{3}(0.3)^3(0.7)^1 = 4 \cdot 0.027 \cdot 0.7 = 0.0756$

$P(X = 4) = \binom{4}{4}(0.3)^4(0.7)^0 = 1 \cdot 0.0081 \cdot 1 = 0.0081$

**Verification:** $0.2401 + 0.4116 + 0.2646 + 0.0756 + 0.0081 = 1.0$ ✓

---

## The Cumulative Distribution Function (CDF)

The CDF gives the probability of at most $k$ successes:

$$
F(k) = P(X \leq k) = \sum_{i=0}^{k} \binom{n}{i} p^i (1-p)^{n-i}
$$

**Properties:**
- $F(k)$ is a step function, increasing at each integer
- $F(-1) = 0$ (by convention)
- $F(n) = 1$

---

## Computing CDF Values

**Setup:** $n = 4$, $p = 0.3$ (continuing previous example)

$F(0) = P(X \leq 0) = 0.2401$

$F(1) = P(X \leq 1) = 0.2401 + 0.4116 = 0.6517$

$F(2) = P(X \leq 2) = 0.6517 + 0.2646 = 0.9163$

$F(3) = P(X \leq 3) = 0.9163 + 0.0756 = 0.9919$

$F(4) = P(X \leq 4) = 0.9919 + 0.0081 = 1.0$

---

## Using the CDF for Range Probabilities

The CDF makes it easy to compute probabilities over ranges:

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

## Worked Example: Range Probability

**Setup:** $n = 10$, $p = 0.4$. Find $P(3 \leq X \leq 6)$.

$$
P(3 \leq X \leq 6) = F(6) - F(2)
$$

$$
= P(X \leq 6) - P(X \leq 2)
$$

$$
= \sum_{k=0}^{6} \binom{10}{k}(0.4)^k(0.6)^{10-k} - \sum_{k=0}^{2} \binom{10}{k}(0.4)^k(0.6)^{10-k}
$$

Computing: $F(6) \approx 0.9452$ and $F(2) \approx 0.1673$

$$
P(3 \leq X \leq 6) \approx 0.9452 - 0.1673 = 0.7779
$$

---

## Expected Value (Mean)

The expected number of successes is:

$$
E[X] = np
$$

**Derivation:**

$X = X_1 + X_2 + ... + X_n$ where each $X_i \sim \text{Bernoulli}(p)$

By linearity of expectation:

$$
E[X] = E[X_1] + E[X_2] + ... + E[X_n] = p + p + ... + p = np
$$

**Example:** In 100 coin flips with $p = 0.5$, we expect $100 \times 0.5 = 50$ heads.

---

## Variance

The variance of the number of successes is:

$$
\text{Var}(X) = np(1-p)
$$

**Derivation:**

Since $X_1, X_2, ..., X_n$ are independent:

$$
\text{Var}(X) = \text{Var}(X_1) + ... + \text{Var}(X_n) = np(1-p)
$$

**Standard deviation:**

$$
\sigma = \sqrt{np(1-p)}
$$

**Example:** For $n = 100$, $p = 0.5$:

$$
\text{Var}(X) = 100 \times 0.5 \times 0.5 = 25
$$

$$
\sigma = \sqrt{25} = 5
$$

---

## Mode of the Distribution

The mode (most likely value) is approximately:

$$
\text{mode} \approx \lfloor (n+1)p \rfloor \text{ or } \lceil (n+1)p \rceil - 1
$$

For integer $(n+1)p$, there may be two modes.

**Example:** $n = 10$, $p = 0.3$

$(n+1)p = 11 \times 0.3 = 3.3$

Mode = $\lfloor 3.3 \rfloor = 3$

The most likely number of successes is 3.

---

## Shape of the Distribution

The shape depends on $p$:

**$p < 0.5$:** Right-skewed (tail extends toward larger values)

**$p = 0.5$:** Symmetric

**$p > 0.5$:** Left-skewed (tail extends toward smaller values)

As $n$ increases, the distribution becomes more symmetric and bell-shaped (by the Central Limit Theorem).

---

## Normal Approximation

For large $n$, the Binomial can be approximated by a Normal distribution:

$$
X \approx N(np, np(1-p))
$$

**Rule of thumb:** The approximation is reasonable when:
- $np \geq 10$ and $n(1-p) \geq 10$

**Continuity correction:** Since Binomial is discrete and Normal is continuous:

$$
P(X \leq k) \approx \Phi\left(\frac{k + 0.5 - np}{\sqrt{np(1-p)}}\right)
$$

where $\Phi$ is the standard Normal CDF.

---

## Poisson Approximation

For large $n$ and small $p$ (with $np = \lambda$ moderate):

$$
\text{Binomial}(n, p) \approx \text{Poisson}(\lambda = np)
$$

**Rule of thumb:** Works well when $n \geq 20$ and $p \leq 0.05$.

This is useful because Poisson probabilities are easier to compute.

---

## Relationship to Bernoulli

The Binomial distribution is the sum of independent Bernoulli trials:

$$
X = \sum_{i=1}^{n} X_i
$$

where $X_i \sim \text{Bernoulli}(p)$ are independent.

Special case: $\text{Binomial}(1, p) = \text{Bernoulli}(p)$

---

## Sum of Binomials

If $X \sim \text{Binomial}(n_1, p)$ and $Y \sim \text{Binomial}(n_2, p)$ are independent with the **same** $p$:

$$
X + Y \sim \text{Binomial}(n_1 + n_2, p)
$$

This property does not hold if $p$ values differ.

---

## Applications in Machine Learning

**A/B testing:**

Comparing conversion rates between two versions. Each user's action is Bernoulli, total conversions are Binomial.

**Classification metrics:**

Number of true positives in $n$ predictions follows Binomial if predictions are independent.

**Bootstrap sampling:**

Number of times a specific sample appears follows approximately $\text{Binomial}(n, 1/n) \approx \text{Poisson}(1)$.

**Dropout regularization:**

Number of neurons kept in a layer follows Binomial distribution.

---

## Maximum Likelihood Estimation

Given observations from $\text{Binomial}(n, p)$ with known $n$, the MLE for $p$ is:

$$
\hat{p} = \frac{\bar{x}}{n}
$$

where $\bar{x}$ is the sample mean of observed counts.

If you observe a single value $x$:

$$
\hat{p} = \frac{x}{n}
$$

---

## Properties Summary

- **Support:** $\{0, 1, 2, ..., n\}$
- **Parameters:** $n \in \{1, 2, ...\}$, $p \in [0, 1]$
- **PMF:** $P(X = k) = \binom{n}{k}p^k(1-p)^{n-k}$
- **Mean:** $E[X] = np$
- **Variance:** $\text{Var}(X) = np(1-p)$
- **Skewness:** $\frac{1-2p}{\sqrt{np(1-p)}}$
- **MGF:** $M_X(t) = [(1-p) + pe^t]^n$
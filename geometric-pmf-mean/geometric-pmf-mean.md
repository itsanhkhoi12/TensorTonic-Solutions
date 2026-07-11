## What Is a Geometric Distribution?

The Geometric distribution models the **number of trials until the first success** in a sequence of independent Bernoulli trials.

It answers the question: "How many times must I repeat an experiment before I succeed for the first time?"

---

## Two Conventions

There are two common ways to define the Geometric distribution:

**Convention 1: Number of trials until first success**

$X \in \{1, 2, 3, ...\}$

Includes the successful trial in the count.

**Convention 2: Number of failures before first success**

$Y \in \{0, 1, 2, ...\}$

Counts only failures, not the success.

These are related by $X = Y + 1$. We will primarily use Convention 1.

---

## Real-World Examples

Many waiting-time scenarios follow a Geometric distribution:

- Number of coin flips until the first heads
- Number of job applications until the first offer
- Number of customers until the first purchase
- Number of attempts until passing an exam
- Number of rolls until rolling a six
- Number of server requests until the first failure

---

## The Parameter $p$

The Geometric distribution has a single parameter:

$$
p = P(\text{success on each trial})
$$

**Constraints:**
- $0 < p \leq 1$
- $p = 0$ is not allowed (you would wait forever)

The probability of failure is $q = 1 - p$.

---

## The Probability Mass Function (PMF)

For Convention 1 (number of trials until first success):

$$
P(X = k) = (1-p)^{k-1} p
$$

where $k \in \{1, 2, 3, ...\}$.

**Interpretation:**
- $(1-p)^{k-1}$ = probability of failing the first $k-1$ trials
- $p$ = probability of succeeding on trial $k$

---

## Deriving the PMF

To get the first success on trial $k$, we need:
- Failure on trial 1: probability $(1-p)$
- Failure on trial 2: probability $(1-p)$
- ...
- Failure on trial $k-1$: probability $(1-p)$
- Success on trial $k$: probability $p$

Since trials are independent:

$$
P(X = k) = \underbrace{(1-p) \cdot (1-p) \cdots (1-p)}_{k-1 \text{ times}} \cdot p = (1-p)^{k-1} p
$$

---

## Worked Example: Coin Flips

**Setup:** Flip a fair coin ($p = 0.5$) until you get heads. What is the probability that the first heads occurs on flip 4?

**Solution:**

$$
P(X = 4) = (1 - 0.5)^{4-1} \cdot 0.5 = (0.5)^3 \cdot 0.5 = 0.125 \cdot 0.5 = 0.0625
$$

There is a 6.25% chance the first heads is on flip 4.

---

## Computing Multiple PMF Values

**Setup:** $p = 0.3$ (30% success rate per trial)

$P(X = 1) = (0.7)^0 \cdot 0.3 = 1 \cdot 0.3 = 0.300$

$P(X = 2) = (0.7)^1 \cdot 0.3 = 0.7 \cdot 0.3 = 0.210$

$P(X = 3) = (0.7)^2 \cdot 0.3 = 0.49 \cdot 0.3 = 0.147$

$P(X = 4) = (0.7)^3 \cdot 0.3 = 0.343 \cdot 0.3 = 0.103$

$P(X = 5) = (0.7)^4 \cdot 0.3 = 0.240 \cdot 0.3 = 0.072$

The probabilities decrease geometrically (hence the name).

---

## Verifying the PMF Sums to 1

The sum of all probabilities must equal 1:

$$
\sum_{k=1}^{\infty} P(X = k) = \sum_{k=1}^{\infty} (1-p)^{k-1} p = p \sum_{j=0}^{\infty} (1-p)^j
$$

Using the geometric series formula $\sum_{j=0}^{\infty} r^j = \frac{1}{1-r}$ for $|r| < 1$:

$$
= p \cdot \frac{1}{1 - (1-p)} = p \cdot \frac{1}{p} = 1 \checkmark
$$

---

## Expected Value (Mean)

The expected number of trials until first success is:

$$
E[X] = \frac{1}{p}
$$

**Intuition:** If success probability is $p = 0.2$ (20%), you expect to need $1/0.2 = 5$ trials on average.

**Derivation:**

$$
E[X] = \sum_{k=1}^{\infty} k \cdot (1-p)^{k-1} p
$$

This sum evaluates to $1/p$ using calculus techniques (derivative of geometric series).

---

## Expected Value Examples

**Fair coin ($p = 0.5$):**
$$
E[X] = \frac{1}{0.5} = 2
$$
On average, 2 flips to get heads.

**Rolling a six ($p = 1/6$):**
$$
E[X] = \frac{1}{1/6} = 6
$$
On average, 6 rolls to get a six.

**1% success rate ($p = 0.01$):**
$$
E[X] = \frac{1}{0.01} = 100
$$
On average, 100 trials to succeed.

---

## Variance

The variance of the Geometric distribution is:

$$
\text{Var}(X) = \frac{1-p}{p^2}
$$

**Standard deviation:**
$$
\sigma = \frac{\sqrt{1-p}}{p}
$$

**Example:** For $p = 0.2$:
$$
\text{Var}(X) = \frac{0.8}{0.04} = 20
$$
$$
\sigma = \sqrt{20} \approx 4.47
$$

---

## Cumulative Distribution Function (CDF)

The CDF gives the probability of success by trial $k$:

$$
F(k) = P(X \leq k) = 1 - (1-p)^k
$$

**Derivation:**

$P(X \leq k)$ = probability of at least one success in $k$ trials

$= 1 - P(\text{no successes in } k \text{ trials})$

$= 1 - (1-p)^k$

---

## CDF Examples

**Setup:** $p = 0.3$

$F(1) = 1 - (0.7)^1 = 1 - 0.7 = 0.30$

$F(2) = 1 - (0.7)^2 = 1 - 0.49 = 0.51$

$F(3) = 1 - (0.7)^3 = 1 - 0.343 = 0.657$

$F(5) = 1 - (0.7)^5 = 1 - 0.168 = 0.832$

$F(10) = 1 - (0.7)^{10} = 1 - 0.028 = 0.972$

By trial 10, there is a 97.2% chance you have succeeded.

---

## Survival Function

The probability of NOT succeeding by trial $k$:

$$
P(X > k) = 1 - F(k) = (1-p)^k
$$

This is the probability of $k$ consecutive failures.

**Example:** For $p = 0.3$, probability of still waiting after 5 trials:
$$
P(X > 5) = (0.7)^5 = 0.168 = 16.8\%
$$

---

## Memoryless Property

The Geometric distribution is **memoryless**:

$$
P(X > s + t | X > s) = P(X > t)
$$

If you have already failed $s$ times, the probability of needing at least $t$ more trials is the same as starting fresh.

**Intuition:** Past failures do not affect future success probability. Each trial is independent.

**Example:** If you have flipped 10 tails in a row, the expected number of additional flips to get heads is still $1/p$, not less.

---

## Proof of Memorylessness

$$
P(X > s + t | X > s) = \frac{P(X > s + t \text{ and } X > s)}{P(X > s)}
$$

Since $X > s + t$ implies $X > s$:

$$
= \frac{P(X > s + t)}{P(X > s)} = \frac{(1-p)^{s+t}}{(1-p)^s} = (1-p)^t = P(X > t)
$$

The Geometric is the **only** discrete memoryless distribution.

---

## Alternative PMF (Convention 2)

For $Y$ = number of failures before first success:

$$
P(Y = k) = (1-p)^k p
$$

where $k \in \{0, 1, 2, ...\}$.

**Mean:**
$$
E[Y] = \frac{1-p}{p}
$$

**Variance:**
$$
\text{Var}(Y) = \frac{1-p}{p^2}
$$

Note: $Y = X - 1$, so $E[Y] = E[X] - 1 = \frac{1}{p} - 1 = \frac{1-p}{p}$

---

## Relationship to Other Distributions

**Negative Binomial:**

The Geometric is a special case of Negative Binomial with $r = 1$ success.

**Exponential:**

The Geometric is the discrete analog of the Exponential distribution. Both are memoryless.

**Bernoulli:**

Each trial in a Geometric sequence is a Bernoulli trial.

---

## Sum of Geometrics

If $X_1, X_2, ..., X_r$ are independent $\text{Geometric}(p)$ random variables:

$$
\sum_{i=1}^{r} X_i \sim \text{Negative Binomial}(r, p)
$$

This is the number of trials to get $r$ successes.

---

## Maximum Likelihood Estimation

Given observations $x_1, x_2, ..., x_n$ from $\text{Geometric}(p)$:

$$
\hat{p} = \frac{n}{\sum_{i=1}^{n} x_i} = \frac{1}{\bar{x}}
$$

The MLE is the reciprocal of the sample mean.

---

## Mode of the Distribution

The mode (most likely value) is always:

$$
\text{mode} = 1
$$

The probability decreases as $k$ increases, so the first trial is always most likely to be the success.

---

## Applications in Machine Learning

**Waiting time models:**
Expected number of iterations until convergence.

**Reliability:**
Number of uses until first failure.

**Sampling:**
Number of random samples until finding a specific type.

**Coupon collector:**
Related to collecting all items in a set.
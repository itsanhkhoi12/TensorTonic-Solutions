## What Is Matrix Factorization SGD?

Matrix factorization (MF) decomposes the user-item rating matrix into lower-dimensional latent factor matrices. Stochastic Gradient Descent (SGD) is the most common algorithm for learning these factors by iteratively minimizing prediction error.

The goal is to find user factors $\mathbf{p}_u$ and item factors $\mathbf{q}_i$ such that:

$$
r_{ui} \approx \mathbf{p}_u^T \mathbf{q}_i
$$

---

## The Model

**Rating prediction:**

$$
\hat{r}_{ui} = \mu + b_u + b_i + \mathbf{p}_u^T \mathbf{q}_i
$$

where:
- $\mu$: Global mean rating
- $b_u$: User bias
- $b_i$: Item bias
- $\mathbf{p}_u \in \mathbb{R}^k$: User latent factor vector
- $\mathbf{q}_i \in \mathbb{R}^k$: Item latent factor vector
- $k$: Number of latent factors (typically 20-200)

---

## The Objective Function

Minimize regularized squared error over observed ratings:

$$
\mathcal{L} = \sum_{(u,i) \in R} (r_{ui} - \hat{r}_{ui})^2 + \lambda \left( ||\mathbf{p}_u||^2 + ||\mathbf{q}_i||^2 + b_u^2 + b_i^2 \right)
$$

where:
- $R$ is the set of observed ratings
- $\lambda$ is the regularization strength

Regularization prevents overfitting by penalizing large parameter values.

---

## SGD Update Rules

For each observed rating $(u, i, r_{ui})$:

**Step 1: Compute prediction error**

$$
e_{ui} = r_{ui} - \hat{r}_{ui}
$$

**Step 2: Update biases**

$$
b_u \leftarrow b_u + \eta (e_{ui} - \lambda b_u)
$$

$$
b_i \leftarrow b_i + \eta (e_{ui} - \lambda b_i)
$$

**Step 3: Update latent factors**

$$
\mathbf{p}_u \leftarrow \mathbf{p}_u + \eta (e_{ui} \mathbf{q}_i - \lambda \mathbf{p}_u)
$$

$$
\mathbf{q}_i \leftarrow \mathbf{q}_i + \eta (e_{ui} \mathbf{p}_u - \lambda \mathbf{q}_i)
$$

where $\eta$ is the learning rate.

---

## Understanding the Update

The update for $\mathbf{p}_u$ has two parts:

**Gradient term:** $e_{ui} \mathbf{q}_i$

Move in the direction that reduces error. If $e_{ui} > 0$ (under-predicted), move $\mathbf{p}_u$ toward $\mathbf{q}_i$.

**Regularization term:** $-\lambda \mathbf{p}_u$

Shrink $\mathbf{p}_u$ toward zero to prevent overfitting.

The learning rate $\eta$ controls step size.

---

## Worked Example

**Setup:**

- Current $\mathbf{p}_u = [0.5, 0.3]$
- Current $\mathbf{q}_i = [0.4, 0.6]$
- Current $b_u = 0.2$, $b_i = -0.1$, $\mu = 3.5$
- Actual rating $r_{ui} = 4.0$
- Learning rate $\eta = 0.01$
- Regularization $\lambda = 0.02$

**Step 1: Compute prediction**

$$
\hat{r}_{ui} = 3.5 + 0.2 + (-0.1) + (0.5 \times 0.4 + 0.3 \times 0.6)
$$

$$
\hat{r}_{ui} = 3.5 + 0.1 + (0.2 + 0.18) = 3.5 + 0.1 + 0.38 = 3.98
$$

**Step 2: Compute error**

$$
e_{ui} = 4.0 - 3.98 = 0.02
$$

**Step 3: Update biases**

$$
b_u = 0.2 + 0.01 \times (0.02 - 0.02 \times 0.2) = 0.2 + 0.01 \times 0.016 = 0.20016
$$

$$
b_i = -0.1 + 0.01 \times (0.02 - 0.02 \times (-0.1)) = -0.1 + 0.01 \times 0.022 = -0.09978
$$

**Step 4: Update user factors**

$$
\mathbf{p}_u[0] = 0.5 + 0.01 \times (0.02 \times 0.4 - 0.02 \times 0.5) = 0.5 + 0.01 \times (-0.002) = 0.49998
$$

$$
\mathbf{p}_u[1] = 0.3 + 0.01 \times (0.02 \times 0.6 - 0.02 \times 0.3) = 0.3 + 0.01 \times 0.006 = 0.30006
$$

**Step 5: Update item factors**

$$
\mathbf{q}_i[0] = 0.4 + 0.01 \times (0.02 \times 0.5 - 0.02 \times 0.4) = 0.4 + 0.01 \times 0.002 = 0.40002
$$

$$
\mathbf{q}_i[1] = 0.6 + 0.01 \times (0.02 \times 0.3 - 0.02 \times 0.6) = 0.6 + 0.01 \times (-0.006) = 0.59994
$$

---

## Training Algorithm

**Initialize:**

- Set $\mu$ to global mean
- Initialize $b_u = 0$, $b_i = 0$
- Initialize $\mathbf{p}_u$, $\mathbf{q}_i$ with small random values

**For each epoch:**

1. Shuffle the observed ratings
2. For each rating $(u, i, r_{ui})$:
   - Compute error $e_{ui}$
   - Update $b_u$, $b_i$, $\mathbf{p}_u$, $\mathbf{q}_i$
3. Optionally compute total loss and check convergence

**Stopping criteria:**

- Fixed number of epochs
- Loss stops decreasing
- Validation error increases (early stopping)

---

## Learning Rate Scheduling

**Constant learning rate:**

Simple but may not converge to best solution.

**Decaying learning rate:**

$$
\eta_t = \frac{\eta_0}{1 + \alpha t}
$$

Larger steps early, smaller steps later for fine-tuning.

**Bold driver:**

Increase $\eta$ if loss decreased, decrease if loss increased.

---

## Importance of Shuffling

Shuffling ratings each epoch is crucial:

**Without shuffling:**

- Patterns in data order can bias learning
- Updates may oscillate

**With shuffling:**

- More random gradient estimates
- Better convergence properties
- Helps escape local minima

---

## Mini-Batch SGD

Instead of one rating at a time, use small batches:

**Compute average gradient over batch:**

$$
\mathbf{p}_u \leftarrow \mathbf{p}_u + \eta \left( \frac{1}{|B|} \sum_{(u,i) \in B} e_{ui} \mathbf{q}_i - \lambda \mathbf{p}_u \right)
$$

**Benefits:**

- More stable gradients
- Better GPU utilization
- Allows parallelization

---

## Initialization Strategies

**Random initialization:**

Draw from $\mathcal{N}(0, 0.01)$ or $\mathcal{U}(-0.01, 0.01)$

**Xavier/He initialization:**

Scale by $\sqrt{1/k}$ where $k$ is number of factors.

**SVD initialization:**

Initialize with truncated SVD of the rating matrix (requires imputation for missing values).

Good initialization can significantly speed up convergence.

---

## Handling the Cold Start During Training

**New user added:**

Initialize $\mathbf{p}_{new}$ with small random values. Updates will occur as they rate items.

**New item added:**

Initialize $\mathbf{q}_{new}$ with small random values. Updates will occur as it receives ratings.

The model learns from new data through continued SGD updates.

---

## Implicit Feedback Variant (ALS-WR)

For implicit feedback (clicks, views), use weighted regularization:

$$
\mathcal{L} = \sum_{u,i} c_{ui}(p_{ui} - \mathbf{p}_u^T \mathbf{q}_i)^2 + \lambda \left( ||\mathbf{p}_u||^2 + ||\mathbf{q}_i||^2 \right)
$$

where $c_{ui}$ is confidence (higher for observed interactions) and $p_{ui}$ is preference (1 if observed, 0 otherwise).

---

## Convergence Properties

**SGD convergence requires:**

- Decreasing learning rate (sum diverges, sum of squares converges)
- Or constant small learning rate (converges to neighborhood of optimum)

**Non-convex objective:**

Matrix factorization is non-convex. SGD finds local minima, which are usually good enough in practice.

---

## Parallelization

**Hogwild SGD:**

Update parameters without locks. Works because most updates affect different parameters (sparse interactions).

**Distributed SGD:**

Partition users or items across machines. Synchronize periodically.

**Alternating Least Squares (ALS):**

Alternative to SGD. Fix one matrix, solve for other. Easier to parallelize.
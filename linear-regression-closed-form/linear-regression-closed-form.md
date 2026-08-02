## The Linear Regression Problem

Linear regression finds the best straight line (or hyperplane) through data points. Given input features $X$ and target values $y$, we want to find weights $w$ such that:

$$
Xw \approx y
$$

The "best" weights minimize the sum of squared errors between predictions and actual values.

---

## Setting Up the Optimization

We want to minimize the squared error:

$$
L(w) = ||Xw - y||^2 = (Xw - y)^T(Xw - y)
$$

This is a quadratic function in $w$, shaped like a bowl. There is a unique minimum (when $X^T X$ is invertible), and we can find it exactly by setting the gradient to zero.

---

## Deriving the Normal Equation

**Step 1: Expand the loss**

$$
L(w) = (Xw - y)^T(Xw - y)
$$

$$
= w^T X^T X w - 2w^T X^T y + y^T y
$$

**Step 2: Take the gradient with respect to $w$**

$$
\nabla_w L = 2 X^T X w - 2 X^T y
$$

**Step 3: Set the gradient to zero**

$$
2 X^T X w - 2 X^T y = 0
$$

$$
X^T X w = X^T y
$$

**Step 4: Solve for $w$**

$$
w = (X^T X)^{-1} X^T y
$$

This is the **normal equation**, the closed-form solution to linear regression.

---

## Understanding Each Component

**$X^T X$** (the Gram matrix):
- Shape: $d \times d$ where $d$ is the number of features
- Symmetric and positive semi-definite
- Entry $(i, j)$ is the dot product of feature columns $i$ and $j$
- Captures the correlation structure of the features

**$(X^T X)^{-1}$:**
- The inverse of the Gram matrix
- Exists when features are not perfectly collinear
- Larger condition number means less stable solution

**$X^T y$:**
- Shape: $d \times 1$
- Entry $i$ is the dot product of feature column $i$ with the target
- Measures how aligned each feature is with the target

---

## A Numerical Example

**Data:** 3 samples, 2 features

$$
X = \begin{bmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{bmatrix}, \quad y = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}
$$

The first column is all ones (the intercept term).

**Step 1: Compute $X^T X$**

$$
X^T X = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & 3 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{bmatrix} = \begin{bmatrix} 3 & 6 \\ 6 & 14 \end{bmatrix}
$$

**Step 2: Compute $X^T y$**

$$
X^T y = \begin{bmatrix} 1 & 1 & 1 \\ 1 & 2 & 3 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix} = \begin{bmatrix} 5 \\ 11 \end{bmatrix}
$$

**Step 3: Compute $(X^T X)^{-1}$**

For a $2 \times 2$ matrix:

$$
\det(X^T X) = 3 \cdot 14 - 6 \cdot 6 = 42 - 36 = 6
$$

$$
(X^T X)^{-1} = \frac{1}{6} \begin{bmatrix} 14 & -6 \\ -6 & 3 \end{bmatrix} = \begin{bmatrix} 7/3 & -1 \\ -1 & 1/2 \end{bmatrix}
$$

**Step 4: Compute $w$**

$$
w = (X^T X)^{-1} X^T y = \begin{bmatrix} 7/3 & -1 \\ -1 & 1/2 \end{bmatrix} \begin{bmatrix} 5 \\ 11 \end{bmatrix} = \begin{bmatrix} 35/3 - 11 \\ -5 + 11/2 \end{bmatrix} = \begin{bmatrix} 2/3 \\ 1/2 \end{bmatrix}
$$

The regression line is: $\hat{y} = \frac{2}{3} + \frac{1}{2}x$

---

## When Does This Work?

**Invertibility requirement:**

$(X^T X)^{-1}$ exists when $X^T X$ is invertible, which requires:
- More samples than features ($n \geq d$)
- No perfect multicollinearity (no feature is a linear combination of others)

**Perfect multicollinearity:**

If two features are perfectly correlated (e.g., one is a scaled version of the other), $X^T X$ is singular. The system has infinitely many solutions.

---

## Numerical Stability Concerns

**Condition number:**

Even when $X^T X$ is technically invertible, it may be ill-conditioned. A large condition number means:
- Small changes in $X$ or $y$ cause large changes in $w$
- Floating-point errors are amplified
- The solution may be unreliable

**Better approaches:**

In practice, avoid computing $(X^T X)^{-1}$ directly. Instead:
- Use QR decomposition: $X = QR$, then solve $Rw = Q^T y$
- Use SVD: more stable for ill-conditioned problems
- Use iterative methods for very large datasets

---

## Adding Regularization

To handle multicollinearity or prevent overfitting, add a regularization term:

**Ridge regression (L2):**

$$
w = (X^T X + \lambda I)^{-1} X^T y
$$

The added $\lambda I$ makes the matrix invertible and shrinks weights toward zero.

**This still has a closed form!** Unlike Lasso (L1 regularization), which requires iterative optimization.

---

## Computational Complexity

- Computing $X^T X$: $O(nd^2)$
- Inverting $X^T X$: $O(d^3)$
- Total: $O(nd^2 + d^3)$

For small $d$ (few features), this is fast. For large $d$, iterative methods like gradient descent may be preferred.

---

## Connection to Projection

Geometrically, $Xw$ is the projection of $y$ onto the column space of $X$. The normal equation finds the point in that subspace closest to $y$.

The residual $y - Xw$ is orthogonal to all columns of $X$:

$$
X^T(y - Xw) = X^T y - X^T X w = 0
$$

This is exactly the normal equation rearranged!
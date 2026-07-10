## The Problem with Squared Error

Mean Squared Error (MSE) is the most common loss function for regression:

$$
\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
$$

MSE works well when errors are normally distributed, but it has a critical weakness: **sensitivity to outliers**.

Because errors are squared, large errors dominate the loss:

- An error of 2 contributes $2^2 = 4$ to the loss
- An error of 10 contributes $10^2 = 100$ to the loss
- An error of 100 contributes $100^2 = 10000$ to the loss

A single outlier with a large error can completely dominate the loss and pull the model away from fitting the majority of the data well.

---

## Mean Absolute Error: The Other Extreme

Mean Absolute Error (MAE) handles outliers better:

$$
\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|
$$

Large errors grow linearly, not quadratically:

- An error of 2 contributes 2 to the loss
- An error of 10 contributes 10 to the loss
- An error of 100 contributes 100 to the loss

MAE is much more robust to outliers. But it has its own problem: the gradient is constant everywhere (either +1 or -1), which can make optimization unstable near the minimum where we want gentle, precise adjustments.

---

## Huber Loss: The Best of Both Worlds

Huber loss combines MSE and MAE. It behaves like MSE for small errors and like MAE for large errors:

$$
L_\delta(y, \hat{y}) = \begin{cases} \frac{1}{2}(y - \hat{y})^2 & \text{if } |y - \hat{y}| \leq \delta \\ \delta \cdot |y - \hat{y}| - \frac{1}{2}\delta^2 & \text{if } |y - \hat{y}| > \delta \end{cases}
$$

where $\delta$ (delta) is a threshold parameter that controls when to switch from quadratic to linear behavior.

**The key insight:**

- For small errors ($|e| \leq \delta$): use squared error, which gives smooth gradients for precise optimization
- For large errors ($|e| > \delta$): use linear error, which prevents outliers from dominating

---

## Understanding the Formula

Let $e = y - \hat{y}$ be the error. The Huber loss can be written as:

$$
L_\delta(e) = \begin{cases} \frac{1}{2}e^2 & \text{if } |e| \leq \delta \\ \delta |e| - \frac{1}{2}\delta^2 & \text{if } |e| > \delta \end{cases}
$$

**Why the specific formula for large errors?**

The term $\delta |e| - \frac{1}{2}\delta^2$ is carefully chosen so that:

1. The function is **continuous** at $|e| = \delta$
2. The function is **differentiable** at $|e| = \delta$ (smooth transition)

At the boundary $|e| = \delta$:

- Quadratic piece: $\frac{1}{2}\delta^2$
- Linear piece: $\delta \cdot \delta - \frac{1}{2}\delta^2 = \frac{1}{2}\delta^2$

Both pieces give the same value, ensuring continuity.

---

## Concrete Examples

Let $\delta = 1.0$. Here are some loss values:

**Small errors (quadratic region):**

- Error $e = 0$: Loss $= \frac{1}{2}(0)^2 = 0$
- Error $e = 0.5$: Loss $= \frac{1}{2}(0.5)^2 = 0.125$
- Error $e = 1.0$: Loss $= \frac{1}{2}(1.0)^2 = 0.5$

**Large errors (linear region):**

- Error $e = 2.0$: Loss $= 1.0 \cdot 2.0 - \frac{1}{2}(1.0)^2 = 2.0 - 0.5 = 1.5$
- Error $e = 5.0$: Loss $= 1.0 \cdot 5.0 - 0.5 = 4.5$
- Error $e = 10.0$: Loss $= 1.0 \cdot 10.0 - 0.5 = 9.5$

**Comparison with MSE for the same errors:**

- Error $e = 2.0$: MSE $= 4.0$, Huber $= 1.5$
- Error $e = 5.0$: MSE $= 25.0$, Huber $= 4.5$
- Error $e = 10.0$: MSE $= 100.0$, Huber $= 9.5$

The Huber loss grows much more slowly for large errors, reducing the influence of outliers.

---

## The Gradient of Huber Loss

The gradient (derivative) of Huber loss with respect to the prediction:

$$
\frac{\partial L_\delta}{\partial \hat{y}} = \begin{cases} -(y - \hat{y}) = \hat{y} - y & \text{if } |y - \hat{y}| \leq \delta \\ -\delta \cdot \text{sign}(y - \hat{y}) & \text{if } |y - \hat{y}| > \delta \end{cases}
$$

**Key properties:**

- For small errors: gradient is proportional to the error (like MSE)
- For large errors: gradient is constant at $\pm\delta$ (like MAE, but bounded)
- The gradient is continuous at $|e| = \delta$
- No gradient explosion for outliers

This bounded gradient is why Huber loss is more stable during training when outliers are present.

---

## Choosing Delta

The threshold $\delta$ is a hyperparameter you must choose:

**Small $\delta$ (e.g., 0.1):**

- Most errors fall in the linear region
- Behavior is closer to MAE
- Very robust to outliers
- May be too aggressive in treating normal errors as outliers

**Large $\delta$ (e.g., 10.0):**

- Most errors fall in the quadratic region
- Behavior is closer to MSE
- Less robust to outliers
- Better optimization near the minimum

**Common default:** $\delta = 1.0$

**How to choose:**

- Look at the scale of your target variable
- Consider what error magnitude should be treated as an outlier
- Cross-validate different values

---

## Huber Loss for a Batch

For a batch of $n$ predictions, the mean Huber loss is:

$$
L = \frac{1}{n} \sum_{i=1}^{n} L_\delta(y_i, \hat{y}_i)
$$

Each sample's loss is computed independently using the piecewise formula, then averaged.

---

## When to Use Huber Loss

**Good use cases:**

- Regression with potential outliers in the target variable
- Noisy real-world data where some measurements may be corrupted
- When you want robustness without completely ignoring large errors
- Reinforcement learning (used in DQN for stable Q-value updates)

**When MSE might be better:**

- Clean data with no outliers
- When large errors should be heavily penalized
- Gaussian-distributed errors

**When MAE might be better:**

- Many outliers or heavy-tailed error distributions
- When you care about median prediction rather than mean

---

## Smooth L1 Loss

In some frameworks (especially object detection), you will see **Smooth L1 Loss**, which is Huber loss with $\delta = 1$:

$$
\text{Smooth L1}(e) = \begin{cases} 0.5 e^2 & \text{if } |e| < 1 \\ |e| - 0.5 & \text{otherwise} \end{cases}
$$

This is exactly Huber loss. The different name comes from the computer vision community, where it was popularized by the Fast R-CNN paper for bounding box regression.
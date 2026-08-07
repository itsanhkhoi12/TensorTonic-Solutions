## Why Gradients Explode

Training a neural network means computing gradients through backpropagation. The chain rule tells us to multiply the local derivatives at each layer together:

$$
\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial h_n} \cdot \frac{\partial h_n}{\partial h_{n-1}} \cdot \frac{\partial h_{n-1}}{\partial h_{n-2}} \cdots \frac{\partial h_2}{\partial h_1} \cdot \frac{\partial h_1}{\partial w_1}
$$

Each factor in that chain is a derivative from one layer. When many of these factors are greater than 1, the product grows exponentially. A network with 50 layers where each derivative is around 1.1 gives $1.1^{50} \approx 117$. If each is around 2, you get $2^{50} \approx 10^{15}$.

This is the **exploding gradient problem**. It shows up most often in:

- **Recurrent networks (RNNs)**: unrolling over many time steps creates a very deep chain of multiplications through the recurrent weight matrix
- **Very deep networks**: any architecture with many layers can suffer from this if the weights or activations are not carefully controlled
- **Certain activation functions**: functions without bounded derivatives (like ReLU, which has derivative 1 for all positive inputs) do not naturally limit gradient magnitude

When gradients explode, the parameter update becomes enormous. A single training step can push the weights so far that the loss jumps to a huge value or becomes NaN. Training effectively crashes.

---

## What Gradient Clipping Does

The idea is simple: **if the gradient is too big, shrink it before using it to update the weights.**

You pick a threshold (called the max norm). Before every parameter update, you check the size of the gradient. If it is within the threshold, you leave it alone. If it exceeds the threshold, you scale it down so its size equals exactly the threshold.

The key property: **clipping only changes the magnitude, never the direction.** The gradient still points in the same direction (toward decreasing loss), it just takes a smaller step. Think of it like a speed limit. You can still drive in whatever direction you want, but your speed is capped.

---

## The L2 Norm (Global Norm)

To measure "how big" a gradient is, we use the **L2 norm**. This is the same as the Euclidean distance from the origin.

For a 1D gradient vector $g = [g_1, g_2, \ldots, g_n]$:

$$
\|g\| = \sqrt{g_1^2 + g_2^2 + \cdots + g_n^2}
$$

A few examples to build intuition:

- $g = [3, 4]$: norm $= \sqrt{9 + 16} = \sqrt{25} = 5$
- $g = [1, 1, 1, 1]$: norm $= \sqrt{4} = 2$
- $g = [0, 0, 0]$: norm $= 0$

For multi-dimensional arrays (like a 2D weight matrix), the "global" norm treats the entire array as one long flattened vector and computes the norm over all elements. A $2 \times 2$ gradient $[[2, 2], [2, 2]]$ has norm $= \sqrt{4 + 4 + 4 + 4} = \sqrt{16} = 4$.

The word "global" means we compute a single norm across all gradient values, not separate norms per row or per layer. This gives one number that captures the overall gradient magnitude.

---

## The Clipping Rule

Once you have the norm, the rule is:

- If $\|g\| \leq \text{max\_norm}$: the gradient is fine, leave it unchanged
- If $\|g\| > \text{max\_norm}$: scale the gradient down

The scaling factor is:

$$
\text{scale} = \frac{\text{max\_norm}}{\|g\|}
$$

And the clipped gradient is:

$$
g_{\text{clipped}} = g \cdot \text{scale}
$$

**Example**: gradient $g = [6, 8]$, max norm $= 5$

1. Compute the norm: $\|g\| = \sqrt{36 + 64} = \sqrt{100} = 10$
2. Since $10 > 5$, clipping is needed
3. Scale factor: $\frac{5}{10} = 0.5$
4. Clipped gradient: $[6 \times 0.5, \; 8 \times 0.5] = [3.0, 4.0]$
5. Verify: $\|g_{\text{clipped}}\| = \sqrt{9 + 16} = 5.0$ (exactly the max norm)

**Example**: gradient $g = [0.1, 0.2, 0.2]$, max norm $= 1.0$

1. Compute the norm: $\|g\| = \sqrt{0.01 + 0.04 + 0.04} = \sqrt{0.09} = 0.3$
2. Since $0.3 \leq 1.0$, no clipping needed
3. Return the gradient unchanged: $[0.1, 0.2, 0.2]$

---

## Why Direction Matters

A common alternative is **element-wise clipping**, where each individual gradient value is capped independently (e.g., clamp every value to $[-1, 1]$). The problem with this approach is that it **changes the direction** of the gradient vector.

Consider $g = [0.5, 10.0]$ with element-wise clipping at 1.0:

- Element-wise result: $[0.5, 1.0]$. The ratio between the two components changed from $0.5 : 10 = 1 : 20$ to $0.5 : 1 = 1 : 2$. The gradient now points in a very different direction.
- Global norm result: the entire vector gets scaled by the same factor, so $[0.5, 10.0]$ becomes something like $[0.05, 1.0]$. The ratio $1 : 20$ is preserved. The direction is exactly the same.

Preserving direction matters because the gradient direction tells you which way loss decreases fastest. Changing the direction means you are no longer following the steepest descent path. Global norm clipping respects the geometry of the optimization landscape.

---

## Choosing the Max Norm

The max norm is a hyperparameter you set before training. Common choices:

- **1.0**: a popular default, especially for RNNs and LSTMs
- **0.5 to 5.0**: the typical range for most deep learning tasks
- **Larger values (10+)**: lighter clipping, only catches extreme spikes

How to think about it:

- **Too small**: you clip almost every step, which slows down learning because the effective learning rate becomes very small
- **Too large**: clipping rarely activates, so it does not protect against the occasional gradient spike
- **Just right**: clipping only triggers during unusual batches or early in training when gradients are unstable, and lets normal gradient steps through unmodified

A practical approach is to monitor the gradient norm during training and set the threshold just above the typical range.

---

## Where Gradient Clipping Shows Up

- **RNNs and LSTMs**: the original motivation for gradient clipping. Long sequences create deep computational graphs through time, making exploding gradients common
- **Transformers**: models like GPT and BERT use gradient clipping during training, typically with max norm around 1.0
- **Reinforcement learning**: policy gradient methods can produce wild gradient spikes when rewards are large or rare
- **Any unstable training run**: if you see loss suddenly jumping to NaN or infinity, gradient clipping is often the first fix to try
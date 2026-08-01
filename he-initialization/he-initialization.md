## Why Xavier Fails for ReLU

Xavier initialization assumes activations are roughly linear (like tanh near zero). But ReLU is different:

$$
\text{ReLU}(x) = \max(0, x)
$$

ReLU sets all negative values to zero, which **halves the variance** of the output compared to the input. If you have inputs with variance $\sigma^2$, after ReLU the variance is approximately $\sigma^2 / 2$.

With Xavier initialization, this variance reduction compounds through layers:
- Layer 1: variance $\rightarrow$ variance/2
- Layer 2: variance/2 $\rightarrow$ variance/4
- Layer 10: variance $\rightarrow$ variance/1024

Activations and gradients vanish in deep networks with ReLU when using Xavier.

---

## He Initialization (Kaiming Initialization)

He initialization, proposed by He et al. (2015), compensates for ReLU's variance reduction by doubling the weight variance:

$$
\text{Var}(W) = \frac{2}{n_{in}}
$$

This is twice the variance of Xavier (fan-in mode), accounting for the factor of 2 lost to ReLU.

---

## He Uniform Distribution

Draw weights uniformly from:

$$
W \sim U\left(-\sqrt{\frac{6}{n_{in}}}, \sqrt{\frac{6}{n_{in}}}\right)
$$

**Example:** Layer with 256 inputs

$\text{bound} = \sqrt{\frac{6}{256}} = \sqrt{0.0234} \approx 0.153$

Weights drawn from $U(-0.153, 0.153)$

---

## He Normal Distribution

Draw weights from a normal distribution:

$$
W \sim N\left(0, \sqrt{\frac{2}{n_{in}}}\right)
$$

**Example:** Layer with 256 inputs

$\sigma = \sqrt{\frac{2}{256}} = \sqrt{0.0078} \approx 0.088$

Weights drawn from $N(0, 0.088)$

---

## Derivation

Consider layer output: $y = \text{ReLU}(Wx)$

Before ReLU: $z = Wx$, and $\text{Var}(z) = n_{in} \cdot \text{Var}(W) \cdot \text{Var}(x)$

After ReLU (assuming symmetric input distribution around zero):
- Half the values become zero
- The other half are unchanged
- $\text{Var}(y) \approx \frac{1}{2} \text{Var}(z)$

To maintain $\text{Var}(y) = \text{Var}(x)$:

$$
\frac{1}{2} \cdot n_{in} \cdot \text{Var}(W) \cdot \text{Var}(x) = \text{Var}(x)
$$

$$
\text{Var}(W) = \frac{2}{n_{in}}
$$

---

## Worked Example: Comparing Xavier and He

**Layer:** 512 inputs, ReLU activation

**Xavier variance:** $\frac{1}{n_{in}} = \frac{1}{512} = 0.00195$

**He variance:** $\frac{2}{n_{in}} = \frac{2}{512} = 0.00391$

He initialization uses weights with twice the variance, compensating for ReLU.

---

## For Leaky ReLU

Leaky ReLU has a small slope $\alpha$ for negative values:

$$
\text{LeakyReLU}(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}
$$

The variance is not halved but reduced by factor $(1 + \alpha^2) / 2$.

He initialization for Leaky ReLU:

$$
\text{Var}(W) = \frac{2}{(1 + \alpha^2) \cdot n_{in}}
$$

For standard Leaky ReLU with $\alpha = 0.01$, this is nearly the same as regular He.

---

## Fan-In vs. Fan-Out Mode

**Fan-in mode (default):** Use $n_{in}$ in the formula

$$
\text{Var}(W) = \frac{2}{n_{in}}
$$

Preserves variance in the forward pass.

**Fan-out mode:** Use $n_{out}$ in the formula

$$
\text{Var}(W) = \frac{2}{n_{out}}
$$

Preserves variance in the backward pass.

**In practice:** Fan-in mode is more common and is the default in most frameworks.

---

## For Convolutional Layers

For a conv layer with kernel size $(k_h, k_w)$ and $c_{in}$ input channels:

$$
n_{in} = c_{in} \times k_h \times k_w
$$

**Example:** 3x3 conv with 128 input channels

$n_{in} = 128 \times 3 \times 3 = 1152$

$\text{Var}(W) = \frac{2}{1152} \approx 0.00174$

$\sigma = \sqrt{0.00174} \approx 0.042$

---

## He vs. Xavier: Side by Side

For a layer with $n_{in} = 1000$:

**Xavier Normal:**
$\sigma = \sqrt{\frac{1}{n_{in}}} = \sqrt{0.001} = 0.0316$

**He Normal:**
$\sigma = \sqrt{\frac{2}{n_{in}}} = \sqrt{0.002} = 0.0447$

He has $\sqrt{2} \approx 1.41$ times larger standard deviation.

---

## When to Use He Initialization

**Use He for:**
- ReLU activation
- Leaky ReLU
- PReLU
- ELU (approximately)
- Any ReLU-like activation that zeroes negative values

**Use Xavier for:**
- Tanh
- Sigmoid
- Linear layers without activation
- Softmax output layers

**General rule:** If your activation is ReLU-family, use He. Otherwise, use Xavier.

---

## Modern Deep Networks

He initialization enabled training of very deep networks:

**VGGNet (2014):** 16-19 layers, struggled with training

**ResNet (2015):** 50-152+ layers, trained successfully with He initialization

The combination of:
1. He initialization
2. ReLU activation
3. Batch normalization
4. Skip connections

Made training networks with 100+ layers practical.

---

## Biases

Like Xavier, biases are typically initialized to zero:

$$
b = 0
$$

Zero biases work well with He initialization.

---

## Verification

To verify He initialization is working:

1. Create a deep network (e.g., 50 layers) with ReLU
2. Initialize with He
3. Forward pass random data
4. Check activation variance at each layer

With correct initialization:
- Variance stays approximately constant through layers
- No explosion or collapse

With incorrect initialization (e.g., Xavier for ReLU):
- Variance shrinks exponentially
- Deep layers have near-zero activations

---

## Implementation Notes

**Normal distribution:**
- Mean: 0
- Std: $\sqrt{2 / n_{in}}$

**Uniform distribution:**
- Min: $-\sqrt{6 / n_{in}}$
- Max: $+\sqrt{6 / n_{in}}$

**Framework support:**
Most frameworks have built-in He/Kaiming initialization with options for:
- Distribution type (normal or uniform)
- Mode (fan_in or fan_out)
- Nonlinearity (relu, leaky_relu with slope)

---

## Historical Impact

He initialization was a crucial ingredient in the deep learning revolution:

- Showed that initialization matters for deep networks
- Provided principled approach based on activation function
- Enabled training of ResNet and subsequent architectures
- Demonstrated that "depth" was achievable with proper techniques

Along with batch normalization and skip connections, He initialization is part of the standard toolkit for training deep CNNs.
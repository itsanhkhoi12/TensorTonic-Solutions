## What Weight Decay Does

Neural networks with millions of parameters can memorize training data instead of learning general patterns. **Weight decay** is a regularization technique that discourages the model from relying on any single parameter being very large.

The idea: at every training step, shrink all the weights slightly toward zero. If a weight is large, it gets penalized more. If a weight is near zero, it barely changes. This keeps the overall magnitude of the network's parameters in check.

Mathematically, weight decay adds a penalty proportional to the weight itself:

$$
w_t = w_{t-1} - \eta \cdot \lambda \cdot w_{t-1}
$$

- $\lambda$ is the decay coefficient (typically 0.01 to 0.1)
- Each step, every weight gets multiplied by $(1 - \eta \lambda)$, which is slightly less than 1
- Over many steps, this prevents weights from growing unboundedly

---

## L2 Regularization vs. Weight Decay

These two terms are often used interchangeably, but they are **not the same thing** when combined with adaptive optimizers like Adam. This distinction is the entire reason AdamW exists.

**L2 regularization** adds a penalty to the **loss function**:

$$
L_{\text{total}} = L_{\text{original}} + \frac{\lambda}{2} \sum w_i^2
$$

When you compute the gradient of this modified loss, the gradient becomes:

$$
g_t^{\text{L2}} = g_t + \lambda \cdot w_{t-1}
$$

The regularization term $\lambda \cdot w_{t-1}$ gets mixed into the gradient. With vanilla SGD, this is equivalent to weight decay. But with Adam, it is not.

**Weight decay** directly shrinks the parameters, completely separate from the gradient:

$$
w_t = w_{t-1} - \eta \cdot \lambda \cdot w_{t-1} - \eta \cdot \text{(gradient-based update)}
$$

The decay happens independently, not through the gradient.

---

## Why L2 + Adam Breaks

With Adam, the gradient gets divided by $\sqrt{v_t}$, where $v_t$ is the running average of squared gradients. This is what gives Adam its adaptive learning rates.

When you use L2 regularization with Adam, the regularization term $\lambda \cdot w$ gets mixed into the gradient **before** the adaptive scaling happens:

1. Modified gradient: $g_t^{\text{L2}} = g_t + \lambda \cdot w_{t-1}$
2. Second moment: $v_t = \beta_2 v_{t-1} + (1 - \beta_2)(g_t^{\text{L2}})^2$
3. Update: $w_t = w_{t-1} - \eta \cdot \frac{m_t}{\sqrt{v_t} + \epsilon}$

The problem: the weight decay signal ($\lambda \cdot w$) is being **divided by** $\sqrt{v_t}$. For parameters with large gradients, $v_t$ is large, so the decay effect is weakened. For parameters with small gradients, $v_t$ is small, so the decay effect is amplified.

This means:

- Parameters that are actively learning (large gradients) get almost no regularization
- Parameters that are barely changing (small gradients) get hit with strong regularization
- The effective regularization strength depends on the gradient magnitude, which is the opposite of what you want

---

## AdamW: The Fix

AdamW (proposed by Loshchilov and Hutter, 2019) solves this by **decoupling** weight decay from the gradient update. The weight decay is applied directly to the parameters, completely bypassing the adaptive scaling.

The three steps:

**Step 1**: Update first moment (same as Adam)

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t
$$

**Step 2**: Update second moment (same as Adam)

$$
v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2
$$

**Step 3**: Parameter update (different from Adam)

$$
w_t = w_{t-1} - \eta \cdot \lambda \cdot w_{t-1} - \eta \cdot \frac{m_t}{\sqrt{v_t} + \epsilon}
$$

Notice the update has two separate terms:

- $\eta \cdot \lambda \cdot w_{t-1}$: the weight decay, applied directly to the parameters. Not affected by $v_t$ at all.
- $\eta \cdot \frac{m_t}{\sqrt{v_t} + \epsilon}$: the adaptive gradient update, exactly like standard Adam.

The weight decay now affects every parameter equally (proportional to its magnitude), regardless of its gradient history. This is the "decoupled" part.

---

## A Concrete Example

Parameters: $w = [1.0, -2.0]$, moments: $m = [0.0, 0.0]$, $v = [0.0, 0.0]$, gradient: $g = [0.3, -0.7]$, $\eta = 0.01$, $\lambda = 0.1$, $\beta_1 = 0.9$, $\beta_2 = 0.999$

**Step 1** (first moment):

- $m_1 = 0.9 \times 0 + 0.1 \times 0.3 = 0.03$
- $m_2 = 0.9 \times 0 + 0.1 \times (-0.7) = -0.07$

**Step 2** (second moment):

- $v_1 = 0.999 \times 0 + 0.001 \times 0.09 = 0.00009$
- $v_2 = 0.999 \times 0 + 0.001 \times 0.49 = 0.00049$

**Step 3** (parameter update for $w_1$):

- Weight decay: $0.01 \times 0.1 \times 1.0 = 0.001$
- Gradient update: $0.01 \times \frac{0.03}{\sqrt{0.00009} + 10^{-8}} = 0.01 \times \frac{0.03}{0.00949} \approx 0.0316$
- New $w_1 = 1.0 - 0.001 - 0.0316 \approx 0.967$

The weight decay ($0.001$) and gradient update ($0.0316$) are independent. The decay does not get scaled by the second moment.

---

## Why It Matters in Practice

AdamW has become the **default optimizer** for training Transformers and large language models:

- **GPT, BERT, T5**: all trained with AdamW
- **Vision Transformers (ViT)**: use AdamW instead of SGD+momentum (which was standard for CNNs)
- **Fine-tuning pretrained models**: AdamW with small weight decay is the standard recipe

The practical benefits:

- Learning rate and weight decay can be tuned **independently**. Changing one does not affect how the other behaves.
- Better generalization: the regularization works as intended, leading to models that perform better on test data
- Typical weight decay values: $0.01$ to $0.1$, with $0.01$ being the most common default

---

## Special Case: Zero Weight Decay

When weight decay $= 0$, AdamW is identical to standard Adam. The weight decay term vanishes:

$$
w_t = w_{t-1} - 0 - \eta \cdot \frac{m_t}{\sqrt{v_t} + \epsilon}
$$

This makes AdamW a strict generalization of Adam. You can always use AdamW and set $\lambda = 0$ to recover Adam behavior.
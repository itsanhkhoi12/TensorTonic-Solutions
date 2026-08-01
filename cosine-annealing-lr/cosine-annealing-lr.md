## Why Decay the Learning Rate

During training, the learning rate controls the step size of each parameter update. The ideal step size changes over the course of training:

- **Early training**: the model is far from any minimum. Large steps are needed to explore the loss landscape and make rapid progress. A high learning rate lets the optimizer cover ground quickly.
- **Mid training**: the model is in a promising region. Moderate steps help navigate toward a good minimum without overshooting.
- **Late training**: the model is near a minimum. Small steps are needed to settle in precisely. Large steps would bounce the parameters back and forth across the minimum.

A **fixed** learning rate is always a compromise. Learning rate schedulers solve this by **reducing the rate over time**, so you get the best of all phases.

---

## The Problem with Linear Decay

The simplest schedule is linear decay: the learning rate drops at a constant rate from start to finish.

$$
\eta(t) = \eta_{\max} - (\eta_{\max} - \eta_{\min}) \cdot \frac{t}{T}
$$

This works, but it has a suboptimal shape. Linear decay:

- Drops quickly at the start, where you actually want to **maintain** a high rate for exploration
- Drops at the same rate in the middle, where most of the productive learning happens
- Drops linearly at the end, when the rate is already small and further reductions have diminishing impact

Ideally, you want a schedule that:

- **Stays high longer** at the start (more exploration time)
- **Drops faster in the middle** (transition from exploration to exploitation)
- **Flattens out at the end** (gentle convergence, no sudden changes)

This is exactly the shape of a cosine curve.

---

## The Cosine Annealing Formula

$$
\eta_t = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min})\left(1 + \cos\left(\frac{t}{T} \cdot \pi\right)\right)
$$

Breaking this apart:

- The cosine function traces half a period, from $\cos(0) = 1$ to $\cos(\pi) = -1$
- Adding 1 shifts the range to $[0, 2]$
- Multiplying by $\frac{1}{2}$ rescales to $[0, 1]$
- Multiplying by $(\eta_{\max} - \eta_{\min})$ scales to the learning rate range
- Adding $\eta_{\min}$ shifts to $[\eta_{\min}, \eta_{\max}]$

The result is a smooth curve from $\eta_{\max}$ down to $\eta_{\min}$.

---

## Tracing the Curve Step by Step

With $\eta_{\max} = 0.1$, $\eta_{\min} = 0$, $T = 100$:

**At $t = 0$** (start):
- $\cos(0) = 1$
- $\eta = 0 + 0.05 \times (1 + 1) = 0.05 \times 2 = 0.1$ (full learning rate)

**At $t = 10$** (10% through):
- $\cos(0.1\pi) = \cos(18°) \approx 0.951$
- $\eta = 0.05 \times (1 + 0.951) = 0.05 \times 1.951 \approx 0.0976$ (barely dropped)

**At $t = 25$** (25% through):
- $\cos(0.25\pi) = \cos(45°) \approx 0.707$
- $\eta = 0.05 \times 1.707 \approx 0.0854$ (still high)

**At $t = 50$** (halfway):
- $\cos(0.5\pi) = \cos(90°) = 0$
- $\eta = 0.05 \times 1 = 0.05$ (exactly the midpoint)

**At $t = 75$** (75% through):
- $\cos(0.75\pi) = \cos(135°) \approx -0.707$
- $\eta = 0.05 \times 0.293 \approx 0.0146$ (dropping fast now)

**At $t = 90$** (90% through):
- $\cos(0.9\pi) \approx -0.951$
- $\eta = 0.05 \times 0.049 \approx 0.0024$ (nearly at minimum)

**At $t = 100$** (end):
- $\cos(\pi) = -1$
- $\eta = 0.05 \times 0 = 0$ (exactly $\eta_{\min}$)

Compare to linear decay at the same points: $0.1, 0.09, 0.075, 0.05, 0.025, 0.01, 0$. Cosine keeps the rate higher for longer in the first half, then drops more steeply.

---

## Cosine vs. Linear: The Key Difference

Looking at how much "training budget" is spent at different learning rate levels:

**Linear decay**:
- Equal time at every learning rate
- 25% of training is above $\eta = 0.075$
- 25% is between $0.05$ and $0.075$
- 25% is between $0.025$ and $0.05$
- 25% is below $0.025$

**Cosine annealing**:
- More time at high and low rates, less in the middle
- ~35% of training is above $\eta = 0.075$ (more exploration)
- ~15% is between $0.05$ and $0.075$
- ~15% is between $0.025$ and $0.05$
- ~35% is below $0.025$ (more fine-tuning)

Cosine spends more time in the productive regimes (high rates for exploration, low rates for convergence) and less time in the intermediate zone.

---

## Warm Restarts (SGDR)

A powerful extension is **cosine annealing with warm restarts** (Loshchilov and Hutter, 2017, the "SGDR" paper):

Instead of one long cosine curve, run multiple shorter cycles:

1. Start at $\eta_{\max}$, anneal to $\eta_{\min}$ over $T_0$ steps
2. **Restart**: jump the learning rate back to $\eta_{\max}$
3. Anneal again, but over $T_1 = T_0 \times \text{mult}$ steps (longer cycle)
4. Restart again, anneal over $T_2 = T_1 \times \text{mult}$ steps
5. Continue...

Why restarts help:

- Each restart gives the optimizer a **large learning rate again**, which can kick it out of a suboptimal local minimum
- The model can explore a new region of the loss landscape
- The progressively longer cycles allow for finer convergence in later cycles
- This is a form of **exploration-exploitation tradeoff** built into the schedule

With $\text{mult} = 2$: cycles of length 10, 20, 40, 80, ... steps.

---

## Handling Steps Beyond Total Steps

When the current step $t$ exceeds $T$, most implementations clamp the learning rate at $\eta_{\min}$. The cosine formula would extrapolate beyond $\cos(\pi)$, which would start increasing the learning rate again. Clamping prevents this.

Some implementations allow this "overshoot" intentionally as a form of warm restart (a full cosine period instead of half).

---

## Where Cosine Annealing Shows Up

- **Image classification**: cosine annealing is the standard schedule for training ResNets, EfficientNets, ConvNeXts, and Vision Transformers. It has largely replaced step decay (the older approach of dropping the learning rate by 10x at specific epochs).
- **Large language models**: many LLM training recipes use warmup + cosine decay. GPT-3 and similar models used this approach.
- **Contrastive learning**: SimCLR, MoCo, CLIP, and other self-supervised methods use cosine schedules.
- **Object detection and segmentation**: DETR, Mask R-CNN, and other detection models often use cosine annealing.
- **As a default**: when in doubt about which schedule to use, cosine annealing is a safe choice. It performs at least as well as linear decay on almost every task and often better.
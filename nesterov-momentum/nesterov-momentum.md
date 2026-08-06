## Why Momentum Exists

Vanilla gradient descent updates parameters using only the current gradient:

$$
w_t = w_{t-1} - \eta \cdot g_t
$$

This has several problems:

- **Noisy gradients**: each mini-batch gives a slightly different gradient estimate. The path to the minimum zigzags because each step points in a slightly different direction.
- **Slow in valleys**: consider a loss surface that is steep in one direction and shallow in another (like a narrow valley). Gradient descent oscillates back and forth across the steep walls while making slow progress along the valley floor.
- **No inertia**: each step is independent. The optimizer has no memory of where it has been going. It cannot build up speed in a consistent direction.

**Momentum** fixes all of these by adding a velocity term:

$$
v_t = \mu \cdot v_{t-1} + \eta \cdot g_t
$$

$$
w_t = w_{t-1} - v_t
$$

- $\mu$ is the momentum coefficient (typically 0.9 or 0.99)
- $v_t$ is the **velocity**: a running accumulation of gradients
- The velocity builds up when gradients point consistently in one direction
- The velocity cancels out when gradients oscillate (because positive and negative gradients cancel)

Think of a ball rolling down a hill:
- On a consistent slope, the ball accelerates (velocity builds up)
- In a valley, the ball oscillates from side to side, but the side-to-side components cancel while the forward component accumulates
- The ball rolls much faster along the valley floor than gradient descent's cautious step-by-step approach

---

## The Problem with Standard Momentum

Standard momentum evaluates the gradient at the **current position** $w_{t-1}$, then uses the velocity to move. But the velocity is about to carry the parameters somewhere new. By the time the update is applied, the gradient information is slightly stale.

This causes **overshooting**. When the optimizer approaches a minimum:

1. The velocity is large (built up from the downhill run)
2. The gradient at the current position says "keep going" (still on the slope)
3. The velocity carries the parameters **past** the minimum
4. Now the gradient reverses, but the velocity still points in the old direction
5. It takes several steps for the gradient to overcome the accumulated velocity
6. The optimizer oscillates around the minimum before settling

The more momentum you have (larger $\mu$), the worse the overshooting.

---

## Nesterov's Insight: Look Before You Leap

Nesterov Accelerated Gradient (NAG), proposed by Yurii Nesterov in 1983, has an elegant fix:

**Instead of evaluating the gradient where you are, evaluate it where momentum is about to take you.**

The algorithm:

**Step 1**: Compute the **look-ahead position** (where momentum would take you):

$$
w_{\text{look}} = w_{t-1} - \mu \cdot v_{t-1}
$$

This is not an update. It is a hypothetical: "if I just applied my current velocity, where would I end up?"

**Step 2**: Compute the gradient at the **look-ahead position**:

$$
g_{\text{look}} = g(w_{\text{look}})
$$

Instead of asking "what is the gradient here?", we ask "what is the gradient **there** (where I am heading)?"

**Step 3**: Update velocity using this look-ahead gradient:

$$
v_t = \mu \cdot v_{t-1} + \eta \cdot g_{\text{look}}
$$

**Step 4**: Update parameters:

$$
w_t = w_{t-1} - v_t
$$

---

## Why Looking Ahead Reduces Overshooting

Imagine rolling toward a valley with a hill on the other side:

**Standard momentum**:
- You are on the downslope
- Gradient at your position says "the slope goes down, keep going"
- Velocity is large and pointing downhill
- You overshoot into the uphill region before the gradient reverses

**Nesterov momentum**:
- You are on the downslope
- But first, you jump ahead to where momentum would take you (already partway up the other side)
- Gradient at **that** position says "you are going uphill, slow down"
- The velocity gets a correction **before** you actually move
- You overshoot less because the correction is proactive, not reactive

The difference is subtle but compounds over many steps. Nesterov momentum consistently converges faster and more smoothly.

---

## A Side-by-Side Comparison

Minimizing $f(x) = x^2$ (minimum at $x = 0$). Gradient: $g(x) = 2x$.

Starting: $w = 5.0$, $v = 1.0$, $\mu = 0.9$, $\eta = 0.01$

**Standard momentum**:
- Gradient at current position: $g(5.0) = 10.0$
- New velocity: $v = 0.9 \times 1.0 + 0.01 \times 10.0 = 0.9 + 0.1 = 1.0$
- New position: $w = 5.0 - 1.0 = 4.0$

**Nesterov momentum**:
- Look-ahead: $w_{\text{look}} = 5.0 - 0.9 \times 1.0 = 4.1$
- Gradient at look-ahead: $g(4.1) = 8.2$ (smaller, because 4.1 is closer to the minimum)
- New velocity: $v = 0.9 \times 1.0 + 0.01 \times 8.2 = 0.982$
- New position: $w = 5.0 - 0.982 = 4.018$

The differences:
- Nesterov used gradient 8.2 instead of 10.0 (more accurate for where we are heading)
- Nesterov's velocity is 0.982 instead of 1.0 (slightly smaller, less overshooting)
- Nesterov ended at 4.018 instead of 4.0 (slightly further, because the lower velocity also means less "braking")

These differences are small per step but accumulate significantly over hundreds or thousands of steps.

---

## Convergence Theory

For convex functions, Nesterov momentum has a provably better convergence rate than standard momentum:

- **Gradient descent**: convergence rate $O(1/t)$ (error decreases as $1/t$)
- **Gradient descent + momentum**: convergence rate $O(1/t)$ (same theoretical rate, but better constant)
- **Nesterov momentum**: convergence rate $O(1/t^2)$ (quadratically faster!)

This is a major theoretical result. $O(1/t^2)$ is actually the **optimal rate** for first-order methods on convex functions. No gradient-based method can do better (without additional information like second-order derivatives).

For non-convex problems (like deep learning), the theoretical guarantees are weaker, but Nesterov momentum still consistently performs better in practice.

---

## Where Nesterov Momentum Shows Up

- **SGD + Nesterov**: the standard variant of SGD for image classification. ResNets, VGGs, EfficientNets, and other CNNs are often trained with SGD + Nesterov momentum ($\mu = 0.9$).
- **Nadam**: Nesterov momentum applied inside Adam. The Adam update uses the Nesterov-adjusted first moment instead of the standard first moment.
- **PyTorch SGD**: when you set `nesterov=True` in `torch.optim.SGD`, it uses the Nesterov variant.
- **When SGD beats Adam**: on large-scale image classification and other tasks where well-tuned SGD generalizes better than Adam, Nesterov momentum is almost always included. It is the standard "serious SGD" configuration.
- **Convex optimization**: Nesterov's accelerated gradient method is foundational in optimization theory and is used in many fields beyond machine learning.
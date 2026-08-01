## Why the Learning Rate Matters

The learning rate $\eta$ controls how big of a step the optimizer takes at each training iteration:

$$
w_t = w_{t-1} - \eta \cdot g_t
$$

If the learning rate is too high:
- The optimizer overshoots the minimum, bouncing back and forth
- Training loss oscillates wildly or even diverges to infinity
- The model never settles into a good solution

If the learning rate is too low:
- Each step is tiny, so training takes forever
- The optimizer can get stuck in shallow local minima or flat regions
- It may never reach a good solution within the training budget

No single fixed learning rate is ideal for the entire training run. Early on, you want larger steps to make fast progress. Later, you want smaller steps to fine-tune the solution without overshooting. This is why we use **learning rate schedulers**.

---

## The Warmup Phase

At the very start of training, the model's weights are randomly initialized. The gradients computed from these random weights can be unreliable and have high variance. Taking large steps based on these noisy early gradients can push the model into a bad region of the loss landscape that is hard to recover from.

**Warmup** solves this by starting with a very small learning rate and gradually increasing it:

- Step 0: learning rate is 0 (or very close to 0)
- Over the next $W$ steps, the learning rate increases linearly
- At step $W$, the learning rate reaches its target value $\eta_0$

During warmup, the model makes cautious, small updates while the optimizer's internal state (like Adam's moment estimates) stabilizes. Once those estimates are reliable, the full learning rate kicks in.

Warmup is especially important for:
- **Transformer models**: without warmup, training often diverges in the first few hundred steps
- **Large batch training**: bigger batches produce noisier gradient estimates early on
- **Adam/AdamW**: the second moment estimates need several steps to become accurate

---

## Linear Decay

After warmup, the learning rate is at its peak $\eta_0$. For the rest of training, it **decays linearly** toward a final value $\eta_f$ (often 0):

- The decay happens smoothly over the remaining steps from $W$ to $T$
- At step $T$ (total training steps), the learning rate reaches exactly $\eta_f$
- After step $T$, it stays fixed at $\eta_f$

Why decay the learning rate?

- **Early training**: large learning rate helps explore the loss landscape and make rapid progress toward a good region
- **Late training**: small learning rate helps the optimizer settle precisely into a minimum without bouncing around
- **Linear decay** is the simplest schedule: the learning rate drops at a constant rate per step

---

## The Three Phases

A linear schedule with warmup has three distinct phases:

**Phase 1: Warmup** (step $t < W$)

The learning rate increases linearly from 0 to $\eta_0$:

$$
\text{LR}(t) = \frac{t \cdot \eta_0}{W}
$$

For example, with $W = 10$ and $\eta_0 = 0.001$:
- Step 0: $\text{LR} = 0$
- Step 5: $\text{LR} = 0.0005$
- Step 10: $\text{LR} = 0.001$

**Phase 2: Decay** ($W \leq t \leq T$)

The learning rate decreases linearly from $\eta_0$ to $\eta_f$:

$$
\text{LR}(t) = \eta_f + (\eta_0 - \eta_f) \cdot \frac{T - t}{T - W}
$$

This is a linear interpolation. At $t = W$, the fraction is $\frac{T - W}{T - W} = 1$, giving $\eta_0$. At $t = T$, the fraction is $\frac{0}{T - W} = 0$, giving $\eta_f$.

For example, with $W = 10$, $T = 100$, $\eta_0 = 0.001$, $\eta_f = 0$:
- Step 10: $\text{LR} = 0.001$
- Step 55: $\text{LR} = 0.0005$
- Step 100: $\text{LR} = 0$

**Phase 3: Post-training** ($t > T$)

The learning rate stays fixed at $\eta_f$. No further changes.

---

## Linear vs. Other Schedules

Linear decay is the simplest schedule, but there are alternatives:

- **Cosine decay**: the learning rate follows a cosine curve, decaying slowly at first, then faster, then slowly again near the end. This is the most popular alternative to linear decay.
- **Step decay**: the learning rate drops by a fixed factor (e.g., $\times 0.1$) at specific milestones (e.g., at 30%, 60%, 90% of training). Common in older CNN training recipes.
- **Exponential decay**: the learning rate is multiplied by a constant factor each step, giving exponential decrease.
- **Constant**: no schedule at all. Rarely used for serious training.

Linear decay is popular because:
- It is simple and predictable
- It has no extra hyperparameters beyond the start/end rates and warmup length
- It works well in practice, especially for fine-tuning pretrained models

---

## Where This Shows Up

- **Transformer pretraining**: warmup + linear (or cosine) decay is the standard recipe for GPT, BERT, and similar models. BERT's original paper used linear warmup + linear decay.
- **Fine-tuning**: when adapting a pretrained model to a new task, a short warmup followed by linear decay to zero is common
- **Hugging Face Transformers**: the library's default scheduler is exactly this: linear warmup then linear decay
- **Any training loop**: learning rate scheduling is standard practice in modern deep learning, not an optional extra
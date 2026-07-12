## What Is Temporal Difference Learning?

Temporal Difference (TD) learning is a fundamental reinforcement learning method that combines ideas from Monte Carlo methods and dynamic programming.

Like Monte Carlo, TD learns from experience without a model. Like dynamic programming, TD updates estimates based on other estimates (bootstrapping).

TD is the foundation for many RL algorithms including Q-learning and SARSA.

---

## The Key Insight

Instead of waiting until the end of an episode to update value estimates, TD updates **after each step** using the observed reward and the estimated value of the next state.

$$
V(S_t) \leftarrow V(S_t) + \alpha \left[ R_{t+1} + \gamma V(S_{t+1}) - V(S_t) \right]
$$

This is called **TD(0)** or one-step TD.

---

## Understanding the Update

The TD update moves the current estimate toward a better estimate:

$$
V_{new}(s) = V_{old}(s) + \alpha \cdot \delta_t
$$

where the **TD error** is:

$$
\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)
$$

**Components:**
- $R_{t+1}$: Immediate reward received
- $\gamma V(S_{t+1})$: Discounted value of next state
- $V(S_t)$: Current estimate being updated
- $R_{t+1} + \gamma V(S_{t+1})$: TD target (better estimate)

---

## The TD Target

The TD target is:

$$
\text{target} = R_{t+1} + \gamma V(S_{t+1})
$$

This is a **one-step return**: the actual reward plus the estimated future value.

Compare to Monte Carlo target: $G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ...$

TD uses an estimate ($V(S_{t+1})$) instead of waiting for the complete return.

---

## Bootstrapping

**Bootstrapping** means updating estimates based on other estimates.

TD bootstraps because the target includes $V(S_{t+1})$, which is itself an estimate.

**Advantages:**
- Can learn before episode ends
- Lower variance than Monte Carlo
- Works for continuing (non-episodic) tasks

**Disadvantages:**
- Introduces bias (estimates may be wrong)
- Can propagate errors

---

## TD(0) Algorithm for Policy Evaluation

**Input:** Policy $\pi$ to evaluate

**Initialize:** $V(s)$ arbitrarily for all $s$

**Repeat for each episode:**

1. Initialize state $S$

2. **Repeat for each step:**
   - $A \leftarrow$ action given by $\pi$ for $S$
   - Take action $A$, observe $R$, $S'$
   - $V(S) \leftarrow V(S) + \alpha[R + \gamma V(S') - V(S)]$
   - $S \leftarrow S'$

3. Until $S$ is terminal

---

## Worked Example

**Setup:**
- Current state: $S_t$
- Current value estimate: $V(S_t) = 10$
- Action taken leads to reward $R_{t+1} = 3$
- Next state: $S_{t+1}$
- Value of next state: $V(S_{t+1}) = 8$
- Learning rate: $\alpha = 0.1$
- Discount factor: $\gamma = 0.9$

**Step 1: Compute TD target**
$$
\text{target} = R_{t+1} + \gamma V(S_{t+1}) = 3 + 0.9 \times 8 = 3 + 7.2 = 10.2
$$

**Step 2: Compute TD error**
$$
\delta_t = 10.2 - 10 = 0.2
$$

**Step 3: Update value**
$$
V(S_t) \leftarrow 10 + 0.1 \times 0.2 = 10 + 0.02 = 10.02
$$

---

## Handling Terminal States

When $S_{t+1}$ is terminal, there is no future value:

$$
V(S_t) \leftarrow V(S_t) + \alpha[R_{t+1} - V(S_t)]
$$

The target is just $R_{t+1}$, with $V(\text{terminal}) = 0$.

**Example:** Agent reaches goal with $R = 100$, current $V(s) = 80$:
$$
V(s) \leftarrow 80 + 0.1 \times (100 - 80) = 82
$$

---

## Multi-Step TD: n-Step Returns

TD(0) uses a 1-step return. We can extend to n-step returns:

**1-step (TD(0)):**
$$
G_t^{(1)} = R_{t+1} + \gamma V(S_{t+1})
$$

**2-step:**
$$
G_t^{(2)} = R_{t+1} + \gamma R_{t+2} + \gamma^2 V(S_{t+2})
$$

**n-step:**
$$
G_t^{(n)} = R_{t+1} + \gamma R_{t+2} + ... + \gamma^{n-1} R_{t+n} + \gamma^n V(S_{t+n})
$$

**$\infty$-step (Monte Carlo):**
$$
G_t^{(\infty)} = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + ...
$$

---

## TD($\lambda$): Eligibility Traces

TD($\lambda$) combines multiple n-step returns using a weighted average:

$$
G_t^\lambda = (1 - \lambda) \sum_{n=1}^{\infty} \lambda^{n-1} G_t^{(n)}
$$

**$\lambda = 0$:** Pure TD(0), one-step updates

**$\lambda = 1$:** Pure Monte Carlo, full returns

**$\lambda \in (0, 1)$:** Blend of short and long-term estimates

---

## Bias-Variance Tradeoff

**Monte Carlo (no bootstrapping):**
- Unbiased: Uses actual returns
- High variance: Returns vary significantly

**TD (bootstrapping):**
- Biased: Uses estimates that may be wrong
- Lower variance: Less affected by later random events

**n-step TD:**
- Larger n: More variance, less bias
- Smaller n: Less variance, more bias

The optimal choice depends on the problem.

---

## Why TD Often Works Better

Despite being biased, TD often outperforms Monte Carlo because:

**1. Lower variance leads to faster convergence with limited data**

**2. Updates happen more frequently (every step vs every episode)**

**3. Works for continuing tasks without natural episodes**

**4. Can learn during episodes, not just after**

---

## Convergence

TD(0) converges to $V^\pi$ under standard conditions:

**1. Learning rates satisfy:**
$$
\sum_t \alpha_t = \infty, \quad \sum_t \alpha_t^2 < \infty
$$

**2. All states visited infinitely often**

**3. The MDP is finite**

In practice, constant small learning rates work well.

---

## The Random Walk Example

**Setup:** 5 states A-B-C-D-E with terminal states at ends. Start in C.

**True values (under random policy):**
$V(A) = 1/6$, $V(B) = 2/6$, $V(C) = 3/6$, $V(D) = 4/6$, $V(E) = 5/6$

**TD learning:**
- After each step, update based on next state's estimate
- Gradually propagates correct values from terminal states

**Monte Carlo:**
- Must wait for episode to end
- Updates based on actual outcome (0 or 1)

TD converges faster in this example.

---

## TD Error as Prediction Error

The TD error $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$ represents:

**Prediction error:** Difference between predicted value and observed outcome (immediate reward plus estimated continuation)

**Learning signal:** Used to adjust predictions

**Neuroscience connection:** TD error resembles dopamine signals in the brain, which encode reward prediction errors.

---

## Online vs Batch TD

**Online TD:**
- Update after each transition
- Standard approach

**Batch TD:**
- Collect many transitions
- Update repeatedly until convergence
- Can be more stable

**Experience replay (as in DQN):**
- Store transitions in buffer
- Sample batches for updates
- Combines benefits of both

---

## TD for Control

TD methods extend to action-value functions for control:

**SARSA (on-policy):**
$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha[R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)]
$$

**Q-learning (off-policy):**
$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha[R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t)]
$$

---

## Advantages of TD Learning

**1. Online learning:** Updates after each step

**2. Model-free:** No environment model needed

**3. Works for continuing tasks:** Does not require episodes

**4. Lower variance:** More stable than Monte Carlo

**5. Foundation for many algorithms:** Q-learning, SARSA, actor-critic

---

## Disadvantages of TD Learning

**1. Biased:** Estimates may be systematically wrong initially

**2. Sensitive to initial values:** Bad initialization can slow learning

**3. Sensitive to learning rate:** Too high causes instability

**4. Can be slow to propagate values:** Information moves one step at a time

---

## Summary: TD vs MC vs DP

**Dynamic Programming:**
- Full model required
- Computes exact values
- Not sample-based

**Monte Carlo:**
- Model-free, sample-based
- Unbiased but high variance
- Episode-based updates

**Temporal Difference:**
- Model-free, sample-based
- Biased but lower variance
- Step-based updates, bootstrapping
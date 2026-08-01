## What Is Q-Learning?

Q-learning is a **model-free, off-policy** reinforcement learning algorithm that learns the optimal action-value function $Q^*(s, a)$ directly from experience.

It learns which action to take in each state to maximize cumulative reward, without needing a model of the environment.

Introduced by Christopher Watkins in 1989, Q-learning is one of the most important algorithms in RL.

---

## The Q-Function

The action-value function (Q-function) represents the expected return from taking action $a$ in state $s$ and then following policy $\pi$:

$$
Q^\pi(s, a) = E_\pi\left[\sum_{k=0}^{\infty} \gamma^k R_{t+k+1} \Big| S_t = s, A_t = a\right]
$$

The **optimal** Q-function $Q^*(s, a)$ gives the maximum expected return:

$$
Q^*(s, a) = \max_\pi Q^\pi(s, a)
$$

---

## The Bellman Optimality Equation

The optimal Q-function satisfies the Bellman optimality equation:

$$
Q^*(s, a) = E\left[R_{t+1} + \gamma \max_{a'} Q^*(S_{t+1}, a') \Big| S_t = s, A_t = a\right]
$$

This says: the value of taking action $a$ in state $s$ equals the immediate reward plus the discounted value of the best action in the next state.

Q-learning iteratively approximates this equation.

---

## The Q-Learning Update Rule

After observing transition $(s, a, r, s')$:

$$
Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]
$$

**Components:**
- $Q(s, a)$: Current Q-value estimate
- $\alpha$: Learning rate
- $r$: Observed reward
- $\gamma$: Discount factor
- $\max_{a'} Q(s', a')$: Estimated value of best action in next state
- $r + \gamma \max_{a'} Q(s', a')$: TD target
- $r + \gamma \max_{a'} Q(s', a') - Q(s, a)$: TD error

---

## Understanding the Update

The update moves $Q(s, a)$ toward a better estimate:

$$
Q_{new} = Q_{old} + \alpha \cdot (\text{target} - Q_{old})
$$

**If target > $Q_{old}$:** The action was better than expected, increase Q-value

**If target < $Q_{old}$:** The action was worse than expected, decrease Q-value

**If target = $Q_{old}$:** Q-value is already accurate, no change

---

## The TD Error

The temporal difference (TD) error is:

$$
\delta_t = R_{t+1} + \gamma \max_{a'} Q(S_{t+1}, a') - Q(S_t, A_t)
$$

This measures the difference between:
- The new estimate: $R_{t+1} + \gamma \max_{a'} Q(S_{t+1}, a')$
- The old estimate: $Q(S_t, A_t)$

The TD error drives learning. Large errors mean our estimate was wrong.

---

## Worked Example

**Setup:**
- Current state: $s$, Action taken: $a$
- Current Q-value: $Q(s, a) = 5.0$
- Observed reward: $r = 2$
- Next state: $s'$
- Q-values at $s'$: $Q(s', a_1) = 3$, $Q(s', a_2) = 7$, $Q(s', a_3) = 4$
- Learning rate: $\alpha = 0.1$
- Discount factor: $\gamma = 0.9$

**Step 1: Find max Q-value at next state**

$$
\max_{a'} Q(s', a') = \max(3, 7, 4) = 7
$$

**Step 2: Compute TD target**

$$
\text{target} = r + \gamma \max_{a'} Q(s', a') = 2 + 0.9 \times 7 = 2 + 6.3 = 8.3
$$

**Step 3: Compute TD error**

$$
\delta = 8.3 - 5.0 = 3.3
$$

**Step 4: Update Q-value**

$$
Q(s, a) \leftarrow 5.0 + 0.1 \times 3.3 = 5.0 + 0.33 = 5.33
$$

---

## Terminal States

When $s'$ is a terminal state, there is no future reward:

$$
Q(s, a) \leftarrow Q(s, a) + \alpha \left[ r - Q(s, a) \right]
$$

The target is just the immediate reward $r$, with no bootstrap term.

**Example:** If reaching goal gives $r = 10$ and $Q(s, a) = 8$:

$$
Q(s, a) \leftarrow 8 + 0.1 \times (10 - 8) = 8.2
$$

---

## Off-Policy Learning

Q-learning is **off-policy**: it learns the optimal policy $\pi^*$ regardless of the policy used to collect data.

**Behavior policy:** The policy used to select actions (often epsilon-greedy for exploration)

**Target policy:** The policy being learned (greedy with respect to Q)

The update uses $\max_{a'} Q(s', a')$, which corresponds to the greedy policy, not the action actually taken.

---

## Q-Learning Algorithm

**Initialize:** $Q(s, a)$ arbitrarily for all $s, a$

**Repeat for each episode:**

1. Initialize state $s$

2. **Repeat for each step:**
   - Choose action $a$ from $s$ using policy derived from $Q$ (e.g., epsilon-greedy)
   - Take action $a$, observe reward $r$ and next state $s'$
   - Update: $Q(s, a) \leftarrow Q(s, a) + \alpha[r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$
   - $s \leftarrow s'$

3. Until $s$ is terminal

---

## Convergence Conditions

Q-learning converges to $Q^*$ under these conditions:

**1. All state-action pairs visited infinitely often**

Exploration must cover the entire space.

**2. Learning rate satisfies:**

$$
\sum_t \alpha_t = \infty \quad \text{and} \quad \sum_t \alpha_t^2 < \infty
$$

Example: $\alpha_t = 1/t$ satisfies this.

**3. Rewards are bounded**

Finite rewards ensure finite Q-values.

In practice, constant small learning rates work well.

---

## Learning Rate

**High $\alpha$ (e.g., 0.5):**
- Fast initial learning
- May oscillate, not converge
- Good for non-stationary environments

**Low $\alpha$ (e.g., 0.01):**
- Slow, stable learning
- Better convergence guarantees
- May be too slow in practice

**Typical values:** $\alpha \in [0.01, 0.5]$

A common choice is $\alpha = 0.1$.

---

## Discount Factor

**$\gamma = 0$:**
- Only immediate rewards matter
- Myopic behavior

**$\gamma$ close to 1 (e.g., 0.99):**
- Future rewards almost as important as immediate
- Longer planning horizon
- Can be unstable

**$\gamma = 1$:**
- Undiscounted, only for episodic tasks
- Total reward matters equally at all times

**Typical values:** $\gamma \in [0.9, 0.99]$

---

## Q-Learning vs SARSA

**Q-Learning (off-policy):**

$$
Q(s, a) \leftarrow Q(s, a) + \alpha[r + \gamma \max_{a'} Q(s', a') - Q(s, a)]
$$
Uses max over next actions (greedy target).

**SARSA (on-policy):**

$$
Q(s, a) \leftarrow Q(s, a) + \alpha[r + \gamma Q(s', a') - Q(s, a)]
$$
Uses the actual next action $a'$ taken.

Q-learning learns optimal policy; SARSA learns policy being followed.

---

## Cliff Walking Example

In the cliff walking problem:

**Q-Learning:** Learns the optimal path (along the cliff edge) because it evaluates the greedy policy. Risky during exploration.

**SARSA:** Learns a safer path (away from cliff) because it accounts for exploration in its value estimates.

This illustrates the practical difference between on-policy and off-policy learning.

---

## The Maximization Bias Problem

Q-learning can overestimate Q-values due to the max operator:

$$
E[\max_a Q(s, a)] \geq \max_a E[Q(s, a)]
$$

When Q-values are noisy, taking the max tends to select overestimated values.

**Solution: Double Q-Learning**

Use two Q-functions, one to select the action, another to evaluate:

$$
Q_1(s, a) \leftarrow Q_1(s, a) + \alpha[r + \gamma Q_2(s', \arg\max_{a'} Q_1(s', a')) - Q_1(s, a)]
$$

---

## Tabular vs Function Approximation

**Tabular Q-Learning:**
- Stores Q-values in a table
- Works for small, discrete state spaces
- Exact representation

**Q-Learning with Function Approximation:**
- Uses neural network: $Q(s, a; \theta)$
- Handles large/continuous state spaces
- Examples: DQN, Double DQN

The update becomes gradient descent on the TD error.

---

## Exploration Strategies

Q-learning needs exploration to visit all state-action pairs:

**Epsilon-greedy:** Random action with probability $\epsilon$

**Optimistic initialization:** Initialize Q-values high to encourage exploration

**UCB:** Add exploration bonus based on visit counts

**Boltzmann exploration:** Action probability proportional to Q-value

---

## Common Pitfalls

**1. Insufficient exploration:**
- Not all state-action pairs visited
- Policy may be suboptimal

**2. Learning rate too high:**
- Q-values oscillate
- No convergence

**3. Forgetting to handle terminal states:**
- No max term for terminal states

**4. Using Q-learning when on-policy is better:**
- Sometimes SARSA is more appropriate (safer policies)
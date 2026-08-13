# <span style="font-size: 20px;">Vanishing Gradient Simulation</span>

<span style="font-size: 14px;">The vanishing gradient problem is the central failure mode that limits Vanilla RNNs from learning long-range dependencies. When gradients propagate backward through many time steps during Backpropagation Through Time (BPTT), they involve repeated multiplication by the recurrent weight matrix $W_{hh}$. The spectral norm of this matrix -- its largest singular value -- determines whether gradients decay to zero, explode to infinity, or remain stable.</span>

---

## <span style="font-size: 16px;">What It Is</span>

<span style="font-size: 14px;">In a Vanilla RNN, the hidden state at time $t$ is computed as $h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b)$. During training, the loss $L$ is computed at the final time step (or accumulated across steps), and gradients must flow backward through the entire sequence. To update parameters based on information from early time steps, the gradient of the loss with respect to an early hidden state $h_0$ must pass through every intermediate time step.</span>

<span style="font-size: 14px;">This backward pass involves a chain of matrix multiplications. At each step, the gradient is multiplied by the Jacobian of the hidden state transition, which in a simplified model reduces to multiplication by $W_{hh}$. Over $T$ steps, the gradient accumulates $T$ such multiplications. The behavior of this repeated multiplication is entirely governed by the spectral properties of $W_{hh}$.</span>

<span style="font-size: 14px;">This problem demonstrates that behavior in its purest form: starting from gradient norm $1.0$ at the current time step, compute what happens to the gradient norm at each of $T$ backward steps. The result reveals whether the network can propagate useful gradient information across the full sequence or whether the signal is destroyed long before it reaches the earliest time steps.</span>

---

## <span style="font-size: 16px;">Key Equations</span>

<span style="font-size: 14px;">The gradient of the loss with respect to an early hidden state $h_k$ depends on the gradient at the final step $h_T$ through the chain rule:</span>

$$
\frac{\partial L}{\partial h_k} = \frac{\partial L}{\partial h_T} \prod_{t=k+1}^{T} \frac{\partial h_t}{\partial h_{t-1}}
$$

<span style="font-size: 14px;">In the simplified model where the tanh derivative is approximately $1$, each Jacobian $\frac{\partial h_t}{\partial h_{t-1}}$ reduces to $W_{hh}$. The product becomes:</span>

$$
\prod_{t=k+1}^{T} \frac{\partial h_t}{\partial h_{t-1}} \approx W_{hh}^{T-k}
$$

<span style="font-size: 14px;">Taking the norm of both sides:</span>

$$
\left\|\frac{\partial L}{\partial h_k}\right\| \propto \|W_{hh}\|_2^{\,T-k}
$$

<span style="font-size: 14px;">where $\|W_{hh}\|_2$ is the **spectral norm** -- the largest singular value. Starting from norm $1.0$ and propagating backward through $T$ steps, the gradient norm at step $i$ is:</span>

$$
g_i = \|W_{hh}\|_2^{\,i}
$$

---

## <span style="font-size: 16px;">The Spectral Norm</span>

<span style="font-size: 14px;">The spectral norm of a matrix $A$ is defined as its largest singular value, denoted $\sigma_1(A)$ or $\|A\|_2$. It has a precise geometric meaning: the maximum factor by which $A$ can stretch any unit vector.</span>

$$
\|A\|_2 = \max_{\|v\| = 1} \|Av\| = \sigma_1(A)
$$

<span style="font-size: 14px;">To compute the spectral norm, perform a Singular Value Decomposition (SVD) of $W_{hh} = U \Sigma V^T$, where $\Sigma$ contains singular values $\sigma_1 \geq \sigma_2 \geq \ldots \geq \sigma_n \geq 0$. The spectral norm is $\sigma_1$, the largest entry.</span>

<span style="font-size: 14px;">The spectral norm governs the worst-case behavior of repeated multiplication. When the gradient vector is multiplied by $W_{hh}$ repeatedly, the component aligned with the top singular vector gets scaled by $\sigma_1$ at each step. After $T$ multiplications, the gradient norm scales as $\sigma_1^T$.</span>

<span style="font-size: 14px;">The spectral norm is distinct from the **Frobenius norm** $\|A\|_F = \sqrt{\sum_{i,j} A_{ij}^2}$, which measures total matrix magnitude but does not predict gradient behavior under repeated multiplication. A matrix can have a large Frobenius norm but spectral norm less than $1$, leading to vanishing gradients despite the matrix "looking large."</span>

---

## <span style="font-size: 16px;">Three Regimes</span>

<span style="font-size: 14px;">The value of $\|W_{hh}\|_2$ relative to $1$ determines which of three qualitatively different regimes the gradient falls into.</span>

<span style="font-size: 14px;">**Vanishing ($\|W_{hh}\|_2 < 1$).** Each backward step shrinks the gradient. With $\sigma_1 = 0.8$ and $T = 10$: the gradient norms are $[0.8, 0.64, 0.512, 0.4096, 0.3277, 0.2621, 0.2097, 0.1678, 0.1342, 0.1074]$. By step 10, the gradient retains roughly $10\%$ of its original magnitude. By step 50, it would be $0.8^{50} \approx 1.4 \times 10^{-5}$ -- effectively zero.</span>

<span style="font-size: 14px;">**Stable ($\|W_{hh}\|_2 = 1$).** The gradient norm remains constant: $1^T = 1$ for all $T$. Every time step contributes equally to learning regardless of sequence length. Achieving this requires explicit constraints such as orthogonal initialization or spectral normalization.</span>

<span style="font-size: 14px;">**Exploding ($\|W_{hh}\|_2 > 1$).** Each backward step amplifies the gradient. With $\sigma_1 = 1.2$ and $T = 10$: the gradient norms are $[1.2, 1.44, 1.728, 2.0736, 2.4883, 2.9860, 3.5832, 4.2998, 5.1598, 6.1917]$. The gradient grows over $6\times$ in 10 steps. For $T = 100$, it would reach $1.2^{100} \approx 8.3 \times 10^7$.</span>

---

## <span style="font-size: 16px;">Why This Matters</span>

<span style="font-size: 14px;">**Long-range dependencies become invisible.** Consider a language model processing "The cat, which sat on the mat near the door by the window, was sleeping." The subject "cat" and verb "was" are separated by many tokens. If gradients vanish over that distance, the model receives no learning signal connecting the verb's error back to the subject's representation. The model learns only short-range patterns.</span>

<span style="font-size: 14px;">**Training appears to converge but the model is shallow.** Vanishing gradients do not cause training to crash. The model still learns local patterns (bigrams, trigrams) because those involve short gradient paths. The loss decreases and metrics improve, but the model never captures long-range structure. This makes vanishing gradients harder to diagnose than exploding gradients, which produce obvious numerical failures.</span>

<span style="font-size: 14px;">**Exploding gradients destabilize training.** Large gradients cause large parameter updates, shifting the loss landscape dramatically. The next forward pass produces very different activations, leading to even larger gradients. This positive feedback loop causes the loss to spike, oscillate, or diverge. NaN values in parameters are a typical symptom.</span>

---

## <span style="font-size: 16px;">The Exponential Nature</span>

<span style="font-size: 14px;">Even small deviations from spectral norm $1$ compound rapidly. This is not gradual degradation -- it is exponential, and exponentials are deceptively fast.</span>

<span style="font-size: 14px;">A spectral norm of $0.9$ -- only $10\%$ below the stable threshold -- yields: $0.9^{10} \approx 0.349$, $0.9^{50} \approx 0.00515$, $0.9^{100} \approx 2.66 \times 10^{-5}$. A sequence length of $100$ tokens is routine in NLP, yet even this "almost stable" spectral norm destroys gradient information completely.</span>

<span style="font-size: 14px;">The same exponential works in reverse. A spectral norm of $1.1$ yields: $1.1^{10} \approx 2.594$, $1.1^{50} \approx 117.4$, $1.1^{100} \approx 13{,}781$. The gradient is amplified by nearly $14{,}000$ over $100$ steps.</span>

<span style="font-size: 14px;">This exponential sensitivity explains why Vanilla RNNs fail on any task requiring memory beyond $10$-$20$ time steps. The spectral norm would need to be maintained at exactly $1.0$ throughout training, but gradient descent has no mechanism to enforce this constraint. As weights update, the spectral norm drifts, and the exponential takes over.</span>

---

## <span style="font-size: 16px;">Paper Context</span>

<span style="font-size: 14px;">The vanishing gradient problem was formally identified in two foundational works. Sepp Hochreiter's 1991 diploma thesis first demonstrated that gradient flow in recurrent networks is fundamentally unstable, showing that error signals flowing backward in time either shrink or grow exponentially.</span>

<span style="font-size: 14px;">Bengio, Simard, and Frasconi formalized this in their 1994 paper "Learning Long-Term Dependencies with Gradient Descent is Difficult." They proved that for recurrent networks with bounded weights, the gradient must either vanish or explode exponentially with temporal distance. The paper states: "The influence of a given input on the hidden layer, and therefore on the network output, either decays or blows up exponentially as it cycles around the network's recurrent connections." This is a mathematical inevitability for networks that propagate gradients through repeated matrix multiplication.</span>

<span style="font-size: 14px;">Bengio et al. demonstrated that the problem is not specific to any activation function or training algorithm. As long as the network relies on multiplying Jacobians through time, the exponential dynamics are unavoidable. The only escape is to change the architecture -- to create paths through which gradients flow without repeated multiplication by the same matrix.</span>

<span style="font-size: 14px;">This analysis directly motivated the Long Short-Term Memory (LSTM) by Hochreiter and Schmidhuber (1997). The LSTM's cell state with additive updates controlled by gates creates a gradient highway through time. The forget gate, when close to $1$, allows the gradient to pass through nearly unchanged: $\frac{\partial c_t}{\partial c_{t-1}} = f_t$, replacing the problematic $W_{hh}^T$ with scalar gate values and breaking the exponential decay.</span>

---

## <span style="font-size: 16px;">Numerical Example</span>

<span style="font-size: 14px;">Consider $T = 10$ time steps with three different spectral norms: $0.8$, $1.0$, and $1.2$. Starting from gradient norm $1.0$, the gradient norm at step $i$ is $\sigma_1^i$.</span>

<span style="font-size: 14px;">**Spectral norm = 0.8 (vanishing):**</span>

<span style="font-size: 14px;">Step 1: $0.8^1 = 0.8000$. Step 2: $0.8^2 = 0.6400$. Step 3: $0.8^3 = 0.5120$. Step 4: $0.8^4 = 0.4096$. Step 5: $0.8^5 = 0.3277$. Step 6: $0.8^6 = 0.2621$. Step 7: $0.8^7 = 0.2097$. Step 8: $0.8^8 = 0.1678$. Step 9: $0.8^9 = 0.1342$. Step 10: $0.8^{10} = 0.1074$.</span>

<span style="font-size: 14px;">**Spectral norm = 1.0 (stable):**</span>

<span style="font-size: 14px;">All $10$ steps produce gradient norm $1.0$. Every time step contributes equally to learning.</span>

<span style="font-size: 14px;">**Spectral norm = 1.2 (exploding):**</span>

<span style="font-size: 14px;">Step 1: $1.2^1 = 1.2000$. Step 2: $1.2^2 = 1.4400$. Step 3: $1.2^3 = 1.7280$. Step 4: $1.2^4 = 2.0736$. Step 5: $1.2^5 = 2.4883$. Step 6: $1.2^6 = 2.9860$. Step 7: $1.2^7 = 3.5832$. Step 8: $1.2^8 = 4.2998$. Step 9: $1.2^9 = 5.1598$. Step 10: $1.2^{10} = 6.1917$.</span>

<span style="font-size: 14px;">The contrast is stark: after $10$ steps, the vanishing case retains $10.7\%$ of the gradient while the exploding case has amplified it to $619\%$. Extend to $T = 50$: $0.8^{50} \approx 1.4 \times 10^{-5}$ versus $1.2^{50} \approx 9100$. The divergence between regimes grows dramatically with sequence length.</span>

---

## <span style="font-size: 16px;">Solutions</span>

<span style="font-size: 14px;">**LSTM constant error carousel.** The LSTM cell state uses additive updates: $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$. The gradient of $c_t$ with respect to $c_{t-1}$ is $f_t$ (element-wise), not a full matrix multiplication. When the forget gate is near $1$, the gradient passes through almost unchanged, creating a "constant error carousel" that does not suffer from exponential decay.</span>

<span style="font-size: 14px;">**GRU gating.** The Gated Recurrent Unit (Cho et al., 2014) uses the update gate $z_t$ to interpolate: $h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$. When $z_t \approx 0$, $h_t \approx h_{t-1}$ and the gradient flows through unchanged. The GRU merges forget and input gates into one, reducing parameters while still providing gradient-stable paths.</span>

<span style="font-size: 14px;">**Gradient clipping.** Pascanu, Mikolov, and Bengio (2013) proposed clipping the gradient norm to a threshold $\tau$: if $\|g\| > \tau$, replace $g$ with $\tau \cdot g / \|g\|$. This handles exploding gradients by capping update magnitudes. It does nothing for vanishing gradients -- a gradient already near zero cannot be helped by clipping.</span>

<span style="font-size: 14px;">**Orthogonal initialization and residual connections.** Initializing $W_{hh}$ as an orthogonal matrix ensures spectral norm $1$ at the start of training. Residual connections ($y = x + f(x)$) in stacked RNNs provide skip paths with an identity gradient term, preventing complete vanishing across layers.</span>

---

## <span style="font-size: 16px;">Pitfalls</span>

* <span style="font-size: 14px;">**Confusing spectral norm with Frobenius norm.** The Frobenius norm $\|A\|_F = \sqrt{\sum_{ij} A_{ij}^2}$ measures overall matrix magnitude but does not predict gradient behavior under repeated multiplication. A $100 \times 100$ matrix with all singular values equal to $0.5$ has Frobenius norm $5.0$ but spectral norm $0.5$, and gradients vanish. The spectral norm is the correct quantity because it captures the multiplicative growth rate.</span>

* <span style="font-size: 14px;">**Forgetting that tanh derivative further reduces the gradient.** The simplified model ignores the activation function. In practice, each backward step multiplies by $\text{diag}(\tanh'(z_t)) \cdot W_{hh}$, where $\tanh'(z) = 1 - \tanh^2(z) \in (0, 1]$. The effective spectral norm per step is strictly less than $\|W_{hh}\|_2$. Vanishing is worse in practice than the formula suggests.</span>

* <span style="font-size: 14px;">**Assuming gradient clipping solves vanishing gradients.** Clipping prevents norms from exceeding a threshold, handling explosions. It does not amplify small gradients. If the spectral norm is $0.9$ and gradients have decayed to $10^{-5}$ after $100$ steps, clipping does nothing. Solving vanishing gradients requires architectural changes, not clipping.</span>

* <span style="font-size: 14px;">**Ignoring that this is a simplified model.** The formula $g_i = \sigma_1^i$ assumes the same $W_{hh}$ at every step, no activation derivative, and alignment with the top singular vector. In a real network, the tanh derivative varies by time step and the gradient direction rotates. The simplified model captures qualitative behavior but the exact rate differs in practice.</span>

* <span style="font-size: 14px;">**Initializing LSTM forget gate bias at zero.** When using an LSTM to solve vanishing gradients, initializing the forget gate bias at $0$ gives $\sigma(0) = 0.5$, halving the cell state at every step -- itself a form of vanishing gradient with rate $0.5^T$. Best practice (Gers et al., 2000) is to initialize the bias to $1$ or higher so $\sigma(1) \approx 0.73$, biasing toward retention.</span>

* <span style="font-size: 14px;">**Conflating vanishing gradients with zero gradients.** Vanishing gradients are not literally zero -- they are exponentially small. A gradient of $10^{-15}$ is technically nonzero but in float32 is indistinguishable from zero. The practical threshold depends on precision and the optimizer: in float32 with Adam's epsilon of $10^{-8}$, gradients below roughly $10^{-7}$ contribute nothing to updates.</span>

---
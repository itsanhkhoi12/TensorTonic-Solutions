# <span style="font-size: 20px;">SGNS Gradient Step</span>

<span style="font-size: 14px;">Skip-gram with Negative Sampling (SGNS) is the workhorse training objective behind Word2Vec (Mikolov et al., 2013). Instead of a full softmax over the vocabulary, it trains two embedding matrices by treating each (center, context) pair as a binary classification problem against a handful of sampled negative words. This problem implements one full stochastic gradient descent (SGD) step of that objective, computing the gradients by hand and updating both matrices.</span>

---

## <span style="font-size: 16px;">The SGNS Objective</span>

<span style="font-size: 14px;">Word2Vec keeps two embeddings per word: an **input** (center) vector in $W_{in}$ and an **output** (context) vector in $W_{out}$. For a center word $c$ and an observed context word $o$, the model maximizes the probability that the pair is real, while pushing down the probability that $k$ randomly sampled negative words $n_1, \ldots, n_k$ are real neighbors of $c$.</span>

<span style="font-size: 14px;">Writing $v_c = W_{in}[c]$ and $u_w = W_{out}[w]$, the per-example loss for a single (center, positive) pair with its negatives is:</span>

$$
L = -\log \sigma(v_c \cdot u_o) - \sum_{i=1}^{k} \log \sigma(-\,v_c \cdot u_{n_i})
$$

<span style="font-size: 14px;">where $\sigma(x) = 1 / (1 + e^{-x})$ is the logistic sigmoid. The first term rewards a high dot product between the center and the true context. Each negative term rewards a **low** dot product between the center and a sampled non-neighbor, since $\sigma(-x) = 1 - \sigma(x)$.</span>

---

## <span style="font-size: 16px;">From Softmax to Binary Classification</span>

<span style="font-size: 14px;">The original Skip-gram model defined $p(o \mid c)$ with a softmax over the entire vocabulary. Computing that normalizer and its gradient costs $O(V)$ per step, which is prohibitive for vocabularies of millions of words. The Word2Vec paper introduces negative sampling as a cheap approximation:</span>

* <span style="font-size: 14px;">Treat the real pair $(c, o)$ as a positive example with label $1$.</span>
* <span style="font-size: 14px;">Draw $k$ negative words from a noise distribution (the paper uses the unigram distribution raised to the $3/4$ power) and label them $0$.</span>
* <span style="font-size: 14px;">Run a logistic regression that distinguishes the real context from the noise.</span>

<span style="font-size: 14px;">This turns one expensive $O(V)$ softmax into $k + 1$ cheap logistic terms, where $k$ is typically $5$ to $20$ for small datasets and $2$ to $5$ for large ones. The paper reports that this both speeds training and improves the quality of frequent-word representations.</span>

---

## <span style="font-size: 16px;">Deriving the Gradients</span>

<span style="font-size: 14px;">The gradient of the loss decomposes neatly because of the sigmoid derivative $\sigma'(x) = \sigma(x)(1 - \sigma(x))$ and the chain rule. The single most useful fact is that the gradient of $-\log \sigma(s)$ with respect to the score $s$ is $\sigma(s) - 1$, and the gradient of $-\log \sigma(-s)$ with respect to $s$ is $\sigma(s)$.</span>

<span style="font-size: 14px;">Define the scores $s_o = v_c \cdot u_o$ and $s_i = v_c \cdot u_{n_i}$. Then the gradients are:</span>

$$
\frac{\partial L}{\partial u_o} = (\sigma(s_o) - 1)\, v_c
$$

$$
\frac{\partial L}{\partial u_{n_i}} = \sigma(s_i)\, v_c
$$

$$
\frac{\partial L}{\partial v_c} = (\sigma(s_o) - 1)\, u_o + \sum_{i=1}^{k} \sigma(s_i)\, u_{n_i}
$$

<span style="font-size: 14px;">A clean way to read this: every word $w$ involved in the step has a **target label** $t_w$ (the positive context has $t = 1$, every negative has $t = 0$). The shared structure is that each gradient is a coefficient $(\sigma(\text{score}) - t)$ times the other matrix's vector. This is exactly the gradient of logistic regression, where $(\hat{y} - y)$ multiplies the input features.</span>

---

## <span style="font-size: 16px;">Shared Structure with Logistic Regression</span>

<span style="font-size: 14px;">The coefficient $(\sigma(s) - t)$ is the prediction error of a binary classifier. For the positive word the target is $1$, so the coefficient $\sigma(s_o) - 1$ is negative whenever the model is not yet confident, pulling $u_o$ and $v_c$ toward each other. For a negative word the target is $0$, so the coefficient $\sigma(s_i)$ is positive, pushing $u_{n_i}$ and $v_c$ apart. The magnitude of each update is proportional to how wrong the current prediction is, which is the same self-correcting behavior as ordinary logistic regression.</span>

<span style="font-size: 14px;">This is why SGNS embeddings end up encoding co-occurrence statistics. Levy and Goldberg (2014) later showed that SGNS implicitly factorizes a shifted pointwise mutual information matrix, which explains why the learned vectors capture semantic and syntactic regularities.</span>

---

## <span style="font-size: 16px;">The SGD Update</span>

<span style="font-size: 14px;">SGD moves each parameter a small step in the direction that decreases the loss. With learning rate $\eta$ (lr), the updates are:</span>

$$
u_o \leftarrow u_o - \eta\, (\sigma(s_o) - 1)\, v_c
$$

$$
u_{n_i} \leftarrow u_{n_i} - \eta\, \sigma(s_i)\, v_c
$$

$$
v_c \leftarrow v_c - \eta\, \Big[(\sigma(s_o) - 1)\, u_o + \sum_{i=1}^{k} \sigma(s_i)\, u_{n_i}\Big]
$$

<span style="font-size: 14px;">Only the rows touched by this step change: the single center row of $W_{in}$, and the $k + 1$ rows of $W_{out}$ for the positive and negative words. Every other row is untouched. This sparsity is what makes SGNS so fast: each step is $O((k + 1) \cdot D)$ where $D$ is the embedding dimension, independent of vocabulary size.</span>

---

## <span style="font-size: 16px;">Why Compute All Gradients Before Applying</span>

<span style="font-size: 14px;">The gradients for $v_c$ depend on the **pre-update** output vectors $u_o$ and $u_{n_i}$, and the gradients for those output vectors depend on the **pre-update** center vector $v_c$. If the center vector is updated first and then reused to compute the output gradients, the output updates would be based on a value that no longer matches the math. The correct procedure is:</span>

* <span style="font-size: 14px;">Snapshot $v_c$ and read all output vectors.</span>
* <span style="font-size: 14px;">Compute every gradient using these original values.</span>
* <span style="font-size: 14px;">Only then apply all updates.</span>

<span style="font-size: 14px;">This is the standard convention for a single synchronous gradient step. In a naive in-place implementation that updates $W_{in}[c]$ before computing the $W_{out}$ gradients, the results drift, especially with large learning rates where the mutated value differs substantially from the original.</span>

---

## <span style="font-size: 16px;">Input and Output Matrices Both Update</span>

<span style="font-size: 14px;">A common point of confusion is that Word2Vec maintains two separate embedding tables. Both are trainable and both receive gradients on every step:</span>

* <span style="font-size: 14px;">$W_{in}$ holds the **center** (input) vectors. After training, these are usually the embeddings exported and used downstream.</span>
* <span style="font-size: 14px;">$W_{out}$ holds the **context** (output) vectors, used only as the second half of each dot product during training.</span>

<span style="font-size: 14px;">Some practitioners average the two tables or sum them; the paper itself keeps the input matrix as the final word vectors. Regardless of which is exported, both must be updated during training, since the objective is symmetric in the dot product $v_c \cdot u_w$.</span>

---

## <span style="font-size: 16px;">The Role of the Learning Rate</span>

<span style="font-size: 14px;">The learning rate $\eta$ scales the size of each step. Word2Vec uses a linearly decaying schedule, starting around $0.025$ and shrinking toward zero as training progresses. A larger $\eta$ makes faster initial progress but risks overshooting and oscillation; a smaller $\eta$ is stable but slow. Because SGNS updates are sparse and frequent, even a modest learning rate accumulates into large total movement over a corpus of billions of tokens.</span>

<span style="font-size: 14px;">Because the gradient coefficients $(\sigma(s) - t)$ are bounded in $[-1, 1]$, a single SGNS step can never move a row by more than $\eta$ times the magnitude of the partner vector. This built-in bound is one reason SGNS is stable even without gradient clipping. When the model is confident and correct (the positive score is large and positive, the negative scores are large and negative), all coefficients approach zero and the row stops moving, which is the natural convergence signal for that pair.</span>

---

## <span style="font-size: 16px;">The Noise Distribution and Choice of $k$</span>

<span style="font-size: 14px;">In a full training loop the negative ids are sampled, not given. Word2Vec draws them from a unigram distribution raised to the $3/4$ power, $P(w) \propto f(w)^{3/4}$, where $f(w)$ is the corpus frequency of word $w$. Raising to $3/4$ flattens the distribution: it samples rare words more often than their raw frequency would, and very frequent words slightly less often, which the paper found gives better embeddings than either the plain unigram or the uniform distribution.</span>

<span style="font-size: 14px;">The number of negatives $k$ trades quality against speed:</span>

* <span style="font-size: 14px;">Small corpora benefit from $k$ in the range $5$ to $20$, giving each positive pair a stronger contrastive signal.</span>
* <span style="font-size: 14px;">Large corpora can use $k$ as small as $2$ to $5$, since the sheer number of updates compensates.</span>

<span style="font-size: 14px;">This problem fixes the negative ids in each test case so the step is deterministic and checkable, but the gradient math is identical regardless of how the negatives were chosen. A negative id may coincide with the positive id or repeat within the list; in that case the gradient contributions accumulate on the shared output row rather than overwriting one another.</span>

---

## <span style="font-size: 16px;">Comparison with Autograd</span>

<span style="font-size: 14px;">Modern frameworks would express this loss and call backward(), letting reverse-mode automatic differentiation compute the same gradients. Implementing the closed form by hand is valuable for understanding because:</span>

* <span style="font-size: 14px;">The manual gradient is exactly what autograd produces; verifying them against each other is a standard sanity check.</span>
* <span style="font-size: 14px;">The original Word2Vec was written in C with hand-coded gradients, precisely because the sparse, closed-form update is far cheaper than a general autograd graph for this specific objective.</span>
* <span style="font-size: 14px;">Seeing the $(\sigma - t)$ structure makes the connection to logistic regression and to the implicit matrix factorization view explicit, which a black-box backward() call hides.</span>

---

## Worked Numerical Example ($D = 2$, $k = 1$)

<span style="font-size: 14px;">Let $v_c = [0.1, 0.2]$, positive vector $u_o = [0.1, 0.4]$, negative vector $u_n = [-0.5, 0.3]$, and $\eta = 0.1$.</span>

<span style="font-size: 14px;">1. **Positive score**: $s_o = v_c \cdot u_o = 0.1 \cdot 0.1 + 0.2 \cdot 0.4 = 0.09$, so $\sigma(s_o) \approx 0.5225$ and the coefficient is $\sigma(s_o) - 1 \approx -0.4775$.</span>

<span style="font-size: 14px;">2. **Negative score**: $s_n = v_c \cdot u_n = 0.1 \cdot (-0.5) + 0.2 \cdot 0.3 = 0.01$, so $\sigma(s_n) \approx 0.5025$ and the coefficient is $0.5025$.</span>

<span style="font-size: 14px;">3. **Center gradient**: $\nabla v_c = -0.4775 \cdot [0.1, 0.4] + 0.5025 \cdot [-0.5, 0.3] \approx [-0.2990, -0.0403]$.</span>

<span style="font-size: 14px;">4. **Output gradients**: $\nabla u_o = -0.4775 \cdot [0.1, 0.2] \approx [-0.0477, -0.0955]$ and $\nabla u_n = 0.5025 \cdot [0.1, 0.2] \approx [0.0503, 0.1005]$.</span>

<span style="font-size: 14px;">5. **Apply updates** with $\eta = 0.1$: $v_c \leftarrow [0.1, 0.2] - 0.1 \cdot [-0.2990, -0.0403] \approx [0.1299, 0.2040]$, and similarly $u_o \leftarrow [0.1048, 0.4096]$, $u_n \leftarrow [-0.5050, 0.2899]$.</span>

<span style="font-size: 14px;">Notice the center vector moved toward the positive context and slightly away from the negative, exactly as the objective intends.</span>

---

## <span style="font-size: 16px;">Variants and Modern Context</span>

<span style="font-size: 14px;">SGNS sits at the root of a long line of representation-learning methods, and its gradient step recurs in many places:</span>

* <span style="font-size: 14px;">**GloVe** (Pennington et al., 2014) replaces the sampled objective with a weighted least-squares fit to log co-occurrence counts, but ends up in a similar geometric space.</span>
* <span style="font-size: 14px;">**FastText** (Bojanowski et al., 2017) keeps the exact SGNS update but represents each word as a sum of character n-gram vectors, so the same gradient flows into subword embeddings.</span>
* <span style="font-size: 14px;">**Contrastive learning** in modern systems (for example InfoNCE used by CLIP and SimCLR) generalizes the positive-versus-negatives structure: a real pair scored against sampled negatives, with the same $(\sigma - t)$ style error signal driving the update.</span>

<span style="font-size: 14px;">The dual-table design also reappears: many recommendation and retrieval models keep separate query and item embedding tables trained with a negative-sampling loss, and update both sides per step exactly as SGNS does here.</span>

---

## <span style="font-size: 16px;">Pitfalls</span>

* <span style="font-size: 14px;">**Mutating the center vector before computing output gradients.** If $W_{in}[c]$ is updated in place first, the gradients for $W_{out}$ are then computed with the wrong vector. Always snapshot $v_c$ and read the original output rows, compute every gradient, then apply. The error grows with the learning rate.</span>
* <span style="font-size: 14px;">**Sign confusion (ascent vs descent).** SGD subtracts the gradient. Using a plus sign performs gradient ascent and pushes the loss up, separating words that should be close. The positive coefficient is $\sigma(s_o) - 1$, which is negative; forgetting the $-1$ uses $\sigma(s_o)$ and treats the true context like a negative.</span>
* <span style="font-size: 14px;">**Dropping the negative terms in the center gradient.** The center gradient sums the positive contribution and every negative contribution. Omitting the negative sum leaves $v_c$ updated only toward the context, removing the repulsion that prevents all vectors from collapsing together.</span>
* <span style="font-size: 14px;">**Forgetting to update one of the two matrices.** Both $W_{in}$ and $W_{out}$ receive gradients. Updating only the output table (or only the input table) silently breaks training; the dot-product objective is symmetric and needs both sides to move. Repeated or duplicated negative ids must also accumulate their gradients on the shared row rather than overwrite.</span>

---

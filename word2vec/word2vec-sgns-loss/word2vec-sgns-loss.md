# <span style="font-size: 20px;">Skip-gram Negative Sampling Loss</span>

<span style="font-size: 14px;">Skip-gram with Negative Sampling (SGNS) is the training objective introduced by Mikolov et al. (2013) that made word2vec fast enough to train on billions of words. Instead of predicting a full probability distribution over the entire vocabulary for each context word, SGNS reframes training as a set of independent binary classification problems: tell real (center, context) pairs apart from randomly sampled noise pairs.</span>

---

## <span style="font-size: 16px;">The Full-Softmax Problem</span>

<span style="font-size: 14px;">The original skip-gram model predicts context words from a center word. For a center word $c$ and a context word $o$, the model uses an input embedding $v_c$ and an output embedding $u_o$, and defines the probability with a softmax over the whole vocabulary $W$:</span>

$$
p(o \mid c) = \frac{\exp(u_o^\top v_c)}{\sum_{w=1}^{W} \exp(u_w^\top v_c)}
$$

<span style="font-size: 14px;">The denominator sums over every word in the vocabulary. Real vocabularies have $10^5$ to $10^7$ words, so each training example would require a dot product against every output vector, plus the same cost again during backpropagation. With billions of training tokens this is computationally hopeless.</span>

<span style="font-size: 14px;">The paper states the goal plainly: the softmax normalization is "impractical because the cost of computing the gradient is proportional to $W$". Every alternative in the paper exists to avoid touching all $W$ output vectors per update.</span>

---

## <span style="font-size: 16px;">From NCE to Negative Sampling</span>

<span style="font-size: 14px;">Negative sampling is a simplification of **Noise Contrastive Estimation** (NCE, Gutmann and Hyvarinen, 2012; Mnih and Teh, 2012). NCE reduces density estimation to binary classification: train a logistic classifier to separate true data samples from samples drawn from a known noise distribution. NCE preserves enough structure to approximate the softmax probabilities.</span>

<span style="font-size: 14px;">word2vec only needs good embeddings, not calibrated probabilities. So the authors drop the parts of NCE that are needed for density estimation and keep only the binary classification core. The result is negative sampling: a cheaper objective tuned specifically for learning representations rather than modeling likelihood.</span>

<span style="font-size: 14px;">Concretely, NCE weights each noise sample by the ratio of data and noise densities so that the classifier's output can be converted back into a probability. Negative sampling throws away those weights and the noise normalization, treating every sampled negative as a plain label-0 example. The paper notes that while NCE approximately maximizes the log-probability of the softmax, negative sampling does not, and that this trade is acceptable precisely because the embeddings, not the probabilities, are the product.</span>

---

## <span style="font-size: 16px;">The SGNS Objective</span>

<span style="font-size: 14px;">For a single observed (center, positive context) pair $(c, o)$, the model draws $k$ negative words $n_1, \dots, n_k$ from a noise distribution and minimizes:</span>

$$
L = -\log\sigma(v_c^\top u_o) - \sum_{i=1}^{k}\log\sigma(-v_c^\top u_{n_i})
$$

<span style="font-size: 14px;">where $\sigma(x) = 1 / (1 + e^{-x})$ is the logistic sigmoid. The terms have a clean interpretation:</span>

* <span style="font-size: 14px;">**Positive term** $-\log\sigma(v_c^\top u_o)$: push the score of the real pair up, since $\sigma$ approaches 1 as the dot product grows, driving this loss to 0.</span>
* <span style="font-size: 14px;">**Negative terms** $-\log\sigma(-v_c^\top u_{n_i})$: push the score of each noise pair down. $\sigma(-x)$ approaches 1 when $x$ is very negative, so the loss is minimized when noise dot products are large and negative.</span>

<span style="font-size: 14px;">Each term is the binary cross-entropy of a logistic classifier. The positive pair has label 1, every negative pair has label 0. The center word uses its **input** embedding $v_c$; both the positive and negative context words use their **output** embeddings $u$.</span>

<span style="font-size: 14px;">A subtle but important point: this loss is for a single observed (center, positive) pair. A skip-gram pass over a sentence generates one such pair for every center word and every context word inside its window, and each of those pairs gets its own fresh set of $k$ negatives. The total training objective sums this per-pair loss over the whole corpus. Because the negatives are resampled per pair, the same noise word can appear as a negative for many different centers, which is fine: the objective only ever asks whether a specific (center, candidate) dot product should be high or low.</span>

<span style="font-size: 14px;">Note also that there is no normalization across the vocabulary anywhere in $L$. Each term depends only on the one dot product it contains. This locality is exactly what makes the gradient cheap: an update touches the input vector of the center, the output vector of the positive, and the $k$ output vectors of the negatives, and nothing else.</span>

---

## <span style="font-size: 16px;">Sigmoid as Binary Classification</span>

<span style="font-size: 14px;">The sigmoid turns a raw dot product into a probability that a pair is "real". Define $D = 1$ for a true pair and $D = 0$ for a noise pair. Then:</span>

$$
p(D = 1 \mid c, w) = \sigma(v_c^\top u_w), \qquad p(D = 0 \mid c, w) = 1 - \sigma(v_c^\top u_w) = \sigma(-v_c^\top u_w)
$$

<span style="font-size: 14px;">The identity $1 - \sigma(x) = \sigma(-x)$ is why the negative term carries the minus sign inside the sigmoid. Maximizing the log-likelihood of the labels (1 for the observed pair, 0 for each sampled negative) gives exactly the loss above. Minimizing $L$ is maximizing that log-likelihood.</span>

---

## <span style="font-size: 16px;">Why softplus for Stability</span>

<span style="font-size: 14px;">Computing $-\log\sigma(x)$ naively means evaluating $\sigma(x)$ first, then taking its log. When $x$ is a large negative number, $\sigma(x)$ underflows to exactly 0 in floating point, and $\log(0) = -\infty$. The loss then becomes $\text{inf}$ or $\text{nan}$, and gradients explode. With unbounded embeddings, dot products can easily reach magnitudes of 30 or more, so this is a real failure mode, not a corner case.</span>

<span style="font-size: 14px;">The stable rewrite uses the softplus function $\text{softplus}(x) = \log(1 + e^x)$:</span>

$$
-\log\sigma(x) = -\log\frac{1}{1 + e^{-x}} = \log(1 + e^{-x}) = \text{softplus}(-x)
$$

<span style="font-size: 14px;">So the positive term becomes $\text{softplus}(-v_c^\top u_o)$ and each negative term becomes $\text{softplus}(v_c^\top u_{n_i})$:</span>

$$
L = \text{softplus}(-v_c^\top u_o) + \sum_{i=1}^{k}\text{softplus}(v_c^\top u_{n_i})
$$

<span style="font-size: 14px;">Library softplus implementations use the identity $\text{softplus}(x) = \max(x, 0) + \log(1 + e^{-|x|})$, which never overflows or underflows for any finite input. This is the same trick PyTorch uses inside $\texttt{F.softplus}$ and $\texttt{F.logsigmoid}$.</span>

---

## <span style="font-size: 16px;">The Role of k</span>

<span style="font-size: 14px;">$k$ is the number of negative samples drawn per positive pair. It directly controls the cost: each update touches $k + 1$ output vectors instead of all $W$. The paper reports:</span>

* <span style="font-size: 14px;">**Small datasets:** $k$ in the range 5 to 20 works well.</span>
* <span style="font-size: 14px;">**Large datasets:** $k$ as small as 2 to 5 is sufficient, because there is far more signal in the data itself.</span>

<span style="font-size: 14px;">Larger $k$ gives a stronger contrastive signal and more stable gradients, at higher per-step cost. The negatives are sampled from a unigram distribution raised to the power $3/4$, which the paper found empirically better than the plain unigram or uniform distribution: it boosts rare words slightly while still favoring frequent ones.</span>

---

## <span style="font-size: 16px;">Input vs Output Embeddings</span>

<span style="font-size: 14px;">word2vec maintains two separate embedding matrices. The **input matrix** holds $v_w$ vectors used when a word acts as the center. The **output matrix** holds $u_w$ vectors used when a word acts as context (positive or negative). The score of a pair is always a dot product between one input vector and one output vector, $v_c^\top u_w$, never two vectors from the same matrix.</span>

<span style="font-size: 14px;">Keeping the matrices separate avoids a self-similarity artifact: a single shared matrix would push a word's vector to have a large dot product with itself, which is undesirable. After training, practitioners usually keep the input matrix as the word vectors, or average the two.</span>

---

## <span style="font-size: 16px;">Comparison with Hierarchical Softmax</span>

<span style="font-size: 14px;">The same paper proposes **hierarchical softmax** as the other fast alternative. It arranges the vocabulary as the leaves of a binary Huffman tree and computes $p(o \mid c)$ as a product of sigmoids along the root-to-leaf path, costing $O(\log W)$ per example instead of $O(W)$.</span>

* <span style="font-size: 14px;">**Hierarchical softmax:** yields proper normalized probabilities, $O(\log W)$ cost, better for rare words because frequent words get shorter codes.</span>
* <span style="font-size: 14px;">**Negative sampling:** simpler to implement, $O(k)$ cost independent of $W$, better for frequent words and low-dimensional vectors, but the scores are not normalized probabilities.</span>

<span style="font-size: 14px;">Negative sampling became the default in practice because of its simplicity and strong empirical results, and the same contrastive idea later reappeared throughout representation learning.</span>

---

## <span style="font-size: 16px;">Modern Context</span>

<span style="font-size: 14px;">SGNS is the prototype for the **contrastive learning** family that now dominates self-supervised representation learning. The recipe is the same: define a score for pairs, label real co-occurrences as positives, draw negatives from a noise distribution, and train a logistic objective to separate them.</span>

* <span style="font-size: 14px;">**InfoNCE** (van den Oord et al., 2018) generalizes the idea with a softmax over one positive and many negatives, used in SimCLR and CLIP.</span>
* <span style="font-size: 14px;">**GloVe** (Pennington et al., 2014) reaches similar embeddings through a weighted least-squares fit on co-occurrence counts, a complementary route to the same geometry.</span>
* <span style="font-size: 14px;">**Levy and Goldberg (2014)** showed SGNS implicitly factorizes a shifted pointwise-mutual-information matrix, connecting the neural objective to classical count-based methods.</span>

<span style="font-size: 14px;">Understanding the SGNS loss is therefore not just historical: the binary-classification-against-noise pattern is a foundational primitive in representation learning.</span>

---

## <span style="font-size: 16px;">Gradients and What They Learn</span>

<span style="font-size: 14px;">The gradient of the loss makes the contrastive behavior explicit. For the positive pair, the derivative of $-\log\sigma(v_c^\top u_o)$ with respect to the score $s_o = v_c^\top u_o$ is $\sigma(s_o) - 1$, a value in $(-1, 0)$. For a negative pair, the derivative of $-\log\sigma(-v_c^\top u_{n_i})$ with respect to $s_{n_i} = v_c^\top u_{n_i}$ is $\sigma(s_{n_i})$, a value in $(0, 1)$.</span>

<span style="font-size: 14px;">By the chain rule, the gradient flowing into the input vector $v_c$ is:</span>

$$
\frac{\partial L}{\partial v_c} = (\sigma(s_o) - 1)\, u_o + \sum_{i=1}^{k} \sigma(s_{n_i})\, u_{n_i}
$$

<span style="font-size: 14px;">The interpretation is direct. The term $(\sigma(s_o) - 1)$ is negative, so a gradient step moves $v_c$ toward $u_o$, pulling the real pair closer. Each $\sigma(s_{n_i})$ is positive, so the step moves $v_c$ away from the noise vectors $u_{n_i}$. The magnitude of each push is the model's current error on that pair: a negative that already scores low contributes almost nothing, while a confidently wrong one contributes a near-unit gradient. This automatic focus on hard, informative examples is what makes the objective sample-efficient.</span>

---

## Worked Example ($D = 2$, $k = 1$)

<span style="font-size: 14px;">Let $v_c = [1, 0]$, $u_o = [1, 0]$, and one negative $u_{n} = [-1, 0]$.</span>

<span style="font-size: 14px;">1. **Positive score**: $v_c^\top u_o = 1 \cdot 1 + 0 \cdot 0 = 1$.</span>

<span style="font-size: 14px;">2. **Negative score**: $v_c^\top u_n = 1 \cdot (-1) + 0 \cdot 0 = -1$.</span>

<span style="font-size: 14px;">3. **Positive loss**: $\text{softplus}(-1) = \log(1 + e^{-1}) \approx 0.3133$.</span>

<span style="font-size: 14px;">4. **Negative loss**: $\text{softplus}(-1) = \log(1 + e^{-1}) \approx 0.3133$ (note the negative term uses $+v_c^\top u_n = -1$ as the softplus input).</span>

<span style="font-size: 14px;">5. **Total**: $L \approx 0.3133 + 0.3133 = 0.6266$. The model is doing well here: the real pair has a high score and the noise pair a low score, so both losses are small.</span>

<span style="font-size: 14px;">A useful sanity check: if every embedding is the zero vector, all dot products are 0, $\sigma(0) = 0.5$, and the loss equals $(k+1)\log 2 \approx 0.6931(k+1)$.</span>

---

## <span style="font-size: 16px;">Pitfalls</span>

* <span style="font-size: 14px;">**Sign error on the negative term.** The negative term is $-\log\sigma(-v_c^\top u_{n_i})$, equivalently $\text{softplus}(+v_c^\top u_{n_i})$. Dropping the inner minus sign (using $\sigma(+v_c^\top u_{n_i})$, i.e. $\text{softplus}(-v_c^\top u_{n_i})$) trains the model to make noise pairs look real, the exact opposite of the intent. The loss still looks plausible on small inputs, so this bug is easy to miss without a check against a reference.</span>
* <span style="font-size: 14px;">**Numerical overflow from naive log-sigmoid.** Writing $-\log(\text{sigmoid}(x))$ directly overflows to $\text{inf}$ or $\text{nan}$ when $|x|$ is large, because the sigmoid saturates to 0 or 1 in floating point. Always use softplus or a fused log-sigmoid. The failure only appears with large-magnitude dot products, which is exactly what well-separated embeddings produce.</span>
* <span style="font-size: 14px;">**Summing vs averaging the negatives.** The objective sums over the $k$ negatives. Averaging (dividing by $k$) shrinks the negative gradient by a factor of $k$, weakening the contrastive signal and changing the effective learning dynamics. The loss value is wrong for any $k > 1$.</span>
* <span style="font-size: 14px;">**Mixing up input and output embeddings.** Every score is $v_c^\top u_w$: a center word's input vector dotted with a context word's output vector. Using two input vectors or two output vectors, or swapping which matrix a word is looked up in, silently corrupts the gradients while still producing a finite-looking loss.</span>

---

# <span style="font-size: 20px;">CBOW Forward Pass</span>

<span style="font-size: 14px;">The Continuous Bag-of-Words (CBOW) model (Mikolov et al., 2013) learns word embeddings by predicting a center word from the words that surround it. It is one of the two architectures introduced in the original word2vec paper, the other being Skip-gram. CBOW treats the context as an unordered bag of words, averages their input embeddings into a single vector, and scores every word in the vocabulary with a softmax classifier.</span>

---

## <span style="font-size: 16px;">What CBOW Computes</span>

<span style="font-size: 14px;">Given a center word and a window of surrounding words, CBOW asks: how well can the model predict the center word from its context? Training maximizes the probability the model assigns to the true center word. The forward pass produces a single scalar cross-entropy loss for one (context, target) example.</span>

<span style="font-size: 14px;">There are two embedding matrices, not one:</span>

* <span style="font-size: 14px;">**Input matrix** $W_{\text{in}} \in \mathbb{R}^{V \times D}$: row $i$ is the input (context) embedding of word $i$. $V$ is the vocabulary size, $D$ is the embedding dimension.</span>
* <span style="font-size: 14px;">**Output matrix** $W_{\text{out}} \in \mathbb{R}^{V \times D}$: row $j$ is the output (target) embedding of word $j$. These are the weights of the prediction layer.</span>

<span style="font-size: 14px;">After training, the input matrix $W_{\text{in}}$ is the one typically kept as the word vectors. The output matrix is discarded or, in some setups, averaged with the input matrix. Keeping two matrices lets a word play two distinct roles, as a context word and as a prediction target, which empirically produces cleaner geometry than tying them.</span>

<span style="font-size: 14px;">A single forward pass therefore consumes one training position: the $m$ ids in the window become the context, the word at the window center becomes the target, and the output is the scalar loss for that one prediction. Sliding the window across a corpus generates one such example per position.</span>

---

## <span style="font-size: 16px;">Key Equations</span>

<span style="font-size: 14px;">Let the context word ids be $c_1, c_2, \ldots, c_m$ and the target (center) word id be $t$. The forward pass has three steps.</span>

<span style="font-size: 14px;">**1. Average the context embeddings** into a single hidden vector $h \in \mathbb{R}^D$:</span>

$$
h = \frac{1}{m} \sum_{k=1}^{m} W_{\text{in}}[c_k]
$$

<span style="font-size: 14px;">**2. Score every vocabulary word** by taking the dot product of $h$ with each output embedding. This is a single matrix-vector product giving logits $z \in \mathbb{R}^V$:</span>

$$
z = W_{\text{out}} \, h, \qquad z_j = W_{\text{out}}[j] \cdot h
$$

<span style="font-size: 14px;">**3. Cross-entropy loss** against the target id $t$ using a full softmax over the whole vocabulary:</span>

$$
P(t \mid \text{context}) = \frac{e^{z_t}}{\sum_{j=1}^{V} e^{z_j}}, \qquad \mathcal{L} = -\log P(t \mid \text{context})
$$

<span style="font-size: 14px;">In practice the loss is computed with $\text{log\_softmax}$ rather than taking the log of softmax directly, for numerical stability:</span>

$$
\mathcal{L} = -\left( z_t - \log \sum_{j=1}^{V} e^{z_j} \right)
$$

---

## <span style="font-size: 16px;">CBOW vs Skip-gram</span>

<span style="font-size: 14px;">The two word2vec architectures invert the prediction direction:</span>

* <span style="font-size: 14px;">**CBOW** predicts the center word from the context: input is the bag of surrounding words, output is the one center word. One prediction per training position.</span>
* <span style="font-size: 14px;">**Skip-gram** predicts each context word from the center word: input is the single center word, output is each surrounding word. It produces $m$ predictions per training position, one per context word.</span>

<span style="font-size: 14px;">The paper reports that CBOW trains faster because it makes a single softmax prediction per position instead of one per context word. Skip-gram is slower but produces better representations for **rare words**, because every occurrence of a rare word generates several training signals (one for each neighbor) rather than being averaged away inside a context bag.</span>

<span style="font-size: 14px;">The paper's own phrasing is that CBOW is "similar to the feedforward NNLM, where the non-linear hidden layer is removed and the projection layer is shared for all words", and that the order of words in the history does not influence the projection. That order-independence is exactly the averaging step below.</span>

---

## <span style="font-size: 16px;">Why Average the Context</span>

<span style="font-size: 14px;">Averaging the context embeddings is what makes CBOW a **bag** of words. The mean is symmetric: permuting the context ids leaves $h$ unchanged, so word order inside the window is discarded. This is a deliberate simplification. The paper removed the expensive ordered hidden layer of earlier neural language models and replaced it with a single shared projection that simply sums (here, averages) the projected context vectors.</span>

<span style="font-size: 14px;">Averaging rather than summing keeps the magnitude of $h$ roughly independent of the window size $m$. With a raw sum, a context of 8 words would produce logits roughly 8 times larger than a context of 2 words, distorting the softmax temperature. Dividing by $m$ normalizes this. Some implementations sum instead of average; the original C tool divides by the window count, matching the mean used here.</span>

<span style="font-size: 14px;">The trade-off is that averaging blurs the contribution of any single context word. A highly informative neighbor and a common stopword are weighted equally, and their embeddings are pulled together into one mean. This is acceptable when the goal is a smooth, general-purpose word representation, which is precisely what word2vec targets. When position or per-word weighting matters, later models reintroduce it through attention rather than a plain mean.</span>

---

## <span style="font-size: 16px;">The Projection Layer</span>

<span style="font-size: 14px;">The mapping from context ids to $h$ is an embedding lookup followed by a mean, not a dense matrix multiply. Row selection $W_{\text{in}}[c_k]$ is equivalent to multiplying a one-hot vector by $W_{\text{in}}$, but indexing is far cheaper. Because there is no nonlinearity between the projection and the output scores, CBOW is a **log-bilinear** model: the score $z_j = W_{\text{out}}[j] \cdot h$ is bilinear in the input and output embeddings.</span>

<span style="font-size: 14px;">The output layer is a plain linear classifier with $V$ classes and no bias. Its weight matrix is $W_{\text{out}}$. There is no separate softmax weight matrix; the output embeddings themselves are the classifier weights.</span>

---

## <span style="font-size: 16px;">The Full-Softmax Cost</span>

<span style="font-size: 14px;">The denominator $\sum_{j=1}^{V} e^{z_j}$ runs over the entire vocabulary. For each training example this costs $O(V \cdot D)$ to compute the logits plus $O(V)$ for the normalization. With a vocabulary of millions of words, the full softmax dominates training time, since every parameter update touches every output embedding through the normalization term.</span>

<span style="font-size: 14px;">The word2vec paper therefore replaces the full softmax with cheaper approximations in practice:</span>

* <span style="font-size: 14px;">**Hierarchical softmax**: organizes the vocabulary as a Huffman tree, reducing the cost per prediction from $O(V)$ to $O(\log V)$. Frequent words sit near the root, so the average path length is short.</span>
* <span style="font-size: 14px;">**Negative sampling (SGNS)**: reframes the problem as binary classification of the true pair against a few sampled noise words, costing $O(k \cdot D)$ for $k$ negatives instead of $O(V \cdot D)$.</span>

<span style="font-size: 14px;">This problem implements the exact full softmax so the loss is well defined and deterministic. It is the conceptual baseline that the sampling methods approximate, and it is the cleanest way to see what CBOW is actually optimizing before efficiency tricks are layered on top.</span>

---

## <span style="font-size: 16px;">Gradient and Training Signal</span>

<span style="font-size: 14px;">The gradient of the cross-entropy loss with respect to the logits is the softmax probability minus the one-hot target:</span>

$$
\frac{\partial \mathcal{L}}{\partial z_j} = P(j \mid \text{context}) - \mathbb{1}[j = t]
$$

<span style="font-size: 14px;">This pushes the logit of the true target up (its gradient is $P(t) - 1 < 0$) and pulls every other logit down in proportion to its current probability. Through the chain rule this updates two groups of parameters:</span>

* <span style="font-size: 14px;">Each output embedding $W_{\text{out}}[j]$ moves toward (target) or away from (non-targets) the context vector $h$, scaled by its error $P(j) - \mathbb{1}[j=t]$.</span>
* <span style="font-size: 14px;">Each context word's input embedding receives the same averaged gradient, because the mean distributes the upstream gradient equally across the $m$ context rows, each scaled by $1/m$.</span>

<span style="font-size: 14px;">Because the gradient flows back through the mean, all context words in one example are nudged identically. This is another reason rare words learn slowly under CBOW: their gradient is diluted by the averaging and shared with the more frequent words in the same window.</span>

---

## <span style="font-size: 16px;">Worked Example</span>

<span style="font-size: 14px;">Take a vocabulary of 4 words, $D = 2$, context ids $[0, 2]$, and target id $1$. Let:</span>

$$
W_{\text{in}} = \begin{pmatrix} 0.1 & -0.2 \ 0.3 & 0.4 \ -0.5 & 0.6 \ 0.7 & -0.8 \end{pmatrix}, \quad W_{\text{out}} = \begin{pmatrix} 0.2 & 0.1 \ -0.3 & 0.5 \ 0.4 & -0.6 \ 0.9 & 0.0 \end{pmatrix}
$$

<span style="font-size: 14px;">**Step 1, average context.** Rows 0 and 2 of $W_{\text{in}}$ are $[0.1, -0.2]$ and $[-0.5, 0.6]$. Their mean is $h = [-0.2, 0.2]$.</span>

<span style="font-size: 14px;">**Step 2, logits.** Each logit is $W_{\text{out}}[j] \cdot h$:</span>

* <span style="font-size: 14px;">$z_0 = 0.2(-0.2) + 0.1(0.2) = -0.02$</span>
* <span style="font-size: 14px;">$z_1 = -0.3(-0.2) + 0.5(0.2) = 0.16$</span>
* <span style="font-size: 14px;">$z_2 = 0.4(-0.2) + (-0.6)(0.2) = -0.20$</span>
* <span style="font-size: 14px;">$z_3 = 0.9(-0.2) + 0.0(0.2) = -0.18$</span>

<span style="font-size: 14px;">**Step 3, loss.** Softmax over $z$ gives the target probability $P(1)$, and the loss is $-\log P(1) \approx 1.177$. The target word 1 has the highest logit, so its probability is the largest of the four, but it is still well below 1, leaving a nonzero loss that training will push down.</span>

---

## <span style="font-size: 16px;">Comparison with SGNS</span>

<span style="font-size: 14px;">Skip-gram with negative sampling (SGNS) is the most widely used word2vec variant, and it is worth contrasting with the full-softmax CBOW implemented here.</span>

* <span style="font-size: 14px;">**Objective.** Full-softmax CBOW maximizes a single normalized probability over $V$ classes. SGNS maximizes the log-sigmoid score of the true (center, context) pair while minimizing the score of $k$ sampled negatives. The SGNS loss is $-\log \sigma(v_t \cdot h) - \sum_{i=1}^{k} \log \sigma(-v_{n_i} \cdot h)$.</span>
* <span style="font-size: 14px;">**Normalization.** CBOW pays $O(V)$ to normalize every step. SGNS never normalizes; it only contrasts the target against a handful of negatives, which is why it scales to huge vocabularies.</span>
* <span style="font-size: 14px;">**Direction.** CBOW averages many context words to predict one center word. Skip-gram uses one center word to predict each context word, so a rare center word still produces several gradient updates.</span>

<span style="font-size: 14px;">Levy and Goldberg (2014) later showed that SGNS implicitly factorizes a shifted pointwise mutual information matrix, giving a theoretical bridge between these neural objectives and classical count-based embeddings. Full-softmax CBOW does not have such a clean closed form, but it remains the most direct expression of "predict the word from its context".</span>

---

## <span style="font-size: 16px;">Modern Context</span>

<span style="font-size: 14px;">CBOW and Skip-gram produce a single static vector per word, independent of sentence context. This is their main limitation: polysemous words like "bank" collapse all senses into one point. Contextual models that followed (ELMo, BERT, and modern Transformer language models) replaced static embeddings with context-dependent representations computed by deep encoders.</span>

<span style="font-size: 14px;">Even so, the CBOW idea persists. The input embedding table at the bottom of every Transformer is a learned $W_{\text{in}}$, and the final language-model head that scores the vocabulary is a learned $W_{\text{out}}$ with a full softmax, often tied to the input table. The averaging step survives in pooling layers that summarize a span of tokens into a single vector. Understanding the CBOW forward pass is a compact way to understand the embedding-and-softmax sandwich that bookends nearly every modern language model.</span>

---

## <span style="font-size: 16px;">Numerical Stability</span>

<span style="font-size: 14px;">Computing softmax as $e^{z_j} / \sum_k e^{z_k}$ directly overflows when any $z_j$ is large. The stable form subtracts the maximum logit first:</span>

$$
\log \sum_j e^{z_j} = z_{\max} + \log \sum_j e^{z_j - z_{\max}}
$$

<span style="font-size: 14px;">This is what $\text{log\_softmax}$ does internally. Using it and then indexing the target entry, rather than building probabilities and taking a log, avoids both overflow from large positive logits and the $\log(0)$ underflow that occurs when a probability rounds to zero.</span>

---

## <span style="font-size: 16px;">Pitfalls</span>

* <span style="font-size: 14px;">**Summing the context instead of averaging.** A raw sum scales the hidden vector with the window size, inflating logits and changing the loss. The mean keeps $h$ at a consistent scale regardless of how many context words are present. Forgetting the $1/m$ factor is the most common CBOW bug.</span>
* <span style="font-size: 14px;">**Projecting with the wrong matrix.** Context lookup uses $W_{\text{in}}$ and scoring uses $W_{\text{out}}$. Reusing $W_{\text{in}}$ for the output projection (a single-matrix model) is a different, weaker model and produces the wrong loss. The two matrices are intentionally separate.</span>
* <span style="font-size: 14px;">**Taking the loss on raw logits.** The loss is the negative log of the softmax probability, not the negative logit. Skipping $\text{log\_softmax}$ omits the normalization term $\log \sum_j e^{z_j}$, so the gradient no longer competes the target against the rest of the vocabulary.</span>
* <span style="font-size: 14px;">**Sign and index errors.** Cross-entropy is the **negative** log probability, so a correct prediction yields a small positive loss, never a negative one. Indexing the wrong row of the log-probabilities (for example always using index 0 instead of the target id) silently trains toward the wrong word.</span>

---

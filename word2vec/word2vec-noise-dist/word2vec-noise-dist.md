# <span style="font-size: 20px;">Negative Sampling Distribution</span>

<span style="font-size: 14px;">The negative sampling distribution is the probability law from which Word2Vec draws "noise" words during training. Introduced by Mikolov et al. (2013) in the skip-gram paper, it raises each word's corpus count to the power $\alpha = 0.75$ and renormalizes. This single design choice, a fractional exponent applied to the unigram frequencies, is what lets skip-gram learn good embeddings without ever evaluating a full softmax over the vocabulary.</span>

---

## <span style="font-size: 16px;">Why Negative Sampling Exists</span>

<span style="font-size: 14px;">The skip-gram model predicts context words from a center word. The naive objective is a softmax over the entire vocabulary:</span>

$$
p(w_O \mid w_I) = \frac{\exp(v_{w_O}^{\prime \top} v_{w_I})}{\sum_{w=1}^{V} \exp(v_w^{\prime \top} v_{w_I})}
$$

<span style="font-size: 14px;">The denominator sums over all $V$ words. For realistic vocabularies ($V$ in the hundreds of thousands or millions), computing this normalizer and its gradient for every training pair is prohibitively expensive. Each update would touch every output vector in the model.</span>

<span style="font-size: 14px;">Negative sampling sidesteps the softmax entirely. Instead of asking "which of all $V$ words is the context word", it reframes training as a set of independent binary classification problems: distinguish the true context word (a positive example) from a handful of $k$ randomly drawn **noise words** (negative examples). The model only updates the embeddings for the positive word and the $k$ sampled negatives, turning an $O(V)$ update into an $O(k)$ update with $k$ typically between 5 and 20.</span>

---

## <span style="font-size: 16px;">What the Noise Distribution Does</span>

<span style="font-size: 14px;">Negative sampling needs a rule for drawing the noise words. That rule is the **noise distribution** $P_n(w)$. For each positive training pair, $k$ negatives are sampled i.i.d. from $P_n(w)$ over the vocabulary. The quality of the learned embeddings depends heavily on this distribution.</span>

<span style="font-size: 14px;">Two obvious choices bracket the design space:</span>

* <span style="font-size: 14px;">**Uniform** ($P_n(w) \propto 1$): every word is equally likely to be a negative. This ignores the fact that some words are vastly more common than others, so the model wastes effort distinguishing the positive from rare words it would almost never confuse anyway.</span>
* <span style="font-size: 14px;">**Unigram** ($P_n(w) \propto \text{count}(w)$): sample negatives in proportion to raw frequency. This over-samples extremely common words ("the", "of", "a"), so the model spends almost all its negative budget on a few function words and rarely sees informative content words as negatives.</span>

<span style="font-size: 14px;">The paper's answer is a compromise between these two extremes, controlled by an exponent $\alpha$.</span>

---

## <span style="font-size: 16px;">The Equation</span>

<span style="font-size: 14px;">Given the corpus counts $\text{count}(w)$ for each word $w$, the noise distribution is the unigram distribution raised to the power $\alpha$ and renormalized to sum to one:</span>

$$
P_n(w) = \frac{\text{count}(w)^{\alpha}}{\sum_{w'=1}^{V} \text{count}(w')^{\alpha}}
$$

<span style="font-size: 14px;">where:</span>

* <span style="font-size: 14px;">$\text{count}(w)$ is the number of times word $w$ appears in the training corpus (the unigram frequency, up to a constant)</span>
* <span style="font-size: 14px;">$\alpha$ is the flattening exponent, set to $0.75$ in the paper</span>
* <span style="font-size: 14px;">the denominator $Z = \sum_{w'} \text{count}(w')^{\alpha}$ is the partition function that makes the result a valid probability distribution</span>

<span style="font-size: 14px;">The paper writes this as $U(w)^{3/4} / Z$, where $U(w)$ is the unigram distribution and $Z$ is the normalizer. Because normalization removes any overall scaling, using raw counts and using frequencies $\text{count}(w)/N$ give the identical result: the factor $N^{\alpha}$ cancels between numerator and denominator.</span>

---

## <span style="font-size: 16px;">Why 0.75 Specifically</span>

<span style="font-size: 14px;">The exponent $\alpha$ interpolates between the two extremes above:</span>

* <span style="font-size: 14px;">$\alpha = 0$: every count becomes $\text{count}(w)^0 = 1$, so $P_n$ is **uniform** over the vocabulary.</span>
* <span style="font-size: 14px;">$\alpha = 1$: $P_n$ equals the raw **unigram** distribution.</span>
* <span style="font-size: 14px;">$0 < \alpha < 1$: a **flattened** unigram. Frequent words are still more likely than rare words, but the gap is compressed. Rare words get sampled more often than pure frequency would allow, and frequent words less often.</span>

<span style="font-size: 14px;">The value $0.75$ was chosen **empirically**. Mikolov et al. report that it "outperformed significantly the unigram and the uniform distributions" on both the analogy task and other benchmarks. It is not derived from a closed-form argument; it is a tuned hyperparameter that happened to work well across tasks and corpora, and the value stuck because subsequent work (including GloVe-era comparisons and the word2vec C reference implementation) reproduced its benefit.</span>

<span style="font-size: 14px;">The intuition for why a sub-linear exponent helps: word frequencies follow a Zipfian (heavy-tailed) law. A handful of function words dominate the raw counts by orders of magnitude. Sampling negatives proportional to raw frequency would mean the model almost only ever contrasts against those few words. Raising counts to $0.75$ shrinks the dynamic range, so a moderately common content word still appears as a negative often enough to provide a useful learning signal, while the truly dominant words no longer monopolize the sampling budget.</span>

---

## <span style="font-size: 16px;">How It Plugs Into the Objective</span>

<span style="font-size: 14px;">The noise distribution is one ingredient of the full skip-gram with negative sampling (SGNS) loss. For a center word $w_I$ and a true context word $w_O$, the paper replaces the softmax objective with:</span>

$$
\log \sigma(v_{w_O}^{\prime \top} v_{w_I}) + \sum_{i=1}^{k} \mathbb{E}_{w_i \sim P_n(w)} \big[ \log \sigma(-v_{w_i}^{\prime \top} v_{w_I}) \big]
$$

<span style="font-size: 14px;">where $\sigma$ is the logistic sigmoid. The first term pushes the dot product of the center and true-context vectors up (toward label $1$). The sum draws $k$ negatives from $P_n(w)$ and pushes each of their dot products down (toward label $0$). The noise distribution $P_n(w)$ is exactly the expectation's sampling law: change it and you change which words the model is trained to push away.</span>

<span style="font-size: 14px;">Note that $P_n(w)$ depends only on corpus counts, not on the model parameters. It is computed once before training and held fixed. This is what makes the precomputed sampling table (described below) possible: the distribution never updates as the embeddings learn.</span>

<span style="font-size: 14px;">A practical subtlety is whether the true context word can also be drawn as a negative. Most implementations simply sample from $P_n(w)$ without excluding the current positive. Because any single word's probability is small in a large vocabulary, the occasional collision has negligible effect, and the simplicity is worth the tiny noise it introduces.</span>

---

## <span style="font-size: 16px;">Relation to NCE</span>

<span style="font-size: 14px;">Negative sampling is a simplified relative of **Noise Contrastive Estimation** (Gutmann and Hyvarinen, 2010; Mnih and Teh, 2012). NCE turns density estimation into a classification problem between data samples and noise samples drawn from a known noise distribution, and it provably approximates the gradient of the full softmax as the number of noise samples grows.</span>

<span style="font-size: 14px;">Negative sampling drops the parts of NCE that NCE needs for that theoretical guarantee (it omits the noise-distribution normalization terms inside the loss), so it does not recover the exact softmax gradient. The paper is explicit that this is acceptable because skip-gram only needs **good embeddings**, not a calibrated language model. The noise distribution $P_n(w)$ plays the same role it does in NCE: it is the law that generates the contrastive negatives, and the $0.75$ exponent is the practical choice that makes that contrast informative.</span>

---

## <span style="font-size: 16px;">Effect on Rare vs Frequent Words</span>

<span style="font-size: 14px;">Consider two words, a frequent one with count $10000$ and a rare one with count $10$. Their ratio under each scheme:</span>

* <span style="font-size: 14px;">**Unigram** ($\alpha = 1$): ratio $= 10000 / 10 = 1000$. The frequent word is sampled a thousand times more often.</span>
* <span style="font-size: 14px;">**Flattened** ($\alpha = 0.75$): ratio $= 10000^{0.75} / 10^{0.75} = 1000 / 5.62 \approx 178$. Still favored, but the gap shrank by more than $5\times$.</span>
* <span style="font-size: 14px;">**Uniform** ($\alpha = 0$): ratio $= 1$. Equal probability.</span>

<span style="font-size: 14px;">So $\alpha = 0.75$ keeps the qualitative ordering of the unigram distribution (common words remain common negatives) while substantially boosting the relative chance of sampling rarer words, which is exactly the balance the paper found to learn the best representations.</span>

---

## Worked Example ($\alpha = 0.75$)

<span style="font-size: 14px;">Let the counts be $[100, 10, 1]$ for three words and $\alpha = 0.75$.</span>

<span style="font-size: 14px;">1. **Raise to the power $\alpha$**: $100^{0.75} \approx 31.623$, $\; 10^{0.75} \approx 5.623$, $\; 1^{0.75} = 1.0$.</span>

<span style="font-size: 14px;">2. **Sum (partition function)**: $Z = 31.623 + 5.623 + 1.0 = 38.246$.</span>

<span style="font-size: 14px;">3. **Normalize**: $P_n = [31.623/38.246, \; 5.623/38.246, \; 1.0/38.246] = [0.8268, 0.1470, 0.0261]$.</span>

<span style="font-size: 14px;">Compare with the pure unigram ($\alpha = 1$) on the same counts: $[100, 10, 1]/111 = [0.9009, 0.0901, 0.0090]$. The flattened distribution has shifted mass off the most frequent word (from $0.90$ down to $0.83$) and onto the two rarer words (the smallest rose from $0.009$ to $0.026$, nearly $3\times$). The probabilities still sum to $1$, and they preserve the ordering.</span>

---

## <span style="font-size: 16px;">Implementation Notes</span>

<span style="font-size: 14px;">In practice the word2vec C code does not sample from this distribution by recomputing it each time. It precomputes a large **unigram table** (commonly $10^8$ entries) where each word's index is repeated a number of times proportional to $\text{count}(w)^{0.75}$, then draws negatives by indexing the table at a uniformly random position. This makes each draw $O(1)$ and amortizes the normalization. The table is just a discretized representation of the same $P_n(w)$ defined above.</span>

<span style="font-size: 14px;">For a from-scratch computation the direct formula is fine: power, then divide by the sum. Doing the arithmetic in double precision avoids accumulation error in the partition function when the vocabulary is large.</span>

---

## <span style="font-size: 16px;">Variants and Modern Context</span>

<span style="font-size: 14px;">The $0.75$ exponent has proven remarkably durable and reappears, sometimes rediscovered, across later representation-learning methods:</span>

* <span style="font-size: 14px;">**GloVe** (Pennington et al., 2014) does not use negative sampling, but its weighting function $f(x) = (x / x_{\max})^{\beta}$ with $\beta = 0.75$ applies the same fractional power to co-occurrence counts, again to keep frequent pairs from dominating the loss. The shared exponent is not a coincidence: both methods are taming the same Zipfian tail.</span>
* <span style="font-size: 14px;">**Node2vec and DeepWalk** adapt skip-gram with negative sampling to graphs, and they carry over the unigram$^{0.75}$ noise distribution over nodes essentially unchanged.</span>
* <span style="font-size: 14px;">**StarSpace, fastText, and many recommendation embeddings** reuse the same smoothed-frequency negative sampler. fastText additionally samples at the subword level, but the frequency smoothing for word-level negatives follows word2vec.</span>

<span style="font-size: 14px;">Later analyses (notably Levy and Goldberg, 2014) showed that SGNS is implicitly factorizing a shifted pointwise-mutual-information matrix, and the noise distribution enters that analysis as the marginal used to define the PMI shift. This gives a post hoc theoretical handle on why the choice of $P_n$ matters: it changes the matrix being factorized, and the $0.75$ smoothing corresponds to a particular reweighting of that matrix that empirically yields better geometry.</span>

<span style="font-size: 14px;">In modern transformer-based language models the full softmax is computed directly (vocabularies of $30$K to $100$K subwords are affordable on accelerators), so explicit negative sampling and its noise distribution have largely disappeared from mainstream LLM pretraining. The idea survives in contrastive learning more broadly, where the choice of negative-sampling distribution remains a central design lever.</span>

---

## <span style="font-size: 16px;">Properties</span>

* <span style="font-size: 14px;">**Valid distribution.** For nonnegative counts and any $\alpha$, every entry is nonnegative and the entries sum to exactly $1$ by construction of the normalizer.</span>
* <span style="font-size: 14px;">**Order-preserving for $\alpha > 0$.** If $\text{count}(a) > \text{count}(b)$ then $P_n(a) > P_n(b)$. The exponent compresses gaps but never reverses the ranking.</span>
* <span style="font-size: 14px;">**Scale-invariant.** Multiplying all counts by a constant $c$ leaves $P_n$ unchanged, because $c^{\alpha}$ factors out of both numerator and denominator. Raw counts, frequencies, and counts-per-million all give the same answer.</span>
* <span style="font-size: 14px;">**Monotone in $\alpha$ at the extremes.** As $\alpha \to 0$ the distribution approaches uniform; as $\alpha \to 1$ it approaches the raw unigram. The chosen $0.75$ sits closer to unigram than to uniform.</span>

---

## <span style="font-size: 16px;">Pitfalls</span>

* <span style="font-size: 14px;">**Forgetting to renormalize after exponentiating.** The raised counts $\text{count}(w)^{\alpha}$ do not sum to one. Returning them directly gives a vector that may sum to hundreds or thousands. Always divide by the partition function $Z = \sum_{w'} \text{count}(w')^{\alpha}$, and verify the result sums to $1$.</span>
* <span style="font-size: 14px;">**Normalizing before exponentiating.** Computing $(\text{count}(w)/\sum \text{count})^{\alpha}$ and treating it as the answer is wrong: a power of a normalized distribution is not normalized, so $\sum_w p(w)^{\alpha} \neq 1$ for $\alpha \neq 1$. The exponent must be applied to the counts first, then normalized once.</span>
* <span style="font-size: 14px;">**Confusing the exponent direction.** The flattening uses $\text{count}^{0.75}$, not $\text{count}^{1/0.75}$. An exponent greater than one sharpens the distribution toward frequent words, the opposite of the intended effect. Any $\alpha \in (0,1)$ flattens; $\alpha > 1$ sharpens.</span>
* <span style="font-size: 14px;">**Using $\log$ instead of a power.** A log transform also compresses the dynamic range, but it is a different function: it can produce negative or zero values (for counts at or below one) and does not yield the distribution the paper specifies. The operation is a fractional power, not a logarithm.</span>
* <span style="font-size: 14px;">**Single-word edge case.** With one word the distribution is trivially $[1.0]$ for any $\alpha$ (including $\alpha = 0$, since $\text{count}^0 = 1$ and $1/1 = 1$). Code that special-cases empty input or assumes $V \ge 2$ can fail here.</span>

---
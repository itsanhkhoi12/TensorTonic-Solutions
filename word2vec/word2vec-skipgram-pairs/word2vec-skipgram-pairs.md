# <span style="font-size: 20px;">Skip-gram Pair Generation</span>

<span style="font-size: 14px;">Skip-gram is one of the two model architectures introduced by Mikolov et al. (2013) for learning distributed word representations. Its training data is not raw text but a stream of **(center, context) pairs** extracted from a sliding window over each sentence. This problem implements that extraction step: given a sequence of token ids and a window size, produce every center-context pair the model would be trained on.</span>

---

## <span style="font-size: 16px;">What Skip-gram Learns</span>

<span style="font-size: 14px;">The Skip-gram objective is to **predict surrounding context words from a given center word**. For each position in the corpus, the center word is fed into the model and the model is asked to assign high probability to each of the words that actually appear nearby. Over millions of such pairs, the embedding of each word is pulled toward the embeddings of the words it co-occurs with, so words that share contexts end up close together in vector space.</span>

<span style="font-size: 14px;">Formally, given a training corpus of tokens $w_1, w_2, \ldots, w_T$ and a window size $c$, the model maximizes the average log probability:</span>

$$
\frac{1}{T} \sum_{t=1}^{T} \sum_{-c \le j \le c,\ j \ne 0} \log p(w_{t+j} \mid w_t)
$$

<span style="font-size: 14px;">The inner sum ranges over every offset $j$ in the window except $j = 0$ (the center itself). Each term $\log p(w_{t+j} \mid w_t)$ corresponds to exactly one (center, context) training pair $(w_t, w_{t+j})$. This problem generates the set of pairs $(w_t, w_{t+j})$ that the objective sums over.</span>

---

## <span style="font-size: 16px;">The Window Concept</span>

<span style="font-size: 14px;">The **window** defines locality. With window size $c$, the context of a center token at position $i$ is every token at positions $i-c$ through $i+c$, excluding $i$ itself. The window captures the intuition behind the distributional hypothesis: words appearing in similar surrounding positions tend to have similar meaning.</span>

<span style="font-size: 14px;">A larger window pulls in more distant words and tends to capture **topical** or **domain** similarity (words that appear in the same kind of document). A smaller window captures more **syntactic** or functional similarity (words that are interchangeable in a sentence). Mikolov et al. report good results with windows around 5 to 10 for Skip-gram.</span>

<span style="font-size: 14px;">For a center at position $i$ in a sequence of length $n$, the context indices are:</span>

$$
\{ j : \max(0, i-c) \le j \le \min(n-1, i+c),\ j \ne i \}
$$

<span style="font-size: 14px;">The $\max$ and $\min$ clamp the window to the sequence boundaries so it never reads past the first or last token.</span>

---

## <span style="font-size: 16px;">Why Pairs Instead of Full Context Vectors</span>

<span style="font-size: 14px;">Skip-gram decomposes the multi-word prediction into independent single-word predictions. Instead of predicting the whole context $\{w_{i-c}, \ldots, w_{i+c}\}$ jointly, it emits one pair per context word and treats each as a separate training example. This has two practical benefits:</span>

* <span style="font-size: 14px;">**Simplicity:** each training step deals with a single softmax over the vocabulary for one target word, rather than a joint distribution over a set of words.</span>
* <span style="font-size: 14px;">**Scalability:** the pair view composes cleanly with negative sampling and hierarchical softmax, the two approximations Mikolov et al. use to avoid the full-vocabulary softmax.</span>

<span style="font-size: 14px;">The pair generation step is therefore the bridge between raw token sequences and the example stream that the optimizer consumes. Getting the pairs right (correct centers, correct contexts, correct boundaries) directly determines what the embeddings learn.</span>

---

## <span style="font-size: 16px;">Skip-gram vs CBOW</span>

<span style="font-size: 14px;">Word2Vec ships two architectures. They use the same window but flip the direction of prediction:</span>

* <span style="font-size: 14px;">**Skip-gram** predicts context from center: input is one word $w_i$, targets are the surrounding words. It generates one pair $(w_i, w_{i+j})$ per context word. Skip-gram works better on small datasets and represents rare words well, because each rare center word still produces several training pairs.</span>
* <span style="font-size: 14px;">**CBOW (Continuous Bag of Words)** predicts center from context: the surrounding words are averaged into a single input and the model predicts the center word $w_i$. CBOW is faster and slightly better on frequent words, but it collapses the context into one example per center position.</span>

<span style="font-size: 14px;">In pair terms, Skip-gram and CBOW use the same window membership; the difference is which element is the input and which is the target. This problem implements the Skip-gram direction: column 0 of each row is the center, column 1 is a context word.</span>

---

## <span style="font-size: 16px;">Fixed vs Dynamic Window</span>

<span style="font-size: 14px;">The original word2vec implementation uses a **dynamic window**: for each center word it samples a random integer $r$ uniformly from $1$ to $c$ and uses $r$ as the effective window for that position. This weights nearby words more heavily (they fall inside the window for more sampled values of $r$) and acts as a cheap form of distance-based weighting.</span>

<span style="font-size: 14px;">This problem deliberately uses a **fixed window** of exactly $c$ on both sides. The dynamic variant depends on a random draw per position, which would make the output nondeterministic and impossible to check exactly. Fixing the window keeps the mapping from input to output deterministic while preserving the core mechanic: enumerate the symmetric neighborhood and emit a pair for each neighbor.</span>

<span style="font-size: 14px;">If you wanted the dynamic behavior, you would replace the constant $c$ inside the loop with a per-center sampled value. Everything else (boundary clamping, self-exclusion, emission order) stays the same.</span>

---

## <span style="font-size: 16px;">Boundary Handling</span>

<span style="font-size: 14px;">Tokens near the start or end of a sequence have a truncated window because there are no words beyond the boundary. The first token has no left context; the last token has no right context. Correct handling clamps the window with $\max(0, i-c)$ on the left and $\min(n-1, i+c)$ on the right.</span>

<span style="font-size: 14px;">Two common mistakes here:</span>

* <span style="font-size: 14px;">**Wrapping around** (using modular indexing like $j \bmod n$) treats the sequence as circular and pairs the last token with the first. This is wrong: a sentence is not a loop.</span>
* <span style="font-size: 14px;">**Negative indexing** in Python silently reads from the end of the tensor. An unclamped $i - c$ when $i < c$ produces a negative index that maps to a token at the other end of the sequence, again creating phantom pairs.</span>

<span style="font-size: 14px;">A single-token sequence has no context at any window size, so it produces zero pairs. The function returns an empty tensor of shape $(0, 2)$ in that case, which keeps the output shape consistent for downstream batching.</span>

---

## <span style="font-size: 16px;">Paper Context and Design Decisions</span>

<span style="font-size: 14px;">Mikolov et al. introduced Skip-gram in "Efficient Estimation of Word Representations in Vector Space" (2013) and refined the training in "Distributed Representations of Words and Phrases and their Compositionality" (2013). The first paper proposed the architecture; the second made it practical on billion-word corpora through negative sampling and subsampling of frequent words.</span>

<span style="font-size: 14px;">The pair stream sits upstream of those tricks. The paper describes the training objective as a sum over context offsets within a window, which is exactly the set of pairs this problem produces. Two design choices in the original work are worth tracing:</span>

* <span style="font-size: 14px;">**Subsampling of frequent words.** Before pairs are generated, very frequent words (like "the", "a") are randomly discarded with a probability tied to their frequency. This both speeds up training and shifts the effective window, since discarding a word lets more distant words become neighbors. This problem operates on the token ids as given and does not subsample, keeping the mapping deterministic.</span>
* <span style="font-size: 14px;">**Negative sampling.** Rather than a full softmax over the vocabulary for each pair, the paper draws a handful of "negative" words per positive pair and trains a binary classifier to separate the true context word from the negatives. The positive pairs fed into negative sampling are precisely the $(center, context)$ pairs generated here.</span>

<span style="font-size: 14px;">The authors found Skip-gram with negative sampling to be the best speed-quality trade-off, and it became the default for downstream word2vec usage. Understanding pair generation makes the rest of the pipeline (subsampling, negative sampling, the embedding update) easy to reason about, because everything downstream consumes this pair stream.</span>

---

## <span style="font-size: 16px;">Complexity</span>

<span style="font-size: 14px;">Each center position contributes at most $2c$ pairs (the full window minus the center). For a sequence of length $n$ the total number of pairs is bounded by $2cn$, and is exactly $2cn$ once away from the boundaries. The time complexity to generate all pairs is therefore $O(n \cdot c)$, linear in both the sequence length and the window size.</span>

<span style="font-size: 14px;">Memory is $O(n \cdot c)$ as well, since every pair is materialized into the output tensor. In a real training pipeline pairs are usually streamed rather than stored, but for this problem the full $(N, 2)$ tensor is returned so it can be checked exactly.</span>

<span style="font-size: 14px;">The exact count of pairs is useful as a sanity check. For an interior position (one where the full window fits), the position contributes $2c$ pairs. Boundary positions contribute fewer: position 0 contributes $\min(c, n-1)$ pairs, position 1 contributes $\min(c, 1) + \min(c, n-2)$, and so on. Summing across all positions gives the total $N$. When $c \ge n - 1$, the window covers the whole sequence from every position, so each of the $n$ centers pairs with all $n - 1$ other tokens, yielding exactly $n(n-1)$ pairs. This is why a window larger than the sequence behaves like a dense all-pairs enumeration.</span>

---

## <span style="font-size: 16px;">Worked Example</span>

<span style="font-size: 14px;">Take token ids $[5, 6, 7]$ with window $c = 2$. The sequence length is $n = 3$.</span>

<span style="font-size: 14px;">1. **Center at position 0 (token 5):** window is $\max(0, -2) = 0$ to $\min(2, 2) = 2$, so positions 0, 1, 2. Exclude 0. Emit $(5, 6)$ from position 1 and $(5, 7)$ from position 2.</span>

<span style="font-size: 14px;">2. **Center at position 1 (token 6):** window is positions 0 to 2. Exclude 1. Emit $(6, 5)$ then $(6, 7)$.</span>

<span style="font-size: 14px;">3. **Center at position 2 (token 7):** window is positions 0 to 2. Exclude 2. Emit $(7, 5)$ then $(7, 6)$.</span>

<span style="font-size: 14px;">The final tensor, in center-then-context order, is:</span>

$$
\begin{pmatrix} 5 & 6 \ 5 & 7 \ 6 & 5 \ 6 & 7 \ 7 & 5 \ 7 & 6 \end{pmatrix}
$$

<span style="font-size: 14px;">Six pairs total, matching the bound $2cn$ clamped by the short sequence. Note that with $c = 2 \ge n - 1$ the window covers the whole sequence, so every ordered pair of distinct positions appears.</span>

---

## <span style="font-size: 16px;">Modern Context</span>

<span style="font-size: 14px;">Skip-gram pairs are the conceptual ancestor of the training signal used by many later representation learners. The core idea, turning co-occurrence into a stream of positive pairs and contrasting them against negatives, reappears across modern machine learning:</span>

* <span style="font-size: 14px;">**GloVe** (Pennington et al., 2014) reformulates the same co-occurrence signal as a weighted least-squares regression on a global word-word count matrix, but it captures the same windowed neighborhoods.</span>
* <span style="font-size: 14px;">**Node2vec and DeepWalk** apply Skip-gram directly to sequences of nodes produced by random walks on a graph, treating walks as sentences and nodes as words.</span>
* <span style="font-size: 14px;">**Contrastive learning** in vision and multimodal models generalizes the positive-pair-versus-negatives idea that negative sampling first popularized for word2vec.</span>

<span style="font-size: 14px;">Transformer language models replaced static word2vec embeddings with contextual representations, but the windowed co-occurrence intuition still underlies how those models learn: nearby tokens shape each other's representations. The pair generation step here is the minimal, transparent version of that signal.</span>

---

## <span style="font-size: 16px;">Emission Order</span>

<span style="font-size: 14px;">Pairs are emitted in a fixed deterministic order: **center position ascending, then context position ascending**. The outer loop walks center positions $0, 1, \ldots, n-1$; the inner loop walks the clamped window left to right, skipping the center. This ordering matters because the output is compared exactly. Any other order (for example contexts emitted right-to-left, or grouping all left contexts before right contexts) produces the same set of pairs but a different tensor, which would fail an exact equality check.</span>

---

## <span style="font-size: 16px;">Pitfalls</span>

* <span style="font-size: 14px;">**Including the self-pair.** Forgetting the $j \ne i$ check pairs each center with itself. The objective explicitly excludes $j = 0$, and a center-context pair where both are the same word carries no co-occurrence information.</span>
* <span style="font-size: 14px;">**Off-by-one on the window.** Using a strict upper bound (a range that stops at $i + c$ exclusive, or comparing with $<$ instead of $\le$) drops the farthest context word on the right. The window is inclusive on both ends: positions $i - c$ through $i + c$.</span>
* <span style="font-size: 14px;">**Wrapping or negative indexing at boundaries.** Computing context indices without clamping lets a negative left index wrap to the end of the sequence (Python negative indexing) or a modular index loop the sequence into a circle. Both invent pairs that span the sentence boundary. Always clamp with $\max(0, i-c)$ and $\min(n-1, i+c)$.</span>
* <span style="font-size: 14px;">**Reversing the pair.** Emitting $(\text{context}, \text{center})$ instead of $(\text{center}, \text{context})$ swaps the columns. For Skip-gram the input is the center and the target is the context, so column 0 must be the center.</span>
* <span style="font-size: 14px;">**Wrong dtype.** Token ids are discrete indices, so the output must be an integer tensor (int64). Returning a float tensor breaks downstream embedding lookups, which require integer indices.</span>

---

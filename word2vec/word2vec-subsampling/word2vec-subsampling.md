# <span style="font-size: 20px;">Frequent-Word Subsampling</span>

<span style="font-size: 14px;">Frequent-word subsampling is the preprocessing trick from Mikolov et al. (2013), "Distributed Representations of Words and Phrases and their Compositionality", that randomly discards very common words during Skip-gram training. Words like "the", "a", and "of" appear millions of times yet carry almost no useful co-occurrence signal, so the authors keep each occurrence with a probability that shrinks as the word becomes more frequent.</span>

---

## <span style="font-size: 16px;">Why Frequent Words Hurt Training</span>

<span style="font-size: 14px;">Word2Vec learns embeddings by predicting context words from a center word (Skip-gram) over a sliding window. The number of training pairs a word generates is roughly proportional to how often it appears in the corpus. This creates two problems for the most common words.</span>

* <span style="font-size: 14px;">**Weak signal.** The co-occurrence of "France" and "Paris" is informative: it tells the model something specific about meaning. The co-occurrence of "the" and "Paris" tells the model almost nothing, because "the" appears next to nearly every noun. Frequent function words do not help distinguish one context from another.</span>
* <span style="font-size: 14px;">**Gradient domination.** Because "the" may account for several percent of all tokens, it participates in a huge fraction of training pairs. Its embedding receives orders of magnitude more updates than a rare but meaningful word, so the optimizer spends most of its effort on words that need it least.</span>

<span style="font-size: 14px;">The paper observes that "the vector representations of frequent words do not change significantly after training on several million examples." In other words, extra exposure to "the" is wasted compute. Subsampling redirects that compute toward rarer, more informative words and, as a side effect, lets the effective context window reach further across the meaningful words that remain.</span>

---

## <span style="font-size: 16px;">The Keep-Probability Formula</span>

<span style="font-size: 14px;">Let $\text{count}(w)$ be the number of times word $w$ occurs in the corpus and let $N = \sum_w \text{count}(w)$ be the total token count. The frequency of $w$ is:</span>

$$
f(w) = \frac{\text{count}(w)}{N}
$$

<span style="font-size: 14px;">Each occurrence of $w$ is then kept with probability:</span>

$$
P_{\text{keep}}(w) = \min\!\left(1, \sqrt{\frac{t}{f(w)}}\right)
$$

<span style="font-size: 14px;">where:</span>

* <span style="font-size: 14px;">$t$ is a chosen threshold, typically around $10^{-5}$ for large corpora</span>
* <span style="font-size: 14px;">$f(w)$ is the relative frequency, a number in $(0, 1]$ that sums to 1 across the vocabulary</span>
* <span style="font-size: 14px;">the $\min$ with 1 caps the probability so it never exceeds a valid probability</span>

<span style="font-size: 14px;">The original paper states the rule as discarding word $w_i$ with probability $P(w_i) = 1 - \sqrt{t / f(w_i)}$. Keeping is the complement, so $P_{\text{keep}}(w) = \sqrt{t / f(w)}$, clamped at 1. Both phrasings describe the same operation. This problem computes the keep-probability directly.</span>

---

## <span style="font-size: 16px;">Reading Each Term</span>

<span style="font-size: 14px;">The behavior of the formula is easiest to understand by splitting the vocabulary at the threshold $t$.</span>

* <span style="font-size: 14px;">**Rare words ($f(w) \le t$).** Here $t / f(w) \ge 1$, so $\sqrt{t / f(w)} \ge 1$ and the $\min$ clamps the keep-probability to exactly 1. Every occurrence of a rare word is kept. Subsampling never throws away signal from words that are already scarce.</span>
* <span style="font-size: 14px;">**Frequent words ($f(w) > t$).** Now $t / f(w) < 1$, so the keep-probability drops below 1. The more frequent the word, the smaller the ratio, and the more aggressively occurrences are dropped.</span>

<span style="font-size: 14px;">The threshold $t$ acts as a soft cutoff: words below it are untouched, words above it are thinned in proportion to how far above they sit.</span>

---

## <span style="font-size: 16px;">Why the Square Root</span>

<span style="font-size: 14px;">A natural alternative would be to keep words with probability $t / f(w)$, with no square root. That decays too fast. If "the" has frequency $f = 5 \times 10^{-2}$ and $t = 10^{-5}$, then $t / f = 2 \times 10^{-4}$, so only one in five thousand occurrences survives. That is so aggressive it can erase a word almost entirely and starve nearby words of context.</span>

<span style="font-size: 14px;">The square root softens the decay. Under $\sqrt{t / f}$, the same "the" is kept with probability $\sqrt{2 \times 10^{-4}} \approx 0.014$, about one in seventy occurrences. Frequent words are still heavily thinned, but not annihilated. The paper describes the formula as "heuristically chosen" because it "aggressively subsamples words whose frequency is greater than $t$ while preserving the ranking of the frequencies." The square root keeps the relative ordering of frequencies intact while compressing their dynamic range.</span>

<span style="font-size: 14px;">There is also a useful scaling property. If one word is four times as frequent as another (and both are above $t$), its keep-probability is only half as large, since $\sqrt{1/4} = 1/2$. The square root turns a multiplicative gap in frequency into a smaller multiplicative gap in keep-probability. A linear rule like $t/f$ would instead turn that same four-times frequency gap into a four-times difference in keep-probability, magnifying rather than dampening the imbalance the technique is meant to reduce.</span>

---

## <span style="font-size: 16px;">Effect on Speed and Embedding Quality</span>

<span style="font-size: 14px;">Subsampling has two reinforcing effects reported in the paper.</span>

* <span style="font-size: 14px;">**Faster training.** Dropping a large share of the most common tokens shrinks the number of training pairs substantially. Mikolov et al. report speedups of roughly 2x to 10x depending on the threshold and corpus.</span>
* <span style="font-size: 14px;">**Better rare-word vectors.** With fewer "the"-style pairs flooding the gradient, the optimizer allocates more updates to informative words. The paper reports "significant improvement in the accuracy of the learned vectors of the rare words" on their analogy benchmark.</span>
* <span style="font-size: 14px;">**Better frequent-word vectors too.** Counterintuitively, thinning common words can also sharpen their own embeddings. Their representations had already converged from over-exposure, and removing redundant updates leaves the few retained occurrences in more informative contexts (since neighboring function words were also dropped), so the signal-to-noise ratio of each surviving pair improves.</span>

<span style="font-size: 14px;">A subtle bonus is window widening. When intervening function words are dropped, the surviving context words sit closer together inside the sliding window, so meaningful words that were just outside the window can now co-occur. This lets a fixed window capture longer-range semantic relationships.</span>

---

## <span style="font-size: 16px;">How It Fits Into Skip-gram</span>

<span style="font-size: 14px;">Subsampling is a corpus preprocessing step, applied before any embedding update. Understanding where it sits in the pipeline clarifies why it is computed once, up front.</span>

<span style="font-size: 14px;">1. **Count pass**: scan the corpus once and tally $\text{count}(w)$ for every word, plus the grand total $N$.</span>

<span style="font-size: 14px;">2. **Probability pass**: compute $P_{\text{keep}}(w)$ for each word in the vocabulary using the formula above. This is a one-time vector operation over the vocabulary, not over the corpus, so it is cheap.</span>

<span style="font-size: 14px;">3. **Streaming pass**: walk the corpus token by token. For each occurrence of word $w$, draw a uniform random number $r \in [0, 1)$ and keep the token only if $r < P_{\text{keep}}(w)$. Dropped tokens are removed before the sliding window forms training pairs.</span>

<span style="font-size: 14px;">Because the keep-probability depends only on global frequency, it is identical for every occurrence of a given word. Two occurrences of "the" are equally likely to be dropped, independently of position. The randomness lives in the third pass; this problem isolates the deterministic second pass, which is the piece that has to be numerically exact.</span>

---

## <span style="font-size: 16px;">Choosing the Threshold $t$</span>

<span style="font-size: 14px;">The threshold $t$ is the single knob that controls how aggressive subsampling is. It is the frequency at which a word transitions from "always kept" to "partially dropped".</span>

* <span style="font-size: 14px;">**Smaller $t$ (for example $10^{-6}$)** moves the cutoff lower, so more words qualify as "frequent" and get thinned, and even moderately common words are subsampled. This maximizes speedup but risks removing useful mid-frequency words.</span>
* <span style="font-size: 14px;">**Larger $t$ (for example $10^{-3}$)** raises the cutoff, so only the very most common words are touched and the corpus is barely thinned. This is gentler but yields a smaller speedup.</span>

<span style="font-size: 14px;">The paper reports that a value around $t = 10^{-5}$ works well for the large news corpus they trained on. The right value scales with corpus size and vocabulary distribution: a corpus where one word dominates needs a different cutoff than a flatter distribution. Because the formula preserves frequency ranking for any positive $t$, sweeping $t$ changes how much is dropped without reshuffling which words are considered most common.</span>

---

## <span style="font-size: 16px;">Comparison With Simpler Strategies</span>

* <span style="font-size: 14px;">**No subsampling.** Every token trains. This wastes compute on function words and lets their gradients dominate, exactly the failure mode the technique fixes.</span>
* <span style="font-size: 14px;">**Hard stop-word list.** Deleting a fixed list of words (the classic stop-word approach) is blunt: it treats every listed word as worthless and every other word as fully kept, with no gradation. It also requires a hand-curated list per language. Subsampling is frequency-driven, language-agnostic, and probabilistic, so a moderately frequent word is only partially thinned rather than fully removed.</span>
* <span style="font-size: 14px;">**Hard frequency cutoff.** Discarding any word above a count threshold is again all-or-nothing. The square-root rule instead provides a smooth probability that preserves frequency ranking, which the paper argues is important.</span>

---

## Worked Example ($t = 10^{-5}$)

<span style="font-size: 14px;">Take a toy corpus with three words and counts $[100, 50, 10]$. The total is $N = 160$.</span>

<span style="font-size: 14px;">1. **Frequencies**: $f = [100/160, 50/160, 10/160] = [0.625, 0.3125, 0.0625]$.</span>

<span style="font-size: 14px;">2. **Ratios $t / f$**: with $t = 10^{-5}$, these are $[1.6 \times 10^{-5}, 3.2 \times 10^{-5}, 1.6 \times 10^{-4}]$.</span>

<span style="font-size: 14px;">3. **Square roots**: $\sqrt{t/f} = [0.004, 0.005657, 0.012649]$ (rounded).</span>

<span style="font-size: 14px;">4. **Clamp at 1**: all three are already below 1, so $P_{\text{keep}} = [0.004, 0.005657, 0.012649]$.</span>

<span style="font-size: 14px;">The most frequent word is kept only about 0.4 percent of the time, while the least frequent of the three survives roughly three times as often. Notice how the keep-probabilities track the frequencies: word 1 is twice as frequent as word 2, and its keep-probability ($0.004$) is about $1/\sqrt{2} \approx 0.707$ times that of word 2 ($0.005657$), exactly the square-root scaling described above. Now contrast a rare word: if its frequency were $f = 10^{-6}$ (below $t$), then $t/f = 10$ and $\sqrt{10} \approx 3.16$, which the $\min$ clamps to 1, so every occurrence is kept.</span>

<span style="font-size: 14px;">As a second check, consider four words with equal counts $[25, 25, 25, 25]$. Each has frequency $f = 0.25$, so each keep-probability is $\sqrt{10^{-5} / 0.25} = \sqrt{4 \times 10^{-5}} \approx 0.006325$. Equal-frequency words receive identical keep-probabilities, which confirms the formula depends only on relative frequency and treats symmetric inputs symmetrically.</span>

---

## <span style="font-size: 16px;">Implementation Notes</span>

<span style="font-size: 14px;">The computation is a short, fully vectorized pipeline over the count tensor.</span>

* <span style="font-size: 14px;">Cast counts to floating point before dividing, otherwise integer division produces zeros and the frequencies collapse.</span>
* <span style="font-size: 14px;">Compute the total with a single reduction over the whole vector, not per-element loops.</span>
* <span style="font-size: 14px;">Form $f = \text{counts} / \text{total}$, then $\sqrt{t / f}$ elementwise, then clamp the maximum to 1.</span>
* <span style="font-size: 14px;">Use double precision when the dynamic range is large. With tiny $t$ and large counts the ratio $t / f$ can be very small, and single precision may lose accuracy in the square root.</span>

<span style="font-size: 14px;">In practice Word2Vec applies the keep-probability per occurrence by drawing a uniform random number and dropping the token if it exceeds $P_{\text{keep}}$. This problem stops at computing the deterministic per-word probabilities, which is the part that must be exactly correct before any sampling happens.</span>

---

## <span style="font-size: 16px;">Pitfalls</span>

* <span style="font-size: 14px;">**Forgetting to clamp at 1.** Without the $\min$, rare words with $f(w) < t$ get a "probability" greater than 1, which is meaningless and, after sampling, would behave like always-keep but corrupt any downstream arithmetic that assumes a valid probability. The clamp is what makes rare words safe.</span>
* <span style="font-size: 14px;">**Dropping the square root.** Using $t / f$ instead of $\sqrt{t / f}$ subsamples far too aggressively and can wipe out frequent words almost entirely, starving their neighbors of context. The square root is the whole point of the heuristic.</span>
* <span style="font-size: 14px;">**Confusing keep-probability with discard-probability.** The paper writes the rule as a discard probability $1 - \sqrt{t/f}$. Returning $1 - \sqrt{t/f}$ when keep is expected inverts the behavior, keeping common words and dropping rare ones.</span>
* <span style="font-size: 14px;">**Integer division.** Computing $\text{count} / N$ in integer arithmetic yields 0 for every word except possibly one, producing garbage frequencies. Always convert counts to float first.</span>
* <span style="font-size: 14px;">**Precision loss with extreme ratios.** With a tiny threshold and a heavily dominant word, the ratio $t / f$ can be on the order of $10^{-9}$ or smaller. In single precision the square root of such a value can lose meaningful digits, so use double precision when correctness at small probabilities matters.</span>

---

## What Is Perplexity?

Perplexity measures how "surprised" a language model is by a sequence of text. A model that assigns high probability to the actual words has low perplexity; a model that assigns low probability has high perplexity.

Mathematically, perplexity is the exponential of the average negative log-likelihood:

$$
PP = \exp\left(-\frac{1}{N} \sum_{i=1}^{N} \log P(w_i | \text{context})\right)
$$

Lower perplexity means the model predicts the text better.

---

## Intuition: Effective Vocabulary Size

Perplexity can be interpreted as the effective number of equally likely choices the model considers at each position.

**Perplexity = 10:** On average, the model is as uncertain as if it were choosing uniformly among 10 words at each position.

**Perplexity = 100:** Like choosing among 100 equally likely words.

**Perplexity = 1:** The model is certain. It always assigns probability 1 to the correct word.

A vocabulary of 50,000 words with uniform predictions would give perplexity 50,000. Good language models achieve perplexity in the range of 20-100 on standard benchmarks.

---

## The Computation Step by Step

**Given:**
- A sequence of tokens: $[t_1, t_2, ..., t_N]$
- Probability distributions from the model: $[P_1, P_2, ..., P_N]$
- Each $P_i$ is a distribution over the vocabulary

**Step 1: Extract probabilities for actual tokens**

For each position $i$, find the probability the model assigned to the token that actually occurred:

$$
p_i = P_i[t_i]
$$

**Step 2: Compute log probabilities**

Take the natural log of each probability:

$$
\log p_i
$$

Since probabilities are between 0 and 1, log probabilities are negative.

**Step 3: Average the negative log probabilities (cross-entropy)**

$$
H = -\frac{1}{N} \sum_{i=1}^{N} \log p_i
$$

This is the cross-entropy between the model's predictions and the actual sequence.

**Step 4: Exponentiate**

$$
PP = e^H
$$

---

## A Numerical Example

**Sequence:** "The cat sat" (3 tokens)

**Model predictions:**

Position 1 ("The"): model gave P("The") = 0.1
Position 2 ("cat"): model gave P("cat") = 0.05
Position 3 ("sat"): model gave P("sat") = 0.02

**Log probabilities:**
- log(0.1) = -2.303
- log(0.05) = -2.996
- log(0.02) = -3.912

**Cross-entropy:**

$$
H = -\frac{1}{3}(-2.303 - 2.996 - 3.912) = \frac{9.211}{3} = 3.07
$$

**Perplexity:**

$$
PP = e^{3.07} = 21.5
$$

The model has perplexity 21.5 on this sequence. On average, it is as uncertain as choosing among about 22 equally likely words.

---

## Perplexity and Bits

Perplexity is closely related to information-theoretic quantities:

**Cross-entropy in bits** (using log base 2):

$$
H_{bits} = -\frac{1}{N} \sum_{i=1}^{N} \log_2 P(w_i)
$$

**Perplexity:**

$$
PP = 2^{H_{bits}}
$$

If the cross-entropy is 5 bits, perplexity is $2^5 = 32$.

This connects to compression: a model with perplexity $PP$ can encode the text using about $\log_2(PP)$ bits per word.

---

## Why Perplexity Matters

**Model comparison:**
Lower perplexity generally means a better model. Comparing perplexity on the same test set ranks models by their predictive quality.

**Early stopping:**
Monitor validation perplexity during training. Stop when it starts increasing to prevent overfitting.

**Hyperparameter tuning:**
Choose hyperparameters that minimize perplexity on held-out data.

**Progress tracking:**
Language model improvements over the years are often reported as perplexity reductions. GPT-2 achieved perplexity ~35 on WikiText-103; GPT-3 reduced it further.

---

## Important Considerations

**Vocabulary matters:**
A model with a smaller vocabulary will have lower perplexity on the same text. Always compare models with the same vocabulary or normalize appropriately.

**Subword tokenization:**
Modern models use BPE or SentencePiece, which affects the number of tokens $N$. Perplexity per word vs. per subword differs.

**Out-of-vocabulary (OOV) words:**
If a word is not in the vocabulary, the model might assign zero probability, making perplexity infinite. Handle OOV carefully.

**Domain mismatch:**
A model trained on news will have high perplexity on medical text. Perplexity measures how well the model fits that specific data distribution.

---

## Perplexity Is Not Everything

**Perplexity does not capture:**
- Fluency vs. factual accuracy
- Coherence over long passages
- Following instructions or prompts
- Safety and bias issues

Two models with the same perplexity can have very different practical qualities. Perplexity is necessary but not sufficient for evaluating language models.

---

## Numerical Stability

Computing products of many small probabilities can underflow. Always work in log space:

**Unstable:**

$$
PP = \left(\prod_i p_i\right)^{-1/N}
$$

**Stable:**

$$
PP = \exp\left(-\frac{1}{N} \sum_i \log p_i\right)
$$

The sum of logs is computed in a numerically stable way, then exponentiated once at the end.
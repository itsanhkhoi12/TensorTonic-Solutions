## The Ranking Problem

In information retrieval and recommendation, we often rank items by relevance. Unlike classification (relevant or not), ranking cares about **order**: showing the best items first matters more than showing them at all.

**Example:** A search engine returns 10 results. If the most relevant result is at position 10, the user might never see it. The same result at position 1 is much more valuable.

NDCG (Normalized Discounted Cumulative Gain) measures ranking quality, giving more credit to relevant items appearing earlier.

---

## Relevance Scores

Each item has a **relevance score** indicating how useful it is. Common scales:

**Binary:** 0 (not relevant) or 1 (relevant)

**Graded:** 0 (not relevant), 1 (somewhat relevant), 2 (relevant), 3 (highly relevant)

Higher scores mean more relevant. The scores come from human judgments or user behavior data.

---

## Cumulative Gain (CG)

The simplest metric: just sum the relevance scores of the top $k$ results.

$$
\text{CG}_k = \sum_{i=1}^{k} rel_i
$$

where $rel_i$ is the relevance of the item at position $i$.

**Problem:** CG does not consider position. Ranking [3, 2, 1] and [1, 2, 3] have the same CG, but the first is clearly better.

---

## Discounted Cumulative Gain (DCG)

DCG adds a **position discount**: items appearing later contribute less.

$$
\text{DCG}_k = \sum_{i=1}^{k} \frac{rel_i}{\log_2(i + 1)}
$$

The denominator $\log_2(i + 1)$ increases with position, reducing the contribution of later items.

**Position discounts:**
- Position 1: $\log_2(2) = 1$ (no discount)
- Position 2: $\log_2(3) \approx 1.58$
- Position 3: $\log_2(4) = 2$
- Position 4: $\log_2(5) \approx 2.32$
- Position 10: $\log_2(11) \approx 3.46$

An item at position 1 contributes its full relevance. The same item at position 10 contributes only about 29% of its relevance.

---

## Alternative DCG Formula

Some implementations use an alternative that more heavily penalizes later positions:

$$
\text{DCG}_k = \sum_{i=1}^{k} \frac{2^{rel_i} - 1}{\log_2(i + 1)}
$$

The numerator $2^{rel_i} - 1$ gives exponentially more weight to higher relevance scores:
- $rel = 0$: $2^0 - 1 = 0$
- $rel = 1$: $2^1 - 1 = 1$
- $rel = 2$: $2^2 - 1 = 3$
- $rel = 3$: $2^3 - 1 = 7$

This version is common in practice and emphasizes highly relevant items.

---

## Worked Example: DCG

Ranking with relevance scores: [3, 2, 0, 1, 2]

Using the standard formula:

Position 1: $3 / \log_2(2) = 3 / 1 = 3.0$

Position 2: $2 / \log_2(3) = 2 / 1.585 = 1.26$

Position 3: $0 / \log_2(4) = 0 / 2 = 0$

Position 4: $1 / \log_2(5) = 1 / 2.32 = 0.43$

Position 5: $2 / \log_2(6) = 2 / 2.58 = 0.77$

$\text{DCG}_5 = 3.0 + 1.26 + 0 + 0.43 + 0.77 = 5.46$

---

## Ideal DCG (IDCG)

DCG depends on the specific relevance scores available. To make it comparable across queries, we normalize by the **best possible DCG**.

IDCG is the DCG of the ideal ranking: all items sorted by relevance in descending order.

**Same items sorted optimally:** [3, 2, 2, 1, 0]

Position 1: $3 / 1 = 3.0$

Position 2: $2 / 1.585 = 1.26$

Position 3: $2 / 2 = 1.0$

Position 4: $1 / 2.32 = 0.43$

Position 5: $0 / 2.58 = 0$

$\text{IDCG}_5 = 3.0 + 1.26 + 1.0 + 0.43 + 0 = 5.69$

---

## Normalized DCG (NDCG)

NDCG is DCG divided by IDCG:

$$
\text{NDCG}_k = \frac{\text{DCG}_k}{\text{IDCG}_k}
$$

**From our example:**

$\text{NDCG}_5 = 5.46 / 5.69 = 0.96$

The ranking achieves 96% of the ideal DCG. It is nearly optimal.

---

## NDCG Properties

**Range:** 0 to 1

**NDCG = 1:** Perfect ranking. Items are ordered exactly by relevance.

**NDCG = 0:** All items have zero relevance (or the ranking is maximally bad).

**Position sensitivity:** Moving a relevant item from position 10 to position 1 significantly increases NDCG.

**Graded relevance:** Unlike precision/recall (binary), NDCG handles graded relevance naturally.

---

## NDCG at k (NDCG@k)

In practice, users only look at the top few results. NDCG@k measures quality of the top $k$ positions only.

**NDCG@1:** Quality of the top result only

**NDCG@5:** Quality of top 5 results

**NDCG@10:** Common for web search evaluation

Different values of $k$ can give different insights:
- NDCG@1 might be low but NDCG@10 high (best item not first, but in top 10)
- NDCG@1 high but NDCG@10 low (first item great, rest poor)

---

## Handling Missing Relevance Scores

If some items in the ranking have no relevance judgment:
- Option 1: Treat unknown relevance as 0
- Option 2: Ignore unjudged items (shift positions up)
- Option 3: Use estimated relevance

The choice depends on the evaluation scenario.

---

## NDCG vs. Other Ranking Metrics

**Mean Average Precision (MAP):**
- Binary relevance only
- Focuses on recall (finding all relevant items)
- Less sensitive to exact position

**Mean Reciprocal Rank (MRR):**
- Only cares about the first relevant item
- Ignores everything after position of first hit

**NDCG advantages:**
- Handles graded relevance
- Position-sensitive throughout the ranking
- Industry standard for recommendation and search

---

## Applications

**Search engines:**
Evaluating result quality for queries.

**Recommendation systems:**
Measuring how well the top-N recommendations match user preferences.

**Learning to rank:**
NDCG is a common optimization target for ranking models.

**A/B testing:**
Comparing different ranking algorithms on real user data.

---

## Computing NDCG in Practice

**Step 1:** Get relevance scores for all items (from labels or user feedback)

**Step 2:** Compute DCG of the actual ranking

**Step 3:** Sort items by relevance to get ideal ordering

**Step 4:** Compute IDCG of ideal ranking

**Step 5:** Divide DCG by IDCG

**Step 6:** Average NDCG across multiple queries for overall evaluation
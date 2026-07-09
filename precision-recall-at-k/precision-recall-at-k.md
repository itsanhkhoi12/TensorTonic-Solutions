## What Are Precision and Recall at K?

Precision@K and Recall@K are ranking metrics that evaluate how well a recommender system places relevant items in the top-K positions.

**Precision@K:** Of the K items recommended, what fraction are relevant?

**Recall@K:** Of all relevant items, what fraction appear in the top-K?

These metrics are borrowed from information retrieval and adapted for recommendation evaluation.

---

## Precision at K Formula

$$
\text{Precision@K} = \frac{|\{\text{relevant items in top-K}\}|}{K} = \frac{|R_K \cap T|}{K}
$$

where:
- $R_K$ is the set of top-K recommended items
- $T$ is the set of truly relevant items

**Range:** 0 to 1 (or 0% to 100%)

---

## Recall at K Formula

$$
\text{Recall@K} = \frac{|\{\text{relevant items in top-K}\}|}{|\{\text{all relevant items}\}|} = \frac{|R_K \cap T|}{|T|}
$$

**Range:** 0 to 1 (or 0% to 100%)

---

## Worked Example

**User's relevant items (ground truth):** {A, B, C, D, E} (5 items)

**Top-10 recommendations:** {A, X, B, Y, Z, C, W, V, U, T}

**Relevant items in top-10:** {A, B, C} (3 items)

**Precision@10:**

$$
\text{Precision@10} = \frac{3}{10} = 0.30 = 30\%
$$

30% of recommendations were relevant.

**Recall@10:**

$$
\text{Recall@10} = \frac{3}{5} = 0.60 = 60\%
$$

60% of relevant items were recommended in top-10.

---

## Precision and Recall at Different K

**Top-5 recommendations:** {A, X, B, Y, Z}

Relevant in top-5: {A, B} (2 items)

- Precision@5 = 2/5 = 0.40
- Recall@5 = 2/5 = 0.40

**Top-3 recommendations:** {A, X, B}

Relevant in top-3: {A, B} (2 items)

- Precision@3 = 2/3 = 0.67
- Recall@3 = 2/5 = 0.40

**Observation:**

- Precision can increase or decrease with K
- Recall always increases or stays same as K increases

---

## The Precision-Recall Tradeoff

As K increases:

**Recall tends to increase:**

More chances to include relevant items.

**Precision tends to decrease:**

Including more items means more irrelevant ones too.

This tradeoff is fundamental to information retrieval and recommendation.

---

## Average Precision and Recall

Compute precision and recall for each user, then average:

$$
\text{Mean Precision@K} = \frac{1}{|U|} \sum_{u \in U} \text{Precision@K}_u
$$

$$
\text{Mean Recall@K} = \frac{1}{|U|} \sum_{u \in U} \text{Recall@K}_u
$$

This gives system-level metrics across all users.

---

## What Counts as Relevant?

**Explicit relevance:**

- Items the user rated 4 or 5 stars
- Items the user added to favorites

**Implicit relevance:**

- Items the user clicked on
- Items the user purchased
- Items the user watched completely

**Future interactions:**

In train/test splits, relevant = items the user interacted with in the test set.

---

## Handling Users with No Relevant Items

If a user has no relevant items in the test set:

**Option 1:** Exclude them from the average

**Option 2:** Assign precision = 0, recall = undefined (or 0)

Clearly document which approach is used.

---

## Handling Users with Few Relevant Items

If a user has only 2 relevant items:

- Maximum possible Recall@10 = 2/2 = 1.0
- If K > |T|, Recall@K can reach 1.0 easily

**Normalization:**

Some formulations cap K at the number of relevant items:

$$
\text{Precision@K} = \frac{|R_K \cap T|}{\min(K, |T|)}
$$

---

## Precision-Recall Curves

Plot precision vs recall as K varies:

**Points on the curve:**

- K=1: (Recall@1, Precision@1)
- K=2: (Recall@2, Precision@2)
- ...
- K=N: (Recall@N, Precision@N)

**Ideal curve:** High precision at all recall levels (upper right corner).

**Poor curve:** Precision drops quickly as recall increases.

---

## F1 Score at K

Harmonic mean of precision and recall:

$$
\text{F1@K} = 2 \cdot \frac{\text{Precision@K} \cdot \text{Recall@K}}{\text{Precision@K} + \text{Recall@K}}
$$

F1 balances both metrics in a single number.

**F1@10 for our example:**

$$
\text{F1@10} = 2 \cdot \frac{0.30 \cdot 0.60}{0.30 + 0.60} = 2 \cdot \frac{0.18}{0.90} = 0.40
$$

---

## Mean Average Precision (MAP)

Average precision across all relevant positions:

$$
\text{AP} = \frac{1}{|T|} \sum_{k=1}^{K} \text{Precision@k} \cdot \text{rel}(k)
$$

where $\text{rel}(k) = 1$ if item at position $k$ is relevant.

**MAP = mean of AP across users.**

MAP rewards placing relevant items early, not just anywhere in top-K.

---

## Normalized Discounted Cumulative Gain (NDCG)

A related metric that also considers position:

$$
\text{DCG@K} = \sum_{k=1}^{K} \frac{\text{rel}(k)}{\log_2(k+1)}
$$

Items at earlier positions contribute more. NDCG normalizes by ideal DCG.

NDCG is more sensitive to ranking order than precision/recall.

---

## Choosing K

**K depends on the application:**

- Mobile screen: K = 3-5 (limited space)
- Web page: K = 10-20
- Email digest: K = 5-10

**Report multiple K values:**

Precision@1, @5, @10, @20 gives a fuller picture.

---

## Precision@K vs Hit Rate@K

**Precision@K:**

Fraction of top-K that are relevant.

**Hit Rate@K:**

Binary: Is at least one relevant item in top-K?

Hit rate is less granular. Precision distinguishes 1 hit from 5 hits in top-10.

---

## Interpretation

**Precision@10 = 0.3:**

"30% of our top-10 recommendations were items the user actually wanted."

**Recall@10 = 0.6:**

"We successfully recommended 60% of the items the user wanted within the top 10."

**Both matter:**

High precision = few irrelevant recommendations
High recall = few missed relevant items

---

## Micro vs Macro Averaging

**Micro-average:**

Pool all users' recommendations, compute precision/recall on the pool.

$$
\text{Precision}_{micro} = \frac{\sum_u |R_K^u \cap T_u|}{\sum_u K}
$$

**Macro-average:**

Compute per-user, then average.

$$
\text{Precision}_{macro} = \frac{1}{|U|} \sum_u \text{Precision@K}_u
$$

Macro-average treats all users equally. Micro-average weights by user activity.
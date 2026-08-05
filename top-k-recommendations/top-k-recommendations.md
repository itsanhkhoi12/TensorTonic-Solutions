## What Are Top-K Recommendations?

Top-K recommendations are the K highest-scoring items presented to a user. The recommendation system computes a score for each candidate item, ranks them by score, and returns the top K.

$$
R_K(u) = \text{argmax}_{S \subset I, |S|=K} \sum_{i \in S} \text{score}(u, i)
$$

In practice, this is simply: sort items by score, take the top K.

---

## The Scoring Function

Different algorithms use different scoring functions:

**Collaborative filtering:**

$$
\text{score}(u, i) = \hat{r}_{ui} = \text{predicted rating}
$$

**Content-based:**

$$
\text{score}(u, i) = \text{sim}(\text{user profile}, \text{item features})
$$

**Matrix factorization:**

$$
\text{score}(u, i) = \mathbf{p}_u^T \mathbf{q}_i
$$

**Hybrid:**

$$
\text{score}(u, i) = \alpha \cdot \text{CF score} + \beta \cdot \text{content score}
$$

---

## The Selection Process

**Step 1:** Identify candidate items

- All items not yet rated by the user, or
- A filtered subset (available items, items in user's region, etc.)

**Step 2:** Compute scores for candidates

**Step 3:** Sort by score (descending)

**Step 4:** Select top K

**Step 5:** Optionally apply business rules or diversity constraints

---

## Worked Example

**User U's candidate items with predicted scores:**

- Item A: 4.5
- Item B: 3.2
- Item C: 4.8
- Item D: 4.1
- Item E: 3.9
- Item F: 4.7

**Sorted by score:**

C (4.8) > F (4.7) > A (4.5) > D (4.1) > E (3.9) > B (3.2)

**Top-3 recommendations:**

{C, F, A}

---

## Filtering Candidates

Not all items should be candidates:

**Already consumed:**

Remove items the user has already rated/purchased/watched.

**Availability:**

Only include in-stock items, currently streaming content, etc.

**Business rules:**

Exclude items that violate policies, age restrictions, regional licensing.

**Recency:**

Only include items from the last N days/months.

---

## Choosing K

**K depends on context:**

- Mobile notification: K = 1-3
- Email digest: K = 5-10
- Website homepage: K = 10-20
- "See more" pages: K = 50-100

**User expectations:**

Users expect to see enough options but not be overwhelmed.

**Screen real estate:**

K is often determined by UI layout.

---

## Ties in Scoring

When multiple items have identical scores:

**Random tie-breaking:**

Randomly select among tied items.

**Secondary sort:**

Break ties using popularity, recency, or another criterion.

**Consistent ordering:**

Use item ID for deterministic results (useful for debugging).

---

## Computational Efficiency

**Naive approach:** Score all items, sort all, take top K.

- Time: O(|I| log |I|) for sorting

**Optimized:** Use partial sort or heap.

- Time: O(|I| + K log K) with selection algorithm

**Approximate:** For very large catalogs, use approximate nearest neighbor search (LSH, FAISS).

---

## Candidate Generation + Re-Ranking

Two-stage approach for large catalogs:

**Stage 1: Candidate generation**

Quickly identify ~100-1000 promising items using simple models or indexes.

**Stage 2: Re-ranking**

Score candidates with a more sophisticated model, select top K.

This balances accuracy and efficiency.

---

## Diversity in Top-K

Pure top-K by score may lack diversity:

**Problem:** Top-K might be 10 action movies if user likes action.

**Solution: Diversification**

Balance relevance with diversity:

$$
R_K = \text{argmax}_{S: |S|=K} \sum_{i \in S} \text{score}(i) + \lambda \cdot \text{diversity}(S)
$$

**MMR (Maximal Marginal Relevance):**

Iteratively select items that are relevant but different from already selected items.

---

## Exploration vs Exploitation

**Exploitation:**

Recommend items with highest predicted scores.

**Exploration:**

Recommend some uncertain items to learn more about user preferences.

**Epsilon-greedy:**

With probability $\epsilon$, recommend random items; otherwise, top-K by score.

**Thompson sampling:**

Sample from posterior distribution of scores.

---

## Position Bias

Users are more likely to interact with items at the top of the list.

**Implication:**

Position 1 gets more clicks than position 10, regardless of relevance.

**Consideration:**

When evaluating, position bias in historical data can confound results.

**Mitigation:**

Occasionally randomize positions or use inverse propensity scoring.

---

## Evaluation of Top-K

**Relevance metrics:**

- Precision@K: Fraction of top-K that are relevant
- Recall@K: Fraction of relevant items in top-K
- NDCG@K: Discounted relevance by position

**Beyond accuracy:**

- Diversity: How different are items in top-K?
- Novelty: How unexpected are the items?
- Coverage: How much of catalog appears in top-K across users?

---

## Top-K vs Rating Prediction

**Rating prediction task:**

Predict the exact rating $\hat{r}_{ui}$.

**Top-K recommendation task:**

Rank items correctly; exact score does not matter.

An algorithm can have poor RMSE but good ranking (and vice versa).

**Evaluation should match the task:**

For top-K, use ranking metrics (precision, recall, NDCG), not RMSE.

---

## Personalization Quality

**Top-K should be personalized:**

Different users should get different recommendations based on their preferences.

**Sanity check:**

If all users get the same top-K, the system is essentially non-personalized (popularity-based).

**Measure personalization:**

Compute average overlap between users' top-K lists. Lower overlap = more personalization.

---

## Online vs Offline Top-K

**Offline (batch):**

Precompute top-K for each user periodically.

- Fast serving
- May be stale

**Online (real-time):**

Compute top-K at request time.

- Always fresh
- Higher latency and compute cost

**Hybrid:**

Precompute candidates, re-rank online with recent context.

---

## Cold Start in Top-K

**New user:**

No personalized scores available.

- Fall back to popularity
- Use content-based on limited profile
- Ask for preferences

**New item:**

No collaborative signals.

- Use content similarity
- Boost new items for exploration

---

## Business Constraints

Real systems have constraints beyond pure relevance:

**Inventory:**

Do not recommend out-of-stock items.

**Freshness:**

Promote new content.

**Sponsored items:**

Insert paid placements.

**Fairness:**

Ensure diverse content creators get exposure.

Top-K selection must balance relevance with these constraints.
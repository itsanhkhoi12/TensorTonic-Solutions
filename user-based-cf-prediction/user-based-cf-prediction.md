## What Is User-Based CF Prediction?

User-based collaborative filtering predicts a user's rating for an item based on how similar users rated that item. The intuition is: if users A and B have similar tastes, and B liked an item that A has not seen, A will probably like it too.

$$
\hat{r}_{ui} = \frac{\sum_{v \in N(u)} \text{sim}(u, v) \cdot r_{vi}}{\sum_{v \in N(u)} |\text{sim}(u, v)|}
$$

where $N(u)$ is the neighborhood of users similar to $u$ who have rated item $i$.

---

## The Core Idea

**To predict User A's rating for Item X:**

1. Find users similar to User A
2. Look at how those similar users rated Item X
3. Combine their ratings, weighted by similarity

If similar users loved X, User A will probably love it. If they hated it, User A probably will too.

---

## The Basic Prediction Formula

$$
\hat{r}_{ui} = \frac{\sum_{v \in N(u)} \text{sim}(u, v) \cdot r_{vi}}{\sum_{v \in N(u)} |\text{sim}(u, v)|}
$$

**Components:**

- $\hat{r}_{ui}$: Predicted rating of user $u$ for item $i$
- $N(u)$: Set of similar users who rated item $i$
- $\text{sim}(u, v)$: Similarity between users $u$ and $v$
- $r_{vi}$: User $v$'s actual rating for item $i$

---

## Worked Example

**Goal:** Predict User A's rating for Movie X

**Similar users who rated Movie X:**

- User B (similarity = 0.9): rated X as 5
- User C (similarity = 0.7): rated X as 4
- User D (similarity = 0.5): rated X as 3

**Prediction:**

$$
\hat{r}_{A,X} = \frac{0.9 \times 5 + 0.7 \times 4 + 0.5 \times 3}{0.9 + 0.7 + 0.5}
$$

$$
\hat{r}_{A,X} = \frac{4.5 + 2.8 + 1.5}{2.1} = \frac{8.8}{2.1} \approx 4.19
$$

Predicted rating is approximately 4.2 stars.

---

## Mean-Centered Prediction

Account for different user rating scales:

$$
\hat{r}_{ui} = \bar{r}_u + \frac{\sum_{v \in N(u)} \text{sim}(u, v) \cdot (r_{vi} - \bar{r}_v)}{\sum_{v \in N(u)} |\text{sim}(u, v)|}
$$

**Interpretation:**

Predict user $u$'s mean rating plus a weighted average of how neighbors deviate from their means.

---

## Mean-Centered Example

**User means:**

- User A (target): mean = 3.5
- User B: mean = 4.2
- User C: mean = 3.0
- User D: mean = 2.5

**Ratings for Movie X:**

- User B: 5 (deviation: 5 - 4.2 = 0.8)
- User C: 4 (deviation: 4 - 3.0 = 1.0)
- User D: 3 (deviation: 3 - 2.5 = 0.5)

**Similarities:** B = 0.9, C = 0.7, D = 0.5

**Prediction:**

$$
\hat{r}_{A,X} = 3.5 + \frac{0.9 \times 0.8 + 0.7 \times 1.0 + 0.5 \times 0.5}{0.9 + 0.7 + 0.5}
$$

$$
\hat{r}_{A,X} = 3.5 + \frac{0.72 + 0.70 + 0.25}{2.1} = 3.5 + \frac{1.67}{2.1} = 3.5 + 0.80 = 4.3
$$

---

## User Similarity Measures

**Pearson correlation:**

$$
\text{sim}(u, v) = \frac{\sum_{i \in I_{uv}} (r_{ui} - \bar{r}_u)(r_{vi} - \bar{r}_v)}{\sqrt{\sum_{i} (r_{ui} - \bar{r}_u)^2} \sqrt{\sum_{i} (r_{vi} - \bar{r}_v)^2}}
$$

Measures linear correlation; handles different rating scales.

**Cosine similarity:**

$$
\text{sim}(u, v) = \frac{\sum_{i \in I_{uv}} r_{ui} \cdot r_{vi}}{\sqrt{\sum_{i} r_{ui}^2} \sqrt{\sum_{i} r_{vi}^2}}
$$

Treats ratings as vectors; angle between vectors.

Pearson is generally preferred because it centers the data.

---

## Choosing the Neighborhood

**K-Nearest Neighbors (KNN):**

Use the K most similar users who rated item $i$.

Typical K: 20 to 100

**Threshold-based:**

Use all users with similarity above threshold $\tau$.

**All neighbors:**

Use all users who rated item $i$ (weighted by similarity).

KNN is most common for balancing quality and computation.

---

## Algorithm Steps

**Offline (precompute):**

1. Compute pairwise user similarities
2. For each user, store top-K most similar users

**Online (at prediction time):**

1. Given target user $u$ and item $i$
2. Find neighbors of $u$ who rated $i$
3. Compute weighted average of their ratings
4. Return prediction

---

## Handling Negative Similarity

When $\text{sim}(u, v) < 0$:

**Option 1:** Exclude negatively correlated users.

**Option 2:** Include them; they contribute negatively to the prediction.

$$
\text{If sim} < 0: \text{ neighbor dislikes item} \Rightarrow \text{ target might like it}
$$

**Common choice:** Use only positive similarities for stability.

---

## Sparse Neighborhoods

**Problem:** Few users may have rated both items needed for similarity.

**Solutions:**

- Expand neighborhood size
- Use default similarity for unseen pairs
- Fall back to item-based CF or popularity

If no neighbors rated item $i$, prediction is undefined. Return global mean or user mean.

---

## User-Based vs Item-Based CF

**User-based:**

- Find similar users
- Aggregate their ratings of target item
- User similarities may change as users rate more

**Item-based:**

- Find similar items
- Aggregate user's ratings of those items
- Item similarities are more stable

Item-based is often preferred at scale because item relationships change less frequently.

---

## Scalability Challenges

**Computing all pairwise similarities:**

$O(|U|^2 \cdot |I|)$ for $|U|$ users and $|I|$ items.

**At prediction time:**

Finding neighbors is $O(|U|)$ without precomputation.

**Solutions:**

- Precompute and store top-K neighbors per user
- Use approximate methods (LSH, clustering)
- Sample users for similarity computation

---

## Cold Start Problem

**New user (no ratings):**

Cannot compute similarity with anyone.

- Fall back to popularity
- Use content-based on demographics
- Ask for initial ratings

**New item:**

Has ratings but affects all users' neighborhoods.

- Incrementally update similarities
- Use content similarity for new item

---

## Significance Weighting

Users with few common items may have unreliable similarity.

**Weighted similarity:**

$$
\text{sim}'(u, v) = \text{sim}(u, v) \cdot \min\left(1, \frac{|I_{uv}|}{\tau}\right)
$$

where $|I_{uv}|$ is the number of items both users rated and $\tau$ is a threshold (e.g., 50).

This down-weights similarities based on few items.

---

## Case Amplification

Emphasize highly similar users:

$$
\text{sim}'(u, v) = \text{sim}(u, v)^\rho
$$

where $\rho > 1$ (e.g., 2.5).

This makes high similarities even higher and low similarities lower.

---

## Evaluation

**Rating prediction accuracy:**

- RMSE: $\sqrt{\frac{1}{|T|} \sum (r - \hat{r})^2}$
- MAE: $\frac{1}{|T|} \sum |r - \hat{r}|$

**Ranking quality:**

- Precision@K, Recall@K
- NDCG@K

Evaluate on held-out test ratings.

---

## The Memory-Based Approach

User-based CF is a memory-based (or neighborhood-based) method:

- Stores all ratings in memory
- Computes predictions from stored ratings at query time
- No explicit model parameters learned

Contrast with model-based methods (matrix factorization) that learn parameters and discard raw data.
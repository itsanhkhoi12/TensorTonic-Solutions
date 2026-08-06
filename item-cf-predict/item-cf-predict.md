## What Is Item-Based CF Prediction?

Item-based collaborative filtering predicts a user's rating for an item based on that user's ratings of similar items. The intuition is: if a user liked items similar to item X, they will probably like item X too.

$$
\hat{r}_{ui} = \frac{\sum_{j \in N(i;u)} \text{sim}(i, j) \cdot r_{uj}}{\sum_{j \in N(i;u)} |\text{sim}(i, j)|}
$$

where $N(i;u)$ is the set of items similar to $i$ that user $u$ has rated.

---

## The Core Idea

**To predict user A's rating for Movie X:**

1. Find movies similar to Movie X
2. Look at how user A rated those similar movies
3. Combine those ratings, weighted by similarity

If user A loved movies similar to X, they will probably love X. If they hated similar movies, they will probably dislike X.

---

## The Prediction Formula in Detail

$$
\hat{r}_{ui} = \frac{\sum_{j \in N(i;u)} \text{sim}(i, j) \cdot r_{uj}}{\sum_{j \in N(i;u)} |\text{sim}(i, j)|}
$$

**Components:**

- $\hat{r}_{ui}$: Predicted rating of user $u$ for target item $i$
- $N(i;u)$: Neighbor items (items similar to $i$ that $u$ has rated)
- $\text{sim}(i, j)$: Similarity between items $i$ and $j$
- $r_{uj}$: User $u$'s actual rating for neighbor item $j$

The denominator normalizes so that if all neighbors have similarity 1.0, we get an unweighted average.

---

## Worked Example

**Goal:** Predict User A's rating for Item X

**Known ratings from User A:**

- Item P: 4.0
- Item Q: 5.0
- Item R: 2.0

**Similarities with Item X:**

- sim(X, P) = 0.8
- sim(X, Q) = 0.6
- sim(X, R) = 0.3

**Prediction:**

$$
\hat{r}_{A,X} = \frac{0.8 \times 4.0 + 0.6 \times 5.0 + 0.3 \times 2.0}{0.8 + 0.6 + 0.3}
$$

$$
\hat{r}_{A,X} = \frac{3.2 + 3.0 + 0.6}{1.7} = \frac{6.8}{1.7} = 4.0
$$

Predicted rating is 4.0 stars.

---

## Choosing Neighbors

**All neighbors:** Use all items user $u$ has rated that have non-zero similarity with $i$.

**Top-K neighbors:** Use only the K most similar items.

**Threshold-based:** Use only items with similarity above a threshold $\tau$.

Top-K is most common because:
- Limits computation
- Reduces noise from weakly similar items
- Typically K = 10 to 50

---

## With Mean-Centering (Adjusted Prediction)

Account for the fact that items have different average ratings:

$$
\hat{r}_{ui} = \bar{r}_i + \frac{\sum_{j \in N(i;u)} \text{sim}(i, j) \cdot (r_{uj} - \bar{r}_j)}{\sum_{j \in N(i;u)} |\text{sim}(i, j)|}
$$

where $\bar{r}_i$ and $\bar{r}_j$ are the mean ratings for items $i$ and $j$.

This predicts the average rating for item $i$ plus an adjustment based on how the user rates similar items relative to their averages.

---

## Mean-Centered Example

**Goal:** Predict User A's rating for Item X

**Item averages:**

- Item X average: 3.5
- Item P average: 4.2
- Item Q average: 3.8

**User A's ratings:**

- Item P: 4.0 (deviation: 4.0 - 4.2 = -0.2)
- Item Q: 5.0 (deviation: 5.0 - 3.8 = +1.2)

**Similarities:**

- sim(X, P) = 0.8
- sim(X, Q) = 0.6

**Prediction:**

$$
\hat{r}_{A,X} = 3.5 + \frac{0.8 \times (-0.2) + 0.6 \times 1.2}{0.8 + 0.6}
$$

$$
\hat{r}_{A,X} = 3.5 + \frac{-0.16 + 0.72}{1.4} = 3.5 + \frac{0.56}{1.4} = 3.5 + 0.4 = 3.9
$$

---

## Item Similarity Measures

Common choices for $\text{sim}(i, j)$:

**Adjusted cosine similarity:**

$$
\text{sim}(i, j) = \frac{\sum_{u \in U_{ij}} (r_{ui} - \bar{r}_u)(r_{uj} - \bar{r}_u)}{\sqrt{\sum_{u} (r_{ui} - \bar{r}_u)^2} \sqrt{\sum_{u} (r_{uj} - \bar{r}_u)^2}}
$$

**Pearson correlation:**

$$
\text{sim}(i, j) = \frac{\sum_{u} (r_{ui} - \bar{r}_i)(r_{uj} - \bar{r}_j)}{\sqrt{\sum_{u} (r_{ui} - \bar{r}_i)^2} \sqrt{\sum_{u} (r_{uj} - \bar{r}_j)^2}}
$$

Adjusted cosine is preferred for item-based CF because it normalizes for user rating scales.

---

## Algorithm Steps

**Offline (precompute):**

1. For each pair of items, compute similarity
2. For each item, store top-K most similar items

**Online (at prediction time):**

1. Given user $u$ and target item $i$
2. Find items in user's history that are similar to $i$
3. Compute weighted average of user's ratings for those items
4. Return predicted rating

---

## Item-Based vs User-Based CF

**Item-based:**

- Find items similar to the target item
- Use the user's ratings of those items
- Items are usually more stable than users (fewer new items)
- Similarities can be precomputed

**User-based:**

- Find users similar to the target user
- Use those users' ratings of the target item
- Users change over time (new ratings)
- Harder to precompute

Item-based CF is generally preferred in practice due to stability and scalability.

---

## Handling Cold Start

**New item (no ratings):**

Cannot compute similarity with other items. Fall back to:
- Content-based similarity
- Popularity baseline
- Random recommendations

**New user (no rating history):**

Cannot find neighbor items user has rated. Fall back to:
- Popular items
- Content-based on user profile
- Ask for initial ratings

---

## Sparse Data Considerations

Most user-item pairs have no rating. When computing item similarity:

**Co-rating requirement:**

Only consider users who rated both items. Few co-ratings lead to unreliable similarity.

**Significance weighting:**

Down-weight similarity when based on few co-ratings:

$$
\text{sim}'(i,j) = \text{sim}(i,j) \cdot \min\left(1, \frac{|U_{ij}|}{\tau}\right)
$$

where $\tau$ is a threshold (e.g., 50 co-ratings).

---

## Prediction Clipping

Predicted ratings may fall outside valid range:

**If predictions are:** [0.5, 5.3, 2.1, -0.2]

**After clipping to [1, 5]:** [1.0, 5.0, 2.1, 1.0]

Always clip predictions to the valid rating range before using them.

---

## Complexity Analysis

**Precomputation (similarity matrix):**

- $O(|I|^2 \cdot |U|)$ for all pairs with all users
- Reduced with sparse optimizations

**Prediction:**

- $O(K)$ per prediction if top-K neighbors precomputed
- Very fast online predictions

This is why item-based CF scales well: expensive computation is done offline.

---

## Evaluation

Evaluate predictions using:

**RMSE (Root Mean Square Error):**

$$
\text{RMSE} = \sqrt{\frac{1}{|T|} \sum_{(u,i) \in T} (r_{ui} - \hat{r}_{ui})^2}
$$

**MAE (Mean Absolute Error):**

$$
\text{MAE} = \frac{1}{|T|} \sum_{(u,i) \in T} |r_{ui} - \hat{r}_{ui}|
$$

Lower is better for both metrics.
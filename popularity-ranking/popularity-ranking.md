## What Is Popularity Ranking?

Popularity ranking is the simplest recommendation strategy: rank items by how popular they are and recommend the most popular ones. Despite its simplicity, it is a strong baseline that sophisticated algorithms must beat.

$$
\text{score}(i) = \text{popularity}(i)
$$

Recommend items with the highest scores.

---

## Measuring Popularity

**Interaction count:**

$$
\text{popularity}(i) = |U_i| = \text{number of users who interacted with } i
$$

**Rating count:**

Number of ratings received.

**Purchase/click count:**

Number of times the item was purchased or clicked.

**View count:**

Number of views or impressions.

---

## Why Popularity Works

**Social proof:**

Popular items are popular for a reason. Many users liking something is a signal of quality.

**Safe recommendations:**

Popular items have broad appeal and are less likely to be completely wrong.

**No cold start for items:**

Once an item has any interactions, it can be recommended.

**Computational simplicity:**

Just count and sort. Extremely fast.

---

## Worked Example

**Item interaction counts:**

- Movie A: 10,000 views
- Movie B: 8,500 views
- Movie C: 7,200 views
- Movie D: 5,100 views
- Movie E: 3,800 views

**Popularity ranking:** A > B > C > D > E

**Top-3 recommendations for any user:** {A, B, C}

---

## Non-Personalized Nature

Popularity ranking is completely non-personalized:

**Every user gets the same recommendations.**

This is both a weakness (no personalization) and a strength (simple, scalable, no user data needed).

---

## Time-Weighted Popularity

Recent interactions may matter more:

**Exponential decay:**

$$
\text{popularity}(i) = \sum_{t} e^{-\lambda(t_{now} - t)} \cdot \mathbb{1}[\text{interaction at } t]
$$

**Time windows:**

Only count interactions in the last week/month.

**Trending:**

Rank by growth rate in popularity, not absolute popularity.

This captures what is hot right now, not just all-time favorites.

---

## Average Rating vs Count

**By count:** Most interactions wins.

**By average rating:** Highest rated wins.

**Problem with averages:**

An item with 2 ratings averaging 5.0 beats an item with 1000 ratings averaging 4.8.

**Bayesian average:**

$$
\bar{r}_{bayes} = \frac{C \cdot m + \sum r_{ui}}{C + n}
$$

where $m$ is global mean, $C$ is prior weight, $n$ is rating count.

This pulls small-sample averages toward the global mean.

---

## Popularity with Filters

Combine popularity with filtering:

**By category:**

Most popular action movies, most popular jazz albums.

**By recency:**

Most popular items added this month.

**By geography:**

Most popular in user's country/region.

This adds some contextual relevance to pure popularity.

---

## Popularity Ranking as Baseline

Every recommendation algorithm should beat popularity ranking.

**If your sophisticated model performs worse than "recommend popular items":**

- The model is not learning useful patterns
- The data may be too sparse
- The evaluation may be flawed

**Report improvement over popularity:**

"Our method improves HR@10 by 15% over popularity baseline."

---

## Popularity Bias Problem

Recommending by popularity creates a feedback loop:

1. Popular items get recommended
2. Recommended items get more interactions
3. They become more popular
4. Repeat

**Rich get richer:**

Popular items become more popular; niche items stay invisible.

**Filter bubble:**

Users only see what everyone else sees.

---

## Breaking the Popularity Loop

**Exploration:**

Occasionally recommend less popular items to gather data.

**Diversity requirements:**

Ensure recommendations include some non-popular items.

**Inverse propensity scoring:**

Weight training data to counteract popularity bias.

**Long-tail optimization:**

Explicitly optimize for recommending long-tail items.

---

## Popularity in Different Domains

**E-commerce:**

Bestsellers lists. "Customers also bought" often heavily influenced by popularity.

**Streaming (Netflix, Spotify):**

"Trending now" and "Top 10" are popularity-based.

**News:**

"Most read" articles.

**Social media:**

Trending hashtags, viral content.

---

## Computing Popularity Efficiently

**Online counting:**

Increment counters in real-time as interactions occur.

**Batch computation:**

Periodically recompute popularity from logs.

**Approximate counting:**

For massive scale, use probabilistic data structures (Count-Min Sketch, HyperLogLog).

---

## Segmented Popularity

Different user segments may have different popular items:

**By demographics:**

Popular among 18-24 year olds vs 50+ year olds.

**By behavior:**

Popular among heavy users vs casual users.

**By cohort:**

Popular among users who joined this month.

This adds mild personalization while keeping simplicity.

---

## Popularity for Cold Start Users

New users have no history for personalization.

**Popularity is the natural fallback:**

Show new users what is popular until you learn their preferences.

**Onboarding:**

Ask new users to rate some popular items to bootstrap their profile.

---

## Limitations of Popularity

**No personalization:**

Cannot capture individual preferences.

**Homogenization:**

Everyone sees the same things.

**Niche neglect:**

Long-tail items are never recommended.

**Past popularity:**

May recommend outdated items unless time-weighted.

**Quality confusion:**

Popular is not always good (viral clickbait).

---

## Hybrid Approaches

Combine popularity with personalization:

**Weighted combination:**

$$
\text{score}(i; u) = \alpha \cdot \text{relevance}(i; u) + (1-\alpha) \cdot \text{popularity}(i)
$$

**Fallback:**

Use personalized scores when available, popularity otherwise.

**Boosting:**

Add popularity bonus to personalized scores.
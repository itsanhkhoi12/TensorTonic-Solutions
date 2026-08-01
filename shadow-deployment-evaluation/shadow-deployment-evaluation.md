## The Problem: How Do You Test a Model on Real Traffic Without Risk?

Deploying a new machine learning model to production is risky. Offline evaluation (on held-out test sets) never perfectly predicts real-world performance. Models may encounter data patterns not present in training, latency characteristics may differ under load, and edge cases may surface only with diverse production traffic.

The traditional approach is to directly replace the production model and hope for the best. If problems emerge, you roll back. But this is reactive and can damage user experience, revenue, or trust during the problem period.

**Shadow deployment** (also called "dark launching") offers a safer alternative. The new candidate model runs alongside the production model on identical inputs, but only the production model predictions are served to users. The shadow model predictions are logged for offline analysis. This allows you to evaluate the candidate on real traffic without any user-facing risk.

---

## How Shadow Deployment Works

In a shadow deployment setup:

**Step 1: Production Model Serves Users**
Every incoming request goes to the production model. Its predictions are returned to users and drive business outcomes.

**Step 2: Shadow Model Receives Same Requests**
Every request is also sent to the shadow (candidate) model. It makes predictions, but these are never shown to users.

**Step 3: Both Predictions Are Logged**
A logging system records, for each request:
- The input features
- The production model prediction
- The shadow model prediction
- The actual outcome (when it becomes available)
- Latency measurements for both models

**Step 4: Offline Analysis**
After collecting sufficient data, you analyze the logs to compare the two models across multiple dimensions.

This architecture ensures that users always see production model predictions while you gather comprehensive data about the candidate.

---

## Key Metrics for Shadow Evaluation

To decide whether the shadow model should replace production, you evaluate multiple metrics:

### Accuracy Comparison

The most important metric: does the shadow model make better predictions?

$$
\text{accuracy} = \frac{\text{number of correct predictions}}{\text{total predictions}}
$$

You compute accuracy for both production and shadow models, then compare:

$$
\text{accuracy\_gain} = \text{shadow\_accuracy} - \text{production\_accuracy}
$$

A positive gain indicates the shadow model is more accurate. You require a minimum gain threshold to justify the risk and effort of switching models.

---

### Latency Evaluation

Even if a model is more accurate, it cannot be deployed if it is too slow. Latency directly impacts user experience and infrastructure costs.

The **P95 latency** (95th percentile) is commonly used because it captures worst-case behavior while excluding extreme outliers:
- 95% of requests complete faster than P95
- It reflects the experience of most users
- It is more stable than P99 while still capturing tail behavior

To compute P95 using the nearest-rank method:

**Step 1**: Sort all latency measurements in ascending order

**Step 2**: Compute the rank: $\text{rank} = \lceil 0.95 \times n \rceil$

**Step 3**: The P95 value is the element at index (rank - 1) in the sorted array (0-indexed)

The shadow model P95 latency must be at or below the maximum acceptable threshold.

---

### Agreement Rate

Agreement rate measures how often the two models make the same prediction, regardless of correctness:

$$
\text{agreement\_rate} = \frac{\text{requests where production prediction = shadow prediction}}{\text{total requests}}
$$

This metric serves multiple purposes:

**Change Magnitude Assessment**: High agreement (say, 95%) indicates the models behave similarly. The switch will have minimal impact. Low agreement (say, 60%) indicates substantial behavioral differences.

**Risk Evaluation**: Models with low agreement may cause user-facing changes that require careful communication or gradual rollout.

**Debugging Aid**: When models disagree, examining those cases reveals where and why they differ.

A minimum agreement threshold ensures the new model does not dramatically change system behavior.

---

## The Promotion Decision

The shadow model is promoted to production only when ALL criteria are satisfied simultaneously:

**Criterion 1: Accuracy Improvement**

$$
\text{accuracy\_gain} \geq \text{min\_accuracy\_gain}
$$

This ensures the new model is actually better (or at least not worse, if min_gain is 0 or negative).

**Criterion 2: Latency Acceptable**

$$
\text{shadow\_p95\_latency} \leq \text{max\_latency\_p95}
$$

This ensures the new model is fast enough for production requirements.

**Criterion 3: Behavior Similarity**

$$
\text{agreement\_rate} \geq \text{min\_agreement\_rate}
$$

This ensures the new model does not behave too differently from production.

If any criterion fails, promotion is rejected. The shadow model needs more tuning or the criteria need adjustment.

---

## Computing the Metrics: Step by Step

Given production logs and shadow logs for $n$ requests:

**Step 1: Compute Production Accuracy**
- Count requests where production_prediction equals actual_value
- Divide by n

**Step 2: Compute Shadow Accuracy**
- Count requests where shadow_prediction equals actual_value
- Divide by n

**Step 3: Compute Accuracy Gain**
- Subtract production accuracy from shadow accuracy

**Step 4: Compute Shadow P95 Latency**
- Extract all shadow latency values
- Sort in ascending order
- Compute rank = ceil(0.95 * n)
- Return element at index (rank - 1)

**Step 5: Compute Agreement Rate**
- Count requests where production_prediction equals shadow_prediction
- Divide by n

**Step 6: Evaluate Promotion Criteria**
- Check if accuracy_gain >= min_accuracy_gain
- Check if shadow_p95 <= max_latency_p95
- Check if agreement_rate >= min_agreement_rate
- Promote only if ALL three are true

---

## A Detailed Worked Example

**Production Log (5 requests):**
- Request 1: prediction=1, actual=1, latency=45ms
- Request 2: prediction=0, actual=0, latency=52ms
- Request 3: prediction=1, actual=0, latency=48ms
- Request 4: prediction=0, actual=1, latency=51ms
- Request 5: prediction=1, actual=1, latency=49ms

**Shadow Log (5 requests):**
- Request 1: prediction=1, actual=1, latency=42ms
- Request 2: prediction=1, actual=0, latency=55ms
- Request 3: prediction=0, actual=0, latency=47ms
- Request 4: prediction=1, actual=1, latency=53ms
- Request 5: prediction=1, actual=1, latency=44ms

**Production Accuracy Calculation:**
- Request 1: prod=1, actual=1, correct
- Request 2: prod=0, actual=0, correct
- Request 3: prod=1, actual=0, wrong
- Request 4: prod=0, actual=1, wrong
- Request 5: prod=1, actual=1, correct
- Correct: 3 out of 5
- Production accuracy = 3/5 = 0.60

**Shadow Accuracy Calculation:**
- Request 1: shadow=1, actual=1, correct
- Request 2: shadow=1, actual=0, wrong
- Request 3: shadow=0, actual=0, correct
- Request 4: shadow=1, actual=1, correct
- Request 5: shadow=1, actual=1, correct
- Correct: 4 out of 5
- Shadow accuracy = 4/5 = 0.80

**Accuracy Gain:** 0.80 - 0.60 = 0.20 (20% improvement)

**Shadow P95 Latency:**
- Shadow latencies: [42, 55, 47, 53, 44]
- Sorted: [42, 44, 47, 53, 55]
- Rank = ceil(0.95 * 5) = ceil(4.75) = 5
- Index = 5 - 1 = 4
- P95 = 55ms

**Agreement Rate:**
- Request 1: prod=1, shadow=1, agree
- Request 2: prod=0, shadow=1, disagree
- Request 3: prod=1, shadow=0, disagree
- Request 4: prod=0, shadow=1, disagree
- Request 5: prod=1, shadow=1, agree
- Agreement: 2 out of 5
- Agreement rate = 2/5 = 0.40

**Promotion Decision (with thresholds: min_accuracy_gain=0.10, max_latency_p95=60, min_agreement_rate=0.50):**
- Accuracy gain: 0.20 >= 0.10? YES
- P95 latency: 55 <= 60? YES
- Agreement rate: 0.40 >= 0.50? NO

**Result:** Promotion REJECTED due to low agreement rate.

Despite the shadow model being more accurate and meeting latency requirements, the low agreement rate indicates significant behavioral differences that warrant investigation before deployment.

---

## Interpreting Agreement Rate

The agreement metric requires careful interpretation:

**High Agreement (>90%) with Accuracy Gain**: The models are similar, but the shadow is slightly better. Low-risk promotion.

**High Agreement with No Accuracy Gain**: The models are nearly identical. There may be no reason to switch.

**Low Agreement (<70%) with Accuracy Gain**: The shadow model makes very different predictions. Even if more accurate overall, the change magnitude may surprise users. Consider gradual rollout.

**Low Agreement with Accuracy Loss**: The shadow model is both different and worse. Do not promote.

---

## Advantages of Shadow Deployment

**Zero User Risk**: Users only see production predictions during evaluation. Bad shadow models do not affect anyone.

**Real Traffic Evaluation**: You test on actual production data patterns, not synthetic test sets.

**Comprehensive Comparison**: You can compute any metric after the fact since all predictions are logged.

**Latency Measurement Under Load**: Shadow model latency reflects real production conditions, not isolated benchmarks.

---

## Limitations and Considerations

**Infrastructure Cost**: Running two models in parallel doubles compute requirements during the shadow period.

**Logging Volume**: Storing predictions and latencies for every request can be expensive at scale.

**Delayed Labels**: Actual outcomes may not be immediately available, delaying the analysis.

**Non-Deterministic Inputs**: If inputs change between production and shadow calls (e.g., due to time-sensitive features), predictions may not be directly comparable.

---

## Where Shadow Deployment Shows Up

**Search Engines**: New ranking algorithms are shadow-deployed to compare relevance without affecting user searches.

**Recommendation Systems**: Candidate recommendation models run in shadow to evaluate engagement predictions before deployment.

**Ad Tech**: New ad ranking models are tested in shadow to verify revenue impact predictions.

**Fraud Detection**: New fraud models run in shadow to measure detection rates without risking false positives on real transactions.

**Healthcare AI**: Clinical prediction models undergo extensive shadow testing before receiving regulatory approval for production use.
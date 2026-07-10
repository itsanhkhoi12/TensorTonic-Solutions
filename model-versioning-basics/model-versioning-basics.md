## The Problem: Which Model Should Go to Production?

In any serious ML system, you will have multiple model versions. Each time you retrain, experiment with new features, or tune hyperparameters, you create a new candidate. But only one model can serve production traffic at a time. How do you decide which one to promote?

This is the core challenge of **model versioning**: tracking model artifacts, their performance metrics, and making principled promotion decisions.

---

## What is a Model Registry?

A **model registry** is a centralized repository that stores:
- Model artifacts (the trained weights, parameters, or serialized objects)
- Metadata (training date, hyperparameters, dataset version)
- Performance metrics (accuracy, latency, resource usage)
- Lineage information (which code and data produced this model)

Popular tools like MLflow, Weights & Biases, and cloud-native solutions (AWS SageMaker, Azure ML, Vertex AI) all provide model registry functionality.

The registry enables teams to:
- Reproduce any past model
- Compare candidates objectively
- Roll back to previous versions if issues arise
- Audit the model development process

---

## The Promotion Decision

When choosing which model to promote, you typically consider multiple factors in a prioritized order:

**1. Primary metric (Accuracy)**: The model core performance measure. Higher accuracy means better predictions. This is almost always the first filter.

**2. Secondary metric (Latency)**: How fast the model responds. In real-time systems, a slightly less accurate model that responds in 10ms may be preferable to a more accurate model that takes 500ms.

**3. Recency (Timestamp)**: All else being equal, newer models are preferred. They were trained on more recent data and reflect the latest code improvements.

---

## Multi-Criteria Comparison

When comparing models, you create a **ranking** based on multiple criteria. The key insight is that criteria have priorities:

$$
\text{Best Model} = \arg\max_m \left( \text{accuracy}(m), -\text{latency}(m), \text{timestamp}(m) \right)
$$

The negative sign on latency converts "lower is better" to "higher is better" for consistent comparison.

This is a **lexicographic ordering**: first sort by accuracy (descending), then by latency (ascending), then by timestamp (descending). The first model in this sorted order is the winner.

---

## Step-by-Step Selection Process

Given a list of model versions, each with (name, accuracy, latency, timestamp):

**Step 1**: Sort all models by accuracy in descending order (highest first)

**Step 2**: Among models with equal accuracy, sort by latency in ascending order (lowest first)

**Step 3**: Among models with equal accuracy AND latency, sort by timestamp in descending order (most recent first)

**Step 4**: The first model in this sorted list is promoted to production

---

## A Concrete Example

Consider three model versions:

- v1: accuracy = 0.92, latency = 45ms, timestamp = 2024-01-15
- v2: accuracy = 0.94, latency = 60ms, timestamp = 2024-01-20
- v3: accuracy = 0.94, latency = 50ms, timestamp = 2024-01-18

**Step 1**: Sort by accuracy descending
- v2 (0.94), v3 (0.94), v1 (0.92)

**Step 2**: v2 and v3 are tied on accuracy. Sort them by latency ascending:
- v3 (50ms), v2 (60ms), then v1 (0.92)

**Result**: **v3** is promoted. It has the highest accuracy AND the lowest latency among top-accuracy models.

---

## Why Not Just Use Accuracy?

If accuracy were the only metric, you could deploy a model that takes 30 seconds per prediction. In production, this creates:
- Poor user experience
- Timeout errors
- High infrastructure costs
- Queue backlogs

Similarly, if you only optimized for latency, you might deploy a trivial model that always predicts the majority class.

The multi-criteria approach balances these trade-offs systematically.

---

## Where Model Versioning Shows Up

**Continuous Training Pipelines**: Automated systems that retrain models daily or weekly need automated promotion logic to decide when a new model is ready.

**A/B Testing**: Before full promotion, a new model version might be deployed to a small percentage of traffic. The registry tracks which version is in each stage.

**Rollbacks**: When a production issue is detected, the registry provides the previous stable version to roll back to immediately.

**Compliance and Auditing**: Regulated industries require documentation of which model version made which predictions, and why it was chosen over alternatives.
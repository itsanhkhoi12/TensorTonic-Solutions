## What Is Ordinal Encoding?

Ordinal encoding is a technique for converting categorical features into numerical values by assigning integers to categories based on their inherent order or rank. Unlike one-hot encoding, it produces a single column with ordered integer values.

For categories with natural order (like education level or size), ordinal encoding preserves this meaningful ranking in the numerical representation.

---

## When to Use Ordinal Encoding

**Ordinal encoding is appropriate when:**

- Categories have a natural, meaningful order
- The ordering relationship should be preserved
- You want to reduce dimensionality compared to one-hot encoding
- The algorithm can use ordered numerical features

**Examples of ordinal features:**

- Education: High School < Bachelor's < Master's < PhD
- Size: Small < Medium < Large < Extra Large
- Rating: Poor < Fair < Good < Excellent
- Priority: Low < Medium < High < Critical

---

## The Basic Process

**Step 1:** Identify the natural order of categories

**Step 2:** Assign integers starting from 0 (or 1) based on the order

**Step 3:** Replace each category with its assigned integer

**Step 4:** Store the mapping for consistent encoding of new data

---

## Worked Example: Education Level

**Categories (ordered):**

1. High School
2. Bachelor's
3. Master's
4. PhD

**Mapping:**

- High School: 0
- Bachelor's: 1
- Master's: 2
- PhD: 3

**Original data:**

[Bachelor's, PhD, High School, Master's, Bachelor's]

**Encoded data:**

[1, 3, 0, 2, 1]

---

## Worked Example: T-Shirt Size

**Categories (ordered):**

- XS (Extra Small)
- S (Small)
- M (Medium)
- L (Large)
- XL (Extra Large)
- XXL (Double Extra Large)

**Mapping:**

- XS: 0
- S: 1
- M: 2
- L: 3
- XL: 4
- XXL: 5

**Original:** [M, L, S, XL, M, XXL]

**Encoded:** [2, 3, 1, 4, 2, 5]

---

## Ordinal vs Label Encoding

**Ordinal encoding:**

- Order is meaningful and intentional
- Categories have inherent ranking
- The assigned integers reflect true relationships

**Label encoding:**

- Order is arbitrary (usually alphabetical or by appearance)
- Categories do not have inherent ranking
- Assigned integers do not reflect meaningful relationships

**Example:**

- Colors: Red = 0, Blue = 1, Green = 2 (arbitrary, use one-hot instead)
- Sizes: Small = 0, Medium = 1, Large = 2 (meaningful order, use ordinal)

---

## Ordinal vs One-Hot Encoding

**Ordinal encoding:**

- Produces 1 column
- Assumes ordering relationship
- Compact representation

**One-hot encoding:**

- Produces k columns for k categories
- No ordering assumption
- Each category is equidistant from others

**Trade-off:** Ordinal is more compact but imposes an ordering that may or may not be appropriate.

---

## Mathematical Representation

Given categories $C = \{c_1, c_2, ..., c_k\}$ with order $c_1 < c_2 < ... < c_k$:

$$
f(c_i) = i - 1
$$

This maps:
- First category to 0
- Second category to 1
- kth category to k-1

Alternatively, starting from 1:

$$
f(c_i) = i
$$

---

## Custom Starting Points

You can start from any integer:

**Starting from 1:**

- High School: 1
- Bachelor's: 2
- Master's: 3
- PhD: 4

**Starting from 0 (more common in programming):**

- High School: 0
- Bachelor's: 1
- Master's: 2
- PhD: 3

Choose based on your model's requirements or conventions.

---

## Non-Uniform Spacing

Sometimes the gap between categories is not equal:

**Example: Pain scale**

- No pain: 0
- Mild: 1
- Moderate: 3
- Severe: 6
- Unbearable: 10

This reflects that the jump from Mild to Moderate is larger than from No pain to Mild.

**Use with caution:** Only if you have domain knowledge supporting the spacing.

---

## Handling Unknown Categories

When new data contains unseen categories:

**Option 1: Assign special value**

$$
f(c_{unknown}) = -1 \text{ or } k
$$

**Option 2: Raise an error**

Force explicit handling of unexpected categories.

**Option 3: Map to most frequent category**

Use the mode of the training data.

**Option 4: Map to middle category**

Neutral assumption when order is unknown.

---

## Handling Missing Values

**Option 1: Separate encoding**

$$
f(\text{NaN}) = -1 \text{ or } k
$$

**Option 2: Impute before encoding**

Fill with mode, median category, or domain-specific default.

**Option 3: Preserve as NaN**

Let the model handle missing values directly.

---

## Ordinal Encoding for Tree-Based Models

Decision trees and random forests can naturally handle ordinal features:

**Benefit:** Trees can find optimal split points within the ordered values.

**Example:**

If Education encoded as [0, 1, 2, 3], tree might split at Education < 2 (separating High School/Bachelor's from Master's/PhD).

---

## Ordinal Encoding for Linear Models

Linear models treat ordinal encoding as numerical:

$$
y = \beta_0 + \beta_1 \cdot \text{Education}
$$

**Assumption:** Equal spacing is meaningful.

If Education increases by 1 (e.g., from Bachelor's to Master's), y changes by $\beta_1$.

**Problem:** Is the effect of Bachelor's to Master's the same as High School to Bachelor's?

If not, consider one-hot encoding or polynomial terms.

---

## Common Ordinal Features

**Customer satisfaction:**

- Very Dissatisfied (0)
- Dissatisfied (1)
- Neutral (2)
- Satisfied (3)
- Very Satisfied (4)

**Risk level:**

- Low (0)
- Medium (1)
- High (2)
- Critical (3)

**Age groups:**

- Child (0)
- Teenager (1)
- Adult (2)
- Senior (3)

---

## Ordinal Encoding in Surveys

Survey responses often use Likert scales:

**Agreement scale:**

- Strongly Disagree: 1
- Disagree: 2
- Neutral: 3
- Agree: 4
- Strongly Agree: 5

**Frequency scale:**

- Never: 0
- Rarely: 1
- Sometimes: 2
- Often: 3
- Always: 4

---

## Verifying Order Correctness

Before applying ordinal encoding, verify the order makes sense:

**Questions to ask:**

1. Is there a clear greater than / less than relationship?
2. Would the domain expert agree on the ordering?
3. Does the order have predictive meaning for the target?

**If no clear order exists:** Use one-hot encoding instead.

---

## Ordinal Encoding with Pandas Example Concept

**Conceptual process:**

1. Define the category order explicitly
2. Create a mapping dictionary
3. Apply the mapping to the data

**Important:** Always explicitly define the order rather than relying on alphabetical or appearance order.

---

## Multi-Level Ordinal Features

Some ordinal features have hierarchical levels:

**Example: Military rank**

Enlisted ranks (E1-E9) < Warrant officers (W1-W5) < Commissioned officers (O1-O10)

**Approach 1:** Single ordinal encoding across all levels

**Approach 2:** Separate ordinal encodings for each level plus a level indicator

---

## Ordinal Encoding and Feature Interactions

Ordinal features can be used in interactions:

**Example:**

- Education level (ordinal)
- Years of experience (numerical)

Interaction: Education_level * Experience

This allows the effect of experience to vary by education level.

---

## Testing the Ordinality Assumption

**Check if ordinality helps:**

1. Fit model with ordinal encoding
2. Fit model with one-hot encoding
3. Compare performance on validation data

**If one-hot significantly outperforms:** The ordinality assumption may not hold.

---

## Ordinal Encoding in Ensemble Methods

**Random Forests:**

Ordinal encoding works well because trees can split at any threshold.

**Gradient Boosting (XGBoost, LightGBM):**

Also handles ordinal features well. LightGBM has native support for categorical features.

**Neural Networks:**

Can use ordinal encoding, but embeddings may capture richer relationships.

---

## Potential Problems

**1. Implied equidistance:**

Ordinal encoding implies equal spacing between categories, which may not be true.

**2. Numerical operations:**

Some models might compute means or other operations that are meaningless for ordinal data. Mean of [Master's, Bachelor's] is not meaningful as (2 + 1) / 2 = 1.5.

**3. Wrong order:**

Incorrect ordering can hurt model performance significantly.

---

## Ordinal vs Numeric

Sometimes ordinal data appears numeric:

**Example:** Star ratings 1-5

This is ordinal, not truly numeric, because:
- The difference between 1 and 2 stars may not equal the difference between 4 and 5 stars
- There is no true zero point
- Ratios are not meaningful (4 stars is not twice as good as 2 stars)

However, treating it as numeric often works well in practice.

---

## Monotonic Relationships

Ordinal encoding assumes monotonic relationship with target:

**Monotonically increasing:**

Higher category value corresponds to higher (or lower) target value consistently.

**Non-monotonic:**

Relationship is not consistent. Middle categories might have different behavior.

If relationship is non-monotonic, one-hot encoding may be better.

---

## Best Practices

**1. Verify natural ordering:**

Ensure the categories have a genuine ordinal relationship.

**2. Document the mapping:**

Keep clear records of which integer maps to which category.

**3. Be consistent:**

Use the same mapping for training and inference.

**4. Consider alternatives:**

If performance is poor, try one-hot encoding.

**5. Handle unknowns:**

Plan for how to handle new categories in production.

---

## Common Mistakes

**1. Assuming all categorical features are ordinal:**

Colors, names, and IDs are not ordinal.

**2. Using wrong order:**

Assigning integers without considering the true ranking.

**3. Relying on default alphabetical order:**

Alphabetical order rarely matches meaningful order.

**4. Forgetting to store the mapping:**

Unable to encode new data consistently.

**5. Treating as continuous:**

Computing statistics like mean and standard deviation on ordinal data.
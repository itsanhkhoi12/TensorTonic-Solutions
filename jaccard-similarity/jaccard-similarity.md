## What Is Jaccard Similarity?

Jaccard similarity (also called Jaccard index or Intersection over Union) measures the similarity between two sets by comparing the size of their intersection to the size of their union.

$$
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
$$

It answers the question: "Of all elements that appear in either set, what fraction appears in both?"

---

## Understanding the Formula

**Numerator:** $|A \cap B|$ = number of elements in both sets (intersection)

**Denominator:** $|A \cup B|$ = number of elements in at least one set (union)

$$
J(A, B) = \frac{\text{Elements in both A and B}}{\text{Elements in A or B or both}}
$$

---

## Range of Values

Jaccard similarity ranges from 0 to 1:

**J = 0:** Sets have no elements in common ($A \cap B = \emptyset$)

**J = 1:** Sets are identical ($A = B$)

**J between 0 and 1:** Sets have partial overlap

---

## Worked Example

**Set A:** {1, 2, 3, 4, 5}

**Set B:** {3, 4, 5, 6, 7}

**Intersection:** $A \cap B$ = {3, 4, 5} → size = 3

**Union:** $A \cup B$ = {1, 2, 3, 4, 5, 6, 7} → size = 7

**Jaccard similarity:**

$$
J(A, B) = \frac{3}{7} \approx 0.429
$$

---

## Alternative Formula

Using set sizes and intersection:

$$
J(A, B) = \frac{|A \cap B|}{|A| + |B| - |A \cap B|}
$$

This avoids explicitly computing the union.

**Example verification:**

$$
J(A, B) = \frac{3}{5 + 5 - 3} = \frac{3}{7} \approx 0.429
$$

---

## Jaccard Distance

The Jaccard distance is the complement of similarity:

$$
d_J(A, B) = 1 - J(A, B)
$$

**Properties:**

- $d_J(A, B) = 0$ when sets are identical
- $d_J(A, B) = 1$ when sets have no overlap
- Satisfies the triangle inequality (is a true metric)

---

## Jaccard in Recommender Systems

**User similarity:**

Compare users by the sets of items they have interacted with.

$$
J(u_1, u_2) = \frac{|I_{u_1} \cap I_{u_2}|}{|I_{u_1} \cup I_{u_2}|}
$$

Users who rated/purchased many of the same items are similar.

**Item similarity:**

Compare items by the sets of users who interacted with them.

$$
J(i_1, i_2) = \frac{|U_{i_1} \cap U_{i_2}|}{|U_{i_1} \cup U_{i_2}|}
$$

Items consumed by many of the same users are similar.

---

## When to Use Jaccard Similarity

**Binary/implicit feedback:**

- Did user watch the movie? (yes/no)
- Did user purchase the item? (yes/no)
- Did user click the link? (yes/no)

**No rating magnitude:**

When you only know what users interacted with, not how much they liked it.

**Set-based data:**

- Tags associated with items
- Categories a user has browsed
- Words in a document

---

## Jaccard vs Cosine Similarity

**Jaccard:**

- Works on sets (binary presence/absence)
- Does not consider frequency or magnitude
- Range: [0, 1]

**Cosine:**

- Works on vectors (numerical values)
- Considers magnitude and direction
- Range: [-1, 1] or [0, 1] for non-negative vectors

**When ratings exist:** Use cosine or Pearson correlation

**When only interactions exist:** Use Jaccard

---

## Example: User Similarity with Jaccard

**User A watched:** {Movie1, Movie2, Movie3, Movie5}

**User B watched:** {Movie2, Movie3, Movie4, Movie6}

**User C watched:** {Movie1, Movie2, Movie3, Movie4, Movie5}

**J(A, B):**

- Intersection: {Movie2, Movie3} → 2
- Union: {Movie1, Movie2, Movie3, Movie4, Movie5, Movie6} → 6
- J(A, B) = 2/6 = 0.333

**J(A, C):**

- Intersection: {Movie1, Movie2, Movie3, Movie5} → 4
- Union: {Movie1, Movie2, Movie3, Movie4, Movie5} → 5
- J(A, C) = 4/5 = 0.8

User C is more similar to User A.

---

## Example: Item Similarity with Jaccard

**Item X purchased by:** {User1, User2, User3}

**Item Y purchased by:** {User2, User3, User4, User5}

**Intersection:** {User2, User3} → 2

**Union:** {User1, User2, User3, User4, User5} → 5

**J(X, Y) = 2/5 = 0.4**

---

## Handling Empty Sets

If either set is empty:

**One set empty:**

$A = \emptyset$, $B = \{1, 2, 3\}$

$A \cap B = \emptyset$, $A \cup B = \{1, 2, 3\}$

$J(A, B) = 0 / 3 = 0$

**Both sets empty:**

$A = \emptyset$, $B = \emptyset$

$A \cup B = \emptyset$ → Division by zero

**Convention:** Define $J(\emptyset, \emptyset) = 1$ (empty sets are identical).

---

## Weighted Jaccard Similarity

For multisets where elements have counts:

$$
J_w(A, B) = \frac{\sum_x \min(A_x, B_x)}{\sum_x \max(A_x, B_x)}
$$

where $A_x$ is the count of element $x$ in multiset $A$.

**Example:**

$A = \{a:3, b:2\}$, $B = \{a:1, b:4, c:1\}$

Numerator: $\min(3,1) + \min(2,4) + \min(0,1) = 1 + 2 + 0 = 3$

Denominator: $\max(3,1) + \max(2,4) + \max(0,1) = 3 + 4 + 1 = 8$

$J_w(A, B) = 3/8 = 0.375$

---

## Min-Hash for Efficient Computation

Computing exact Jaccard for many pairs is expensive. Min-Hash approximates it efficiently:

**Idea:** Hash each element, keep minimum hash value. Similar sets are likely to have the same minimum.

**Property:**

$$
P(\min(h(A)) = \min(h(B))) = J(A, B)
$$

Use multiple hash functions to estimate Jaccard without computing full intersection/union.

---

## Jaccard in Text Similarity

**Shingles (n-grams):**

Convert text to set of character or word n-grams.

**Example (word 2-grams):**

"the cat sat" → {"the cat", "cat sat"}

"the cat ran" → {"the cat", "cat ran"}

Intersection: {"the cat"} → 1

Union: {"the cat", "cat sat", "cat ran"} → 3

J = 1/3 ≈ 0.333

---

## Jaccard vs Overlap Coefficient

**Jaccard:**

$$
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
$$

**Overlap coefficient:**

$$
O(A, B) = \frac{|A \cap B|}{\min(|A|, |B|)}
$$

Overlap coefficient is 1 if one set is a subset of the other. Jaccard is more conservative.

---

## Asymmetric Jaccard-like Measures

**Containment (A in B):**

$$
C(A, B) = \frac{|A \cap B|}{|A|}
$$

What fraction of A's elements are in B?

This is asymmetric: $C(A, B) \neq C(B, A)$ in general.

Useful when one set is the "query" and the other is the "target."

---

## Properties of Jaccard Similarity

**Symmetry:** $J(A, B) = J(B, A)$

**Bounded:** $0 \leq J(A, B) \leq 1$

**Identity:** $J(A, A) = 1$

**Metric (as distance):** $d_J$ satisfies triangle inequality

These properties make Jaccard well-behaved for similarity computations.
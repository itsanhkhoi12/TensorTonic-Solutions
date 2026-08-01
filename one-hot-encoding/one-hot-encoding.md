## What is One-Hot Encoding?

One-hot encoding transforms categorical labels into binary vectors where each category is represented by a unique position. For a sample with class label $k$ out of $K$ possible classes, the one-hot vector has a 1 at position $k$ and 0 everywhere else. This representation is essential for feeding categorical data into machine learning models.

---

## Why One-Hot Encode?

**No ordinal relationship**: Integer encoding (0, 1, 2, 3) implies an ordering that may not exist. Is "red" < "green" < "blue"? One-hot encoding treats all categories as equally different.

**Algorithm compatibility**: Many algorithms (neural networks, logistic regression) expect numerical inputs and interpret integers as continuous values. One-hot provides a proper numerical representation.

**Distance preservation**: In one-hot space, all pairs of different categories are equidistant (Hamming distance = 2), reflecting that switching from "cat" to "dog" is no more different than switching from "cat" to "bird".

---

## The One-Hot Vector

For $K$ classes and a sample with label $y \in \{0, 1, ..., K-1\}$:

$$
\text{one\_hot}(y) = [0, 0, ..., 0, 1, 0, ..., 0]
$$

Where the 1 appears at position $y$.

**Properties**:
- Vector length: $K$
- Sum of elements: 1
- Exactly one non-zero element
- dtype: typically float for compatibility with neural network operations

---

## Matrix Representation

For $N$ samples with labels $y = [y_1, y_2, ..., y_N]$, the one-hot matrix $Y$ has shape $(N, K)$:

$$
Y_{ij} = \begin{cases} 1 & \text{if } y_i = j \\ 0 & \text{otherwise} \end{cases}
$$

Each row is a one-hot vector for one sample.

---

## Worked Example

**Labels**: [0, 2, 1, 0, 2] with $K = 3$ classes

**One-hot matrix**:
- Label 0 → [1, 0, 0]
- Label 2 → [0, 0, 1]
- Label 1 → [0, 1, 0]
- Label 0 → [1, 0, 0]
- Label 2 → [0, 0, 1]

**Result** (5 × 3 matrix):
- Row 0: [1, 0, 0]
- Row 1: [0, 0, 1]
- Row 2: [0, 1, 0]
- Row 3: [1, 0, 0]
- Row 4: [0, 0, 1]

---

## Handling num_classes Parameter

**When num_classes is not specified**: Use $K = \max(y) + 1$

Example: labels = [0, 1, 3] → K = 4 (not 3!)

**When num_classes is specified**: Use the provided value

Example: labels = [0, 1, 2] with num_classes = 5 → K = 5

This creates "extra" columns that are all zeros. Useful when:
- Training data does not contain all possible classes
- Maintaining consistent dimensionality across datasets

---

## Worked Example with Extra Classes

**Labels**: [0, 1, 2] with num_classes = 5

**One-hot matrix** (3 × 5):
- Label 0 → [1, 0, 0, 0, 0]
- Label 1 → [0, 1, 0, 0, 0]
- Label 2 → [0, 0, 1, 0, 0]

Columns 3 and 4 are all zeros since no samples have those labels.

---

## Vectorized Index Assignment

The naive approach loops through samples. A vectorized approach:

1. Create a zero matrix of shape (N, K)
2. Use advanced indexing: `matrix[row_indices, column_indices] = 1`

Where:
- row_indices = [0, 1, 2, ..., N-1] (sample indices)
- column_indices = y (the label values)

This sets one element per row in a single operation.

---

## Label Validation

**Check**: All labels must be less than num_classes

If $y_i \geq K$, the label is invalid and would cause an index error or produce incorrect results.

**Common validations**:
- All labels are non-negative integers
- All labels are less than num_classes
- No NaN or missing values

---

## Inverse Operation

Converting one-hot back to integer labels:

$$
y_i = \arg\max_j(Y_{ij})
$$

The index of the maximum element (the 1) in each row gives the original label.

**Soft labels**: If probabilities instead of hard one-hot (e.g., [0.1, 0.7, 0.2]), argmax still gives the predicted class.

---

## Memory Considerations

For $N$ samples and $K$ classes:
- Integer labels: $N$ integers
- One-hot matrix: $N \times K$ floats

**High cardinality problem**: If K = 10,000 categories, one-hot creates 10,000 columns. Consider:
- Embedding layers (learn dense representations)
- Hashing (fixed-size output)
- Target encoding (replace with statistics)

---

## One-Hot in Neural Networks

**Output layer**: Classification networks produce logits → softmax → one-hot-like probabilities

**Loss functions**: Cross-entropy loss compares predicted probabilities to true one-hot vectors:

$$
\text{CrossEntropy} = -\sum_{j} Y_{ij} \log(\hat{Y}_{ij})
$$

Since $Y_{ij}$ is one-hot, only the true class contributes to the loss.

**Embedding alternative**: For high-cardinality features, embedding layers learn dense representations rather than using sparse one-hot vectors.

---

## One-Hot vs Label Encoding

**Label encoding**: Categories mapped to integers [0, 1, 2, ...]
- Compact representation
- Implies ordinal relationship
- Used by tree-based models that can handle it

**One-hot encoding**: Categories mapped to binary vectors
- Larger representation
- No ordinal relationship
- Required by linear models and neural networks

---

## Where One-Hot Encoding Shows Up

- **Classification Targets**: Converting class labels to target vectors for training

- **Categorical Features**: Encoding nominal variables like color, country, product type

- **Neural Network Outputs**: Softmax outputs compared against one-hot targets

- **Sparse Matrices**: Efficient storage when most elements are zero

- **Attention Mechanisms**: Hard attention uses one-hot selection

- **Sequence-to-Sequence Models**: Target tokens one-hot encoded

- **Multi-Label Classification**: Extension where multiple positions can be 1

- **Feature Engineering**: Creating indicator variables for categorical attributes

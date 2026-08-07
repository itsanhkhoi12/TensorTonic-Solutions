## What Is Vector Normalization?

Vector normalization is the process of converting a vector into a **unit vector** (a vector with length 1) that points in the same direction as the original.

A normalized vector is also called a **unit vector** or **direction vector**.

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{||\mathbf{v}||}
$$

---

## Why Normalize Vectors?

**1. Direction without magnitude:**

When you only care about direction, not length. Example: surface normals for lighting.

**2. Simplified calculations:**

Many formulas simplify when vectors have unit length:
- Dot product becomes just $\cos(\theta)$
- No need to divide by magnitudes repeatedly

**3. Numerical stability:**

Keeping vectors normalized prevents values from growing unboundedly.

**4. Standard representation:**

Allows fair comparison between vectors of different original magnitudes.

---

## The Normalization Formula

For a 3D vector $\mathbf{v} = (v_x, v_y, v_z)$:

**Step 1:** Compute the magnitude (length):

$$
||\mathbf{v}|| = \sqrt{v_x^2 + v_y^2 + v_z^2}
$$

**Step 2:** Divide each component by the magnitude:

$$
\hat{\mathbf{v}} = \left( \frac{v_x}{||\mathbf{v}||}, \frac{v_y}{||\mathbf{v}||}, \frac{v_z}{||\mathbf{v}||} \right)
$$

---

## Properties of Normalized Vectors

**Unit length:**

$$
||\hat{\mathbf{v}}|| = 1
$$

**Same direction:**

$$
\hat{\mathbf{v}} \parallel \mathbf{v}
$$

**Scaling relationship:**

$$
\mathbf{v} = ||\mathbf{v}|| \cdot \hat{\mathbf{v}}
$$

Any vector equals its magnitude times its unit vector.

---

## Worked Example

**Vector:** $\mathbf{v} = (3, 4, 0)$

**Step 1: Compute magnitude**

$$
||\mathbf{v}|| = \sqrt{3^2 + 4^2 + 0^2} = \sqrt{9 + 16 + 0} = \sqrt{25} = 5
$$

**Step 2: Divide components**

$$
\hat{\mathbf{v}} = \left( \frac{3}{5}, \frac{4}{5}, \frac{0}{5} \right) = (0.6, 0.8, 0)
$$

**Verification:**

$$
||\hat{\mathbf{v}}|| = \sqrt{0.6^2 + 0.8^2 + 0^2} = \sqrt{0.36 + 0.64} = \sqrt{1} = 1 \checkmark
$$

---

## Another Example

**Vector:** $\mathbf{v} = (1, 2, 2)$

**Magnitude:**

$$
||\mathbf{v}|| = \sqrt{1^2 + 2^2 + 2^2} = \sqrt{1 + 4 + 4} = \sqrt{9} = 3
$$

**Normalized vector:**

$$
\hat{\mathbf{v}} = \left( \frac{1}{3}, \frac{2}{3}, \frac{2}{3} \right) \approx (0.333, 0.667, 0.667)
$$

**Verification:**

$$
||\hat{\mathbf{v}}|| = \sqrt{\frac{1}{9} + \frac{4}{9} + \frac{4}{9}} = \sqrt{\frac{9}{9}} = 1 \checkmark
$$

---

## Example with Non-Integer Components

**Vector:** $\mathbf{v} = (1, 1, 1)$

**Magnitude:**

$$
||\mathbf{v}|| = \sqrt{1 + 1 + 1} = \sqrt{3} \approx 1.732
$$

**Normalized vector:**

$$
\hat{\mathbf{v}} = \left( \frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}}, \frac{1}{\sqrt{3}} \right) \approx (0.577, 0.577, 0.577)
$$

This is the unit vector pointing equally in all three positive axis directions.

---

## The Zero Vector Problem

**Critical issue:** The zero vector $\mathbf{0} = (0, 0, 0)$ cannot be normalized.

$$
||\mathbf{0}|| = 0
$$

Division by zero is undefined. There is no "direction" for the zero vector.

**Handling:**
- Check if $||\mathbf{v}|| = 0$ (or $||\mathbf{v}|| < \epsilon$ for some small $\epsilon$)
- Return a default vector, raise an error, or handle specially

---

## Numerical Considerations

**Very small vectors:**

If $||\mathbf{v}||$ is extremely small (e.g., $10^{-15}$), division can cause numerical instability.

**Solution:** Use a threshold:

$$
\text{if } ||\mathbf{v}|| < \epsilon: \text{ handle specially}
$$

Typical $\epsilon$: $10^{-8}$ to $10^{-6}$

**Very large vectors:**

Computing $v_x^2 + v_y^2 + v_z^2$ can overflow for very large components.

**Solution:** Scale components first, or use numerically stable norm computation.

---

## Fast Inverse Square Root

In performance-critical applications (games, real-time graphics), the inverse magnitude is often needed:

$$
\frac{1}{||\mathbf{v}||} = \frac{1}{\sqrt{v_x^2 + v_y^2 + v_z^2}}
$$

The famous "fast inverse square root" algorithm (from Quake III) approximates this quickly. Modern CPUs have fast reciprocal square root instructions.

---

## Normalization in Different Norms

The L2 (Euclidean) norm is most common, but other norms exist:

**L1 normalization:**

$$
||\mathbf{v}||_1 = |v_x| + |v_y| + |v_z|
$$

**L$\infty$ normalization:**

$$
||\mathbf{v}||_\infty = \max(|v_x|, |v_y|, |v_z|)
$$

Each gives a different "unit" vector. L2 is standard for geometric applications.

---

## Applications in 3D Graphics

**Surface normals:**

Normals must be unit vectors for correct lighting calculations:

$$
\text{diffuse} = \max(0, \hat{\mathbf{n}} \cdot \hat{\mathbf{l}})
$$

**Direction vectors:**

Camera direction, light direction, velocity direction all benefit from normalization.

**Quaternion normalization:**

Unit quaternions represent rotations. Non-unit quaternions cause scaling artifacts.

---

## Applications in Physics

**Force direction:**

Separate magnitude and direction:

$$
\mathbf{F} = F \cdot \hat{\mathbf{d}}
$$

where $F$ is force magnitude and $\hat{\mathbf{d}}$ is direction.

**Velocity direction:**

Speed vs velocity direction:

$$
\mathbf{v} = |\mathbf{v}| \cdot \hat{\mathbf{v}}
$$

---

## Applications in Machine Learning

**Feature normalization:**

Normalize feature vectors to unit length for:
- Cosine similarity
- Spherical k-means
- Some neural network architectures

**Embeddings:**

Word embeddings, sentence embeddings often normalized before comparison.

**Gradient normalization:**

Gradient clipping by norm prevents exploding gradients.

---

## Normalizing Batches of Vectors

For efficiency, normalize many vectors at once:

**Given:** Matrix $V$ of shape $(n, 3)$ where each row is a vector

**Compute norms:** $||V_i||$ for each row

**Normalize:** Divide each row by its norm

Vectorized operations are much faster than loops.

---

## Re-normalization

After many operations, accumulated floating-point errors can cause "drift":

$$
||\hat{\mathbf{v}}|| \neq 1 \text{ (slightly)}
$$

**Solution:** Periodically re-normalize:

$$
\hat{\mathbf{v}} \leftarrow \frac{\hat{\mathbf{v}}}{||\hat{\mathbf{v}}||}
$$

Common in rotation representations (quaternions, rotation matrices).

---

## Relationship to Projection

Projection of $\mathbf{a}$ onto $\mathbf{b}$ uses the unit vector of $\mathbf{b}$:

$$
\text{proj}_{\mathbf{b}} \mathbf{a} = (\mathbf{a} \cdot \hat{\mathbf{b}}) \hat{\mathbf{b}}
$$

The scalar projection (component along $\mathbf{b}$):

$$
\text{comp}_{\mathbf{b}} \mathbf{a} = \mathbf{a} \cdot \hat{\mathbf{b}}
$$

---

## Generalizing to n Dimensions

The same formula works in any dimension:

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{||\mathbf{v}||} = \frac{\mathbf{v}}{\sqrt{\sum_{i=1}^{n} v_i^2}}
$$

High-dimensional unit vectors lie on the surface of an n-dimensional hypersphere.

---

## Common Mistakes

**1. Forgetting to check for zero vector:**

Always check $||\mathbf{v}|| > \epsilon$ before dividing.

**2. Normalizing in-place incorrectly:**

Must compute magnitude first, then divide all components. Do not divide $v_x$, then use modified $v_x$ for magnitude.

**3. Assuming already normalized:**

Do not assume input vectors are normalized unless explicitly documented.

**4. Accumulating numerical errors:**

Re-normalize periodically in iterative algorithms.
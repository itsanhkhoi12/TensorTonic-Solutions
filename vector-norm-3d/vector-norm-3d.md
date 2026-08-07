## What Is a Vector Norm?

A vector norm is a function that assigns a non-negative **length** or **magnitude** to a vector. It measures "how big" the vector is.

The most common norm in 3D geometry is the **Euclidean norm** (L2 norm), which corresponds to the straight-line distance from the origin.

---

## The Euclidean Norm (L2 Norm)

For a 3D vector $\mathbf{v} = (v_x, v_y, v_z)$:

$$
||\mathbf{v}||_2 = \sqrt{v_x^2 + v_y^2 + v_z^2}
$$

This is the distance from the origin to the point $(v_x, v_y, v_z)$ in 3D space.

When the subscript is omitted, $||\mathbf{v}||$ usually means the L2 norm.

---

## Geometric Interpretation

The Euclidean norm represents:

**1. Length of the vector:**

The straight-line distance from the origin to the vector's tip.

**2. Magnitude of a quantity:**

Speed (magnitude of velocity), force magnitude, etc.

**3. Distance in 3D space:**

The distance from point A to point B is $||\mathbf{B} - \mathbf{A}||$.

---

## Derivation from Pythagorean Theorem

In 2D, the Pythagorean theorem gives:

$$
||\mathbf{v}||^2 = v_x^2 + v_y^2
$$

In 3D, we apply it twice:

First in the XY-plane: $d_{xy}^2 = v_x^2 + v_y^2$

Then from XY to Z: $||\mathbf{v}||^2 = d_{xy}^2 + v_z^2 = v_x^2 + v_y^2 + v_z^2$

---

## Worked Example 1

**Vector:** $\mathbf{v} = (3, 4, 0)$

$$
||\mathbf{v}|| = \sqrt{3^2 + 4^2 + 0^2} = \sqrt{9 + 16 + 0} = \sqrt{25} = 5
$$

This is the classic 3-4-5 right triangle in the XY-plane.

---

## Worked Example 2

**Vector:** $\mathbf{v} = (1, 2, 2)$

$$
||\mathbf{v}|| = \sqrt{1^2 + 2^2 + 2^2} = \sqrt{1 + 4 + 4} = \sqrt{9} = 3
$$

---

## Worked Example 3

**Vector:** $\mathbf{v} = (1, 1, 1)$

$$
||\mathbf{v}|| = \sqrt{1^2 + 1^2 + 1^2} = \sqrt{3} \approx 1.732
$$

This is the space diagonal of a unit cube.

---

## Properties of Norms

**1. Non-negativity:**

$$
||\mathbf{v}|| \geq 0
$$

**2. Zero only for zero vector:**

$$
||\mathbf{v}|| = 0 \iff \mathbf{v} = \mathbf{0}
$$

**3. Scalar multiplication:**

$$
||c\mathbf{v}|| = |c| \cdot ||\mathbf{v}||
$$

**4. Triangle inequality:**

$$
||\mathbf{u} + \mathbf{v}|| \leq ||\mathbf{u}|| + ||\mathbf{v}||
$$

---

## The Squared Norm

Often, we use the **squared norm** to avoid computing square roots:

$$
||\mathbf{v}||^2 = v_x^2 + v_y^2 + v_z^2
$$

**Benefits:**
- Faster computation (no square root)
- Preserves ordering: $||\mathbf{a}|| < ||\mathbf{b}|| \iff ||\mathbf{a}||^2 < ||\mathbf{b}||^2$
- Used in many optimization problems

---

## Relationship to Dot Product

The squared norm equals the dot product with itself:

$$
||\mathbf{v}||^2 = \mathbf{v} \cdot \mathbf{v} = v_x^2 + v_y^2 + v_z^2
$$

Therefore:

$$
||\mathbf{v}|| = \sqrt{\mathbf{v} \cdot \mathbf{v}}
$$

This relationship is fundamental in linear algebra.

---

## Other Common Norms

**L1 Norm (Manhattan norm):**

$$
||\mathbf{v}||_1 = |v_x| + |v_y| + |v_z|
$$

Distance traveling along axis-aligned paths.

**L$\infty$ Norm (Maximum norm):**

$$
||\mathbf{v}||_\infty = \max(|v_x|, |v_y|, |v_z|)
$$

The largest component magnitude.

**Lp Norm (General):**

$$
||\mathbf{v}||_p = \left( |v_x|^p + |v_y|^p + |v_z|^p \right)^{1/p}
$$

L2 is the case $p = 2$.

---

## Comparing Norms

For the same vector $\mathbf{v} = (3, 4, 0)$:

$$
||\mathbf{v}||_1 = 3 + 4 + 0 = 7
$$

$$
||\mathbf{v}||_2 = \sqrt{9 + 16} = 5
$$

$$
||\mathbf{v}||_\infty = \max(3, 4, 0) = 4
$$

In general: $||\mathbf{v}||_\infty \leq ||\mathbf{v}||_2 \leq ||\mathbf{v}||_1$

---

## Distance Between Points

The Euclidean distance between points $\mathbf{A}$ and $\mathbf{B}$:

$$
d(\mathbf{A}, \mathbf{B}) = ||\mathbf{B} - \mathbf{A}|| = \sqrt{(B_x - A_x)^2 + (B_y - A_y)^2 + (B_z - A_z)^2}
$$

**Example:** Distance from $(1, 2, 3)$ to $(4, 6, 3)$:

$$
d = \sqrt{(4-1)^2 + (6-2)^2 + (3-3)^2} = \sqrt{9 + 16 + 0} = 5
$$

---

## Unit Vectors

A unit vector has norm equal to 1:

$$
||\hat{\mathbf{v}}|| = 1
$$

To create a unit vector (normalization):

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{||\mathbf{v}||}
$$

Unit vectors represent pure direction without magnitude.

---

## Applications in 3D Graphics

**Distance calculations:**
- Object collision detection
- Level of detail selection
- Culling (discard far objects)

**Lighting:**
- Light attenuation: $I \propto \frac{1}{||\mathbf{r}||^2}$
- Normal vectors (must be unit length)

**Animation:**
- Speed = norm of velocity vector
- Interpolation distances

---

## Applications in Physics

**Magnitude of vectors:**
- Speed: $|v| = ||\mathbf{v}||$
- Force: $|F| = ||\mathbf{F}||$
- Acceleration: $|a| = ||\mathbf{a}||$

**Energy:**
- Kinetic energy: $KE = \frac{1}{2}m||\mathbf{v}||^2$

**Work:**
- Uses dot product which relates to norms

---

## Applications in Machine Learning

**Distance metrics:**
- k-NN classification uses Euclidean distance
- Clustering algorithms (k-means)

**Regularization:**
- L2 regularization (Ridge): $\lambda ||\mathbf{w}||^2_2$
- L1 regularization (Lasso): $\lambda ||\mathbf{w}||_1$

**Loss functions:**
- Mean Squared Error uses squared L2 norm
- Mean Absolute Error uses L1 norm

---

## Numerical Considerations

**Overflow:**

For very large components, $v_x^2$ might overflow.

**Solution:** Use logarithms or scale before squaring.

**Underflow:**

For very small components, $v_x^2$ might underflow to zero.

**Solution:** Use extended precision or relative comparisons.

**Catastrophic cancellation:**

When components have very different magnitudes, small components may be lost.

---

## Efficient Computation

**Avoid redundant square roots:**

When comparing distances, use squared norms:

$$
||\mathbf{a}|| < ||\mathbf{b}|| \iff ||\mathbf{a}||^2 < ||\mathbf{b}||^2
$$

**SIMD optimization:**

Modern CPUs can compute $v_x^2 + v_y^2 + v_z^2$ in parallel.

**Batch computation:**

For many vectors, process in batches using matrix operations.

---

## Generalizing to n Dimensions

The formula extends to any dimension:

$$
||\mathbf{v}||_2 = \sqrt{\sum_{i=1}^{n} v_i^2}
$$

In high-dimensional spaces, distances behave differently (curse of dimensionality), but the formula remains the same.

---

## Norm Inequalities

**Cauchy-Schwarz inequality:**

$$
|\mathbf{u} \cdot \mathbf{v}| \leq ||\mathbf{u}|| \cdot ||\mathbf{v}||
$$

**Triangle inequality:**

$$
||\mathbf{u} + \mathbf{v}|| \leq ||\mathbf{u}|| + ||\mathbf{v}||
$$

**Reverse triangle inequality:**

$$
||\mathbf{u} - \mathbf{v}|| \geq | ||\mathbf{u}|| - ||\mathbf{v}|| |
$$

These are fundamental properties used in proofs and algorithms.
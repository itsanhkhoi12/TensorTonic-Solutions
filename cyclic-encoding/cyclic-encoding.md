## What Is Cyclic Encoding?

Cyclic encoding (also called circular encoding or trigonometric encoding) is a technique for representing features that have a cyclical or periodic nature. It transforms a single cyclic feature into two features using sine and cosine functions, preserving the circular relationship between values.

This is essential for features like hours of the day, days of the week, months of the year, or angles.

---

## The Problem with Linear Encoding

Consider the hour of the day (0-23):

**With simple integer encoding:**

- Hour 23 is encoded as 23
- Hour 0 is encoded as 0

The numerical difference is 23, but these hours are actually adjacent (just 1 hour apart).

**The issue:** Linear encoding does not capture that the feature wraps around. The model sees 23 and 0 as very different, when they should be very similar.

---

## The Solution: Sine and Cosine

Transform the cyclic feature using trigonometric functions:

$$
x_{sin} = \sin\left(\frac{2\pi \cdot x}{\text{period}}\right)
$$

$$
x_{cos} = \cos\left(\frac{2\pi \cdot x}{\text{period}}\right)
$$

where:
- $x$ is the original value
- period is the length of one complete cycle

---

## Why Sine AND Cosine?

Using only sine would create ambiguity:

$$
\sin(30°) = \sin(150°) = 0.5
$$

Two different values map to the same sine value.

**Combining both resolves ambiguity:**

- $\sin(30°) = 0.5$, $\cos(30°) = 0.866$
- $\sin(150°) = 0.5$, $\cos(150°) = -0.866$

The pair $(\sin, \cos)$ uniquely identifies every point on the cycle.

---

## Geometric Interpretation

The transformation maps each value to a point on the unit circle:

$$
(x_{cos}, x_{sin}) = (\cos(\theta), \sin(\theta))
$$

where $\theta = \frac{2\pi \cdot x}{\text{period}}$

**Properties of points on unit circle:**

- All points have distance 1 from origin
- Adjacent cyclic values map to adjacent points on the circle
- Values that wrap around (like hour 23 and hour 0) are close on the circle

---

## Hour of Day Example

**Feature:** Hour (0-23)

**Period:** 24 hours

**Formula:**

$$
\text{hour}_{sin} = \sin\left(\frac{2\pi \cdot \text{hour}}{24}\right)
$$

$$
\text{hour}_{cos} = \cos\left(\frac{2\pi \cdot \text{hour}}{24}\right)
$$

**Calculations for specific hours:**

Hour 0:
- $\sin(0) = 0$
- $\cos(0) = 1$
- Encoded: (0, 1)

Hour 6:
- $\sin(\pi/2) = 1$
- $\cos(\pi/2) = 0$
- Encoded: (1, 0)

Hour 12:
- $\sin(\pi) = 0$
- $\cos(\pi) = -1$
- Encoded: (0, -1)

Hour 18:
- $\sin(3\pi/2) = -1$
- $\cos(3\pi/2) = 0$
- Encoded: (-1, 0)

---

## Verifying Adjacency is Preserved

**Hour 23 vs Hour 0:**

Hour 23:
- $\sin(2\pi \cdot 23/24) = \sin(23\pi/12) \approx -0.259$
- $\cos(2\pi \cdot 23/24) = \cos(23\pi/12) \approx 0.966$

Hour 0:
- $\sin(0) = 0$
- $\cos(0) = 1$

**Euclidean distance:**

$$
d = \sqrt{(0 - (-0.259))^2 + (1 - 0.966)^2} = \sqrt{0.067 + 0.001} \approx 0.261
$$

This is the same distance as between any two adjacent hours, confirming the cyclic relationship is preserved.

---

## Day of Week Example

**Feature:** Day (0-6, where 0 = Sunday)

**Period:** 7 days

**Formula:**

$$
\text{day}_{sin} = \sin\left(\frac{2\pi \cdot \text{day}}{7}\right)
$$

$$
\text{day}_{cos} = \cos\left(\frac{2\pi \cdot \text{day}}{7}\right)
$$

**Sample values:**

- Sunday (0): (0, 1)
- Monday (1): (0.782, 0.623)
- Tuesday (2): (0.975, -0.223)
- Wednesday (3): (0.434, -0.901)
- Thursday (4): (-0.434, -0.901)
- Friday (5): (-0.975, -0.223)
- Saturday (6): (-0.782, 0.623)

---

## Month of Year Example

**Feature:** Month (1-12 or 0-11)

**Period:** 12 months

**Formula (if months are 1-12):**

$$
\text{month}_{sin} = \sin\left(\frac{2\pi \cdot (\text{month} - 1)}{12}\right)
$$

$$
\text{month}_{cos} = \cos\left(\frac{2\pi \cdot (\text{month} - 1)}{12}\right)
$$

Note: Subtract 1 if months start at 1 to make the range 0-11.

**Key insight:** December (12) and January (1) will be close in the encoded space.

---

## Angle Encoding

**Feature:** Angle in degrees (0-360)

**Period:** 360 degrees

**Formula:**

$$
\text{angle}_{sin} = \sin\left(\frac{2\pi \cdot \text{angle}}{360}\right) = \sin(\text{angle in radians})
$$

$$
\text{angle}_{cos} = \cos\left(\frac{2\pi \cdot \text{angle}}{360}\right) = \cos(\text{angle in radians})
$$

**For radians (0 to $2\pi$):**

Simply use $\sin(\text{angle})$ and $\cos(\text{angle})$ directly.

---

## Wind Direction Example

**Feature:** Wind direction (0-359 degrees, where 0 = North)

**Period:** 360 degrees

**Sample encodings:**

- North (0°): (0, 1)
- East (90°): (1, 0)
- South (180°): (0, -1)
- West (270°): (-1, 0)
- North-East (45°): (0.707, 0.707)

**Benefit:** Directions 359° and 1° are correctly recognized as close (both near North).

---

## Mathematical Properties

**1. Bounded output:**

Both sine and cosine are bounded in $[-1, 1]$.

**2. Continuous:**

Small changes in input produce small changes in output.

**3. Periodic:**

Values that differ by exactly one period map to the same point.

**4. Pythagorean identity:**

$$
\sin^2(\theta) + \cos^2(\theta) = 1
$$

All encoded points lie on the unit circle.

---

## Distance Between Cyclic Values

The Euclidean distance in the encoded space reflects the true cyclic distance:

$$
d = \sqrt{(\sin(\theta_1) - \sin(\theta_2))^2 + (\cos(\theta_1) - \cos(\theta_2))^2}
$$

This can be simplified using trigonometric identities:

$$
d = 2\sin\left(\frac{|\theta_1 - \theta_2|}{2}\right)
$$

Maximum distance is 2 (for values half a period apart).

---

## Comparison with One-Hot Encoding

**One-hot encoding for hours (24 features):**

- Hour 0: [1, 0, 0, ..., 0]
- Hour 1: [0, 1, 0, ..., 0]
- ...
- Hour 23: [0, 0, 0, ..., 1]

**Problems:**

- High dimensionality (24 features vs 2)
- Does not capture that hour 23 and 0 are adjacent
- Treats all non-matching hours as equally different

**Cyclic encoding advantages:**

- Only 2 features
- Preserves cyclic relationships
- More compact representation

---

## Comparison with Ordinal Encoding

**Ordinal encoding:** Hour = 0, 1, 2, ..., 23

**Problems:**

- Hour 23 and 0 appear maximally different (difference of 23)
- Model may incorrectly learn that hour 23 > hour 0 in a meaningful way

**Cyclic encoding fixes this** by making hour 23 and hour 0 close in the feature space.

---

## When to Use Cyclic Encoding

**Good use cases:**

- Time features: hour, minute, second
- Calendar features: day of week, month, day of year
- Angles: wind direction, compass heading, rotation
- Periodic measurements: phase in a wave, seasonal patterns

**Not appropriate for:**

- Non-cyclic ordinal features (education level, rankings)
- Categorical features without natural ordering
- Features where the cycle is not meaningful

---

## Handling Different Ranges

**General formula for range [a, b] with period = b - a:**

$$
x_{sin} = \sin\left(\frac{2\pi \cdot (x - a)}{b - a}\right)
$$

$$
x_{cos} = \cos\left(\frac{2\pi \cdot (x - a)}{b - a}\right)
$$

This shifts the range to start at 0 before applying the transformation.

---

## Multiple Cyclic Features

When you have multiple cyclic features, encode each separately:

**Example: Timestamp with hour and day of week**

- hour_sin, hour_cos (from hour)
- dow_sin, dow_cos (from day of week)

Total: 4 encoded features from 2 original features.

---

## Cyclic Encoding in Time Series

For time series with multiple seasonal patterns:

**Daily seasonality:** Encode hour of day

**Weekly seasonality:** Encode day of week

**Yearly seasonality:** Encode day of year (period = 365 or 366)

Multiple encodings can capture multiple overlapping cycles.

---

## Combining with Other Features

Cyclic encoded features can be:

- Used directly in any model
- Combined with other numerical features
- Used to create interaction features

**Example:** hour_sin * temperature might capture how temperature effect varies by time of day.

---

## Numerical Precision

**Near boundaries:**

At exactly 0 and $2\pi$:
- $\sin(0) = 0$, but $\sin(2\pi) \approx 0$ (small numerical error)
- $\cos(0) = 1 = \cos(2\pi)$

**Mitigation:** The errors are typically negligible for machine learning purposes.

---

## Alternative: Radial Basis Functions

Another approach for cyclic features:

Create Gaussian bumps at regular intervals around the cycle:

$$
f_i(x) = \exp\left(-\frac{(x - c_i)^2}{2\sigma^2}\right)
$$

where $c_i$ are center points and distance is measured cyclically.

This creates more features but can capture more complex patterns.

---

## Common Mistakes

**1. Forgetting to use both sine and cosine:**

Using only sine loses information and creates ambiguity.

**2. Wrong period:**

Using period = 23 for hours instead of 24 (hours go 0-23 but period is 24).

**3. Not handling the range correctly:**

If months are 1-12, need to adjust to 0-11 before encoding.

**4. Using cyclic encoding for non-cyclic features:**

Age is not cyclic (90 should not be close to 0).

---

## Benefits Summary

**1. Compact representation:** 2 features instead of many one-hot columns

**2. Preserves cyclic nature:** Adjacent values remain adjacent after encoding

**3. Continuous:** Works well with gradient-based optimization

**4. Scale-invariant:** Output always in $[-1, 1]$

**5. Works with any model:** Linear models, trees, neural networks all benefit
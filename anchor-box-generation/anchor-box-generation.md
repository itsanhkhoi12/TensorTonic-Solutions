## What Are Anchor Boxes?

Anchor boxes (also called prior boxes or default boxes) are predefined bounding boxes used in object detection. Instead of predicting box coordinates from scratch, the network predicts adjustments to these anchors.

Key idea: scatter anchors densely across the image, then classify each anchor as containing an object or not, and refine the box coordinates.

---

## Why Use Anchors?

**Problem without anchors:**
- Network must predict absolute coordinates (x, y, width, height)
- Large search space
- Hard to learn

**With anchors:**
- Network predicts small offsets from known positions
- Each anchor is a "guess" that the network refines
- Much easier optimization problem

This is analogous to regression: predicting residuals from a baseline is easier than predicting raw values.

---

## Anchor Parameters

Anchors are defined by:

**Position (from feature map grid):**
- Each cell in the feature map generates anchors
- Anchor center is at the cell center in image coordinates

**Scale:**
- The base size of the anchor
- Example: 32, 64, 128 pixels

**Aspect ratio:**
- Width-to-height ratio
- Example: 1:1 (square), 1:2 (tall), 2:1 (wide)

Each combination of (position, scale, aspect ratio) produces one anchor.

---

## Grid to Image Coordinates

The feature map is smaller than the image (due to pooling/striding). To map grid positions to image coordinates:

$$
\text{stride} = \frac{\text{image size}}{\text{feature size}}
$$

For grid cell $(i, j)$:

$$
c_x = (j + 0.5) \times \text{stride}
$$

$$
c_y = (i + 0.5) \times \text{stride}
$$

The +0.5 places the anchor at the cell center.

---

## Computing Anchor Dimensions

Given scale $s$ and aspect ratio $r$:

$$
w = s \cdot \sqrt{r}
$$

$$
h = \frac{s}{\sqrt{r}}
$$

This ensures the anchor area is approximately $s^2$ regardless of aspect ratio.

**Example with scale=64, ratio=2 (wide):**
- w = 64 * sqrt(2) = 90.5
- h = 64 / sqrt(2) = 45.3
- Area = 90.5 * 45.3 = 4099 (close to 64^2 = 4096)

---

## Anchor Box Coordinates

The anchor box in (x1, y1, x2, y2) format:

$$
x_1 = c_x - \frac{w}{2}, \quad y_1 = c_y - \frac{h}{2}
$$

$$
x_2 = c_x + \frac{w}{2}, \quad y_2 = c_y + \frac{h}{2}
$$

---

## Numerical Example

**Parameters:**
- Feature size: 2x2
- Image size: 8
- Scales: [2, 4]
- Aspect ratios: [1.0, 2.0]

**Stride:** 8 / 2 = 4

**Cell (0, 0) center:** cx = 0.5 * 4 = 2, cy = 0.5 * 4 = 2

**Anchors at (0, 0):**

Scale 2, ratio 1.0:
- w = 2 * 1 = 2, h = 2 / 1 = 2
- Box: [2-1, 2-1, 2+1, 2+1] = [1, 1, 3, 3]

Scale 2, ratio 2.0:
- w = 2 * 1.41 = 2.83, h = 2 / 1.41 = 1.41
- Box: [2-1.41, 2-0.71, 2+1.41, 2+0.71] = [0.59, 1.29, 3.41, 2.71]

Scale 4, ratio 1.0:
- w = 4, h = 4
- Box: [0, 0, 4, 4]

Scale 4, ratio 2.0:
- w = 5.66, h = 2.83
- Box: [-0.83, 0.59, 4.83, 3.41]

And so on for all 4 cells...

---

## Total Number of Anchors

$$
\text{Total anchors} = H_{feat} \times W_{feat} \times |\text{scales}| \times |\text{ratios}|
$$

For a 50x50 feature map with 3 scales and 3 ratios:
- 50 * 50 * 3 * 3 = 22,500 anchors

This dense coverage ensures at least one anchor will overlap well with any object.

---

## Anchor Matching

During training, each anchor is matched to ground truth:

**Positive anchor:**
- IoU with some ground truth box >= 0.7
- Or highest IoU anchor for each ground truth

**Negative anchor:**
- IoU with all ground truth boxes < 0.3

**Ignored:**
- IoU between 0.3 and 0.7
- Not used for training

---

## Multi-Scale Anchors

Modern detectors use anchors at multiple feature map resolutions:

**Small feature map (coarse):**
- Large receptive field
- Large anchors
- Detects big objects

**Large feature map (fine):**
- Small receptive field
- Small anchors
- Detects small objects

This is the Feature Pyramid Network (FPN) approach used in many state-of-the-art detectors.

---

## Architectures Using Anchors

**Faster R-CNN:**
- Region Proposal Network (RPN) generates proposals from anchors
- 9 anchors per position (3 scales x 3 ratios)

**SSD (Single Shot Detector):**
- Anchors at multiple feature map levels
- Different scales at different levels

**RetinaNet:**
- 9 anchors per position
- FPN backbone for multi-scale detection

**YOLO v2+:**
- Learned anchor dimensions from data (k-means clustering)
- Called "anchor priors"

---

## Anchor-Free Alternatives

Recent detectors avoid anchors entirely:

**FCOS:**
- Predicts distance to box boundaries from each point
- No anchor hyperparameters to tune

**CenterNet:**
- Predicts object centers as heatmaps
- Predicts size at each center

Anchor-free methods are simpler but anchors remain competitive.
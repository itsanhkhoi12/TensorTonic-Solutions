## What Is a Histogram?

A histogram counts how many times each value appears in a dataset. For grayscale images, it counts how many pixels have each possible intensity value (0 to 255).

The histogram is a 1D array of 256 bins:
- bin[0]: count of pixels with value 0 (black)
- bin[127]: count of pixels with value 127 (mid-gray)
- bin[255]: count of pixels with value 255 (white)

---

## Why Histograms Matter

**Image analysis:**
- Reveals overall brightness (left-skewed = dark, right-skewed = bright)
- Shows contrast (narrow spread = low contrast, wide spread = high contrast)
- Identifies clipping (spikes at 0 or 255)

**Image processing:**
- Automatic thresholding (find valleys in bimodal histograms)
- Histogram equalization (improve contrast)
- Exposure correction

**Computer vision:**
- Image comparison (histogram similarity)
- Object recognition (color histograms)
- Content-based image retrieval

---

## Computing a Histogram

**Step 1: Initialize bins**
- Create array of 256 zeros

**Step 2: Iterate through pixels**
- For each pixel value v:
  - Increment bin[v]

**Step 3: Result**
- histogram[i] = count of pixels with intensity i

---

## Numerical Example

**Small 4x4 image:**

0   50  50  100
0   50  100 100
50  100 150 200
100 150 200 255

**Counting:**
- Value 0 appears 2 times
- Value 50 appears 4 times
- Value 100 appears 5 times
- Value 150 appears 2 times
- Value 200 appears 2 times
- Value 255 appears 1 time
- All other values appear 0 times

**Histogram (non-zero bins only):**
- histogram[0] = 2
- histogram[50] = 4
- histogram[100] = 5
- histogram[150] = 2
- histogram[200] = 2
- histogram[255] = 1

Total: 2 + 4 + 5 + 2 + 2 + 1 = 16 (total pixels)

---

## Interpreting Histograms

**Dark image:**
- Most pixels have low values
- Histogram concentrated on the left
- Few pixels in bright regions

**Bright image:**
- Most pixels have high values
- Histogram concentrated on the right
- Few pixels in dark regions

**Low contrast:**
- Pixels clustered in a narrow range
- Histogram has a narrow peak
- Image looks "washed out"

**High contrast:**
- Pixels spread across full range
- Histogram is wide and relatively flat
- Image has both dark and bright regions

**Bimodal:**
- Two distinct peaks
- Often indicates foreground vs. background
- Useful for thresholding

---

## Normalized Histogram

A normalized histogram converts counts to probabilities:

$$
p[i] = \frac{\text{histogram}[i]}{\text{total pixels}}
$$

Properties:
- All values between 0 and 1
- Sum of all bins equals 1
- Represents probability distribution of intensities

---

## Cumulative Histogram

The cumulative histogram counts pixels up to each intensity:

$$
C[i] = \sum_{j=0}^{i} \text{histogram}[j]
$$

Properties:
- Monotonically increasing
- C[255] = total number of pixels
- Used in histogram equalization

---

## Applications

**Automatic thresholding (Otsu's method):**
- Find threshold that maximizes between-class variance
- Uses histogram to separate foreground and background

**Histogram equalization:**
- Spread pixel values to fill full range
- Improves contrast
- Uses cumulative histogram

**Histogram matching:**
- Transform image so its histogram matches a target
- Used for color normalization

**Exposure detection:**
- Check for clipping (many pixels at 0 or 255)
- Identify over/under exposure

---

## Color Histograms

For color images, compute separate histograms for each channel:
- Red histogram (256 bins)
- Green histogram (256 bins)
- Blue histogram (256 bins)

Or compute joint histogram:
- 256 x 256 x 256 = 16.7 million bins (impractical)
- Instead, reduce to fewer bins (e.g., 8 x 8 x 8 = 512 bins)

---

## Implementation Notes

**Efficiency:**
- Single pass through image: O(H * W)
- Each pixel: one array access and increment

**Memory:**
- Only 256 integers needed (1 KB for 32-bit ints)
- Very lightweight data structure

**Edge cases:**
- Empty image: all bins are 0
- Uniform image: one bin equals H*W, others are 0
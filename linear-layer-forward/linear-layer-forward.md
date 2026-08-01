## The Building Block of Neural Networks

The linear layer (also called a fully connected layer, dense layer, or affine transformation) is the most fundamental operation in deep learning. Nearly every neural network architecture uses linear layers as core components.

A linear layer transforms an input vector $x$ of dimension $d_{in}$ into an output vector $y$ of dimension $d_{out}$ using:

$$
y = Wx + b
$$

Where:
- $W$ is a weight matrix of shape $d_{out} \times d_{in}$
- $b$ is a bias vector of shape $d_{out}$
- $x$ is the input vector of shape $d_{in}$
- $y$ is the output vector of shape $d_{out}$

---

## Breaking Down the Computation

Each output neuron $y_j$ computes a weighted sum of all inputs plus a bias:

$$
y_j = \sum_{i=1}^{d_{in}} W_{ji} x_i + b_j
$$

In words: the $j$-th output is the dot product of the $j$-th row of $W$ with the input $x$, plus the $j$-th bias.

---

## A Concrete Example

**Input:** $x = [1, 2, 3]$ (3 features)

**Weights:** 

$$
W = \begin{bmatrix} 0.1 & 0.2 & 0.3 \\ 0.4 & 0.5 & 0.6 \end{bmatrix}
$$
(2 output neurons, 3 input features)

**Bias:** $b = [0.1, 0.2]$

**Computing output 1:**

$$
y_1 = (0.1)(1) + (0.2)(2) + (0.3)(3) + 0.1 = 0.1 + 0.4 + 0.9 + 0.1 = 1.5
$$

**Computing output 2:**

$$
y_2 = (0.4)(1) + (0.5)(2) + (0.6)(3) + 0.2 = 0.4 + 1.0 + 1.8 + 0.2 = 3.4
$$

**Result:** $y = [1.5, 3.4]$

The 3-dimensional input has been transformed into a 2-dimensional output.

---

## Batch Processing

In practice, we process many samples at once. If $X$ is a matrix of shape $n \times d_{in}$ (n samples, each with $d_{in}$ features), the batched computation is:

$$
Y = XW^T + b
$$

Or equivalently, if $W$ is stored as $d_{in} \times d_{out}$:

$$
Y = XW + b
$$

Here:
- $X$ is $n \times d_{in}$
- $W$ is $d_{in} \times d_{out}$
- $Y$ is $n \times d_{out}$
- $b$ is broadcast to each row (added to all samples)

Each row of $Y$ is the transformed version of the corresponding row of $X$.

---

## Why Linear Layers Are Called "Affine"

A purely linear transformation would be $y = Wx$ with no bias. This maps the origin to the origin.

Adding the bias $b$ makes it an affine transformation: $y = Wx + b$. Affine transformations can shift the origin, allowing the network to learn offsets.

Without biases, a network could only learn functions that pass through the origin. The bias term provides essential flexibility.

---

## What Linear Layers Cannot Do

A single linear layer is severely limited. Composing two linear layers without nonlinearity between them is equivalent to a single linear layer:

$$
y = W_2(W_1 x + b_1) + b_2 = (W_2 W_1)x + (W_2 b_1 + b_2) = W' x + b'
$$

No matter how many linear layers you stack, the result is still a linear function. This is why nonlinear activation functions (ReLU, sigmoid, etc.) are inserted between linear layers.

---

## The Role of Each Component

**Weights $W$:**
- Learned parameters that determine how inputs are combined
- Each row of $W$ defines what pattern one output neuron looks for
- A neuron with weights $[1, -1, 0]$ computes "first input minus second input"

**Biases $b$:**
- Learned parameters that shift the activation
- Allow neurons to activate even when the weighted sum is zero
- One bias per output neuron

**Input $x$:**
- The data or the output from the previous layer
- Can represent raw features, embeddings, or intermediate representations

---

## The Gradient (Backpropagation)

During training, we need gradients to update $W$ and $b$.

**Gradient with respect to $W$:**

$$
\frac{\partial L}{\partial W} = \frac{\partial L}{\partial y} \cdot x^T
$$

**Gradient with respect to $b$:**

$$
\frac{\partial L}{\partial b} = \frac{\partial L}{\partial y}
$$

**Gradient with respect to $x$ (for backpropagating to earlier layers):**

$$
\frac{\partial L}{\partial x} = W^T \cdot \frac{\partial L}{\partial y}
$$

Notice how $W^T$ appears in the backward pass. The transpose of the weight matrix routes gradients back through the network.

---

## Linear Layers in Different Contexts

**Feedforward networks:**

Linear layers alternate with activations: Linear -> ReLU -> Linear -> ReLU -> ... -> Linear -> Output

**Classification:**

The final linear layer typically has one output per class. Its outputs (logits) are passed through softmax for probabilities.

**Regression:**

The final linear layer has one output per target variable. No activation is applied (or sometimes ReLU for non-negative outputs).

**Transformers:**

The feedforward blocks in transformers consist of two linear layers with a nonlinearity between them. The attention mechanism also involves several linear projections.

---

## Parameter Count

A linear layer mapping $d_{in}$ inputs to $d_{out}$ outputs has:
- $d_{in} \times d_{out}$ weights
- $d_{out}$ biases
- Total: $d_{in} \times d_{out} + d_{out}$ parameters

For a layer with 1000 inputs and 500 outputs: $1000 \times 500 + 500 = 500,500$ parameters.

This can become very large, which is why modern architectures often use techniques like attention or convolution to reduce parameter counts.
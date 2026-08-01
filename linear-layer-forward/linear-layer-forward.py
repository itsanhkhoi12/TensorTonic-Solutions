def linear_layer_forward(X, W, b):
    """
    Compute the forward pass of a linear (fully connected) layer.
    """
    n = len(X)
    d_in = len(X[0])
    d_out = len(W[0])
    return [[sum(X[i][k] * W[k][j] for k in range(d_in)) + b[j]
             for j in range(d_out)] for i in range(n)]
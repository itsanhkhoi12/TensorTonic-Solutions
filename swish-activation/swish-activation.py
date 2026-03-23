import numpy as np

def swish(x):
    """
    Implement Swish activation function.
    """
    # Write code here
    x = np.array(x)
    sigmoid_at_x = 1/(1+np.exp(-x))
    return x*sigmoid_at_x
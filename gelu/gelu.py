import numpy as np
import math

def gelu(x):
    """
    Compute the Gaussian Error Linear Unit (exact version using erf).
    x: list or np.ndarray
    Return: np.ndarray of same shape (dtype=float)
    """
    # Write code here
    erf_vector = np.vectorize(math.erf)
    x = np.array(x)
    return 0.5*x*(1+erf_vector(x/np.sqrt(2)))
    
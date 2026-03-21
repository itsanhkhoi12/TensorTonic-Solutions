import numpy as np

def matrix_trace(A):
    """
    Compute the trace of a square matrix (sum of diagonal elements).
    """
    # Write code here
    trace = 0
    n = len(A)
    for i in range(n):
        trace+=A[i][i]
    return trace

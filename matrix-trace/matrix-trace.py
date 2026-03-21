import numpy as np

def matrix_trace(A):
    """
    Compute the trace of a square matrix (sum of diagonal elements).
    """
    # Write code here
    trace = 0
    n = len(A)

    if n == 1:
        trace = A.pop().pop()
        return trace
    else:
        for i in range(n):
            for j in range(n):
                if i==j:
                    trace+=A[i][j]
        return trace

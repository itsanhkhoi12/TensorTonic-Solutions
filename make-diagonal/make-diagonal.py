import numpy as np

def make_diagonal(v):
    """
    Returns: (n, n) NumPy array with v on the main diagonal
    """
    # Write code here
    n = len(v)
    if n==1:
        return np.array([v])
    else:
        diagonal_matrix = np.zeros((n,n))
        for i in range(n):
            diagonal_matrix[i,i] = v[i]
        return diagonal_matrix
    
    
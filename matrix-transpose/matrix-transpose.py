import numpy as np

def matrix_transpose(A):
    """
    Return the transpose of matrix A (swap rows and columns).
    """
    # Write code here
    vector_nums, dims = len(A), len(A[0])
    transposed_A = []
    for i in range(dims):
        transposed_vector = []
        for j in range(vector_nums):
            transposed_vector.append(A[j][i])
        transposed_A.append(transposed_vector)
    return np.array(transposed_A)

import numpy as np

def matrix_factorization_sgd_step(U, V, r, lr, reg):
    """
    Perform one SGD step for matrix factorization.
    """
    # Write code here
    U, V = np.array(U), np.array(V)
    dot_prod = U@V
    e = r - dot_prod
    U_new = U + lr *(e*V - reg*U)
    V_new = V + lr *(e*U - reg*V)
    return U_new, V_new
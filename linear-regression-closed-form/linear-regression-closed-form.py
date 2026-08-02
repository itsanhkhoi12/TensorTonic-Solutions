import numpy as np

def linear_regression_closed_form(X, y):
    """
    Compute the optimal weight vector using the normal equation.
    """
    # Write code here
    X = np.array(X)
    y = np.array(y)
    X_T = np.array(X).T
    inv = np.linalg.inv(X_T@X)
    return inv@(X_T@y)
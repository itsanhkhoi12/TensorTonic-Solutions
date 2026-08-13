import numpy as np

def compute_gradient_norm_decay(T: int, W_hh: np.ndarray) -> list:
    """
    Simulate gradient norm decay over T time steps.
    Returns list of gradient norms.
    """
    # YOUR CODE HERE
    s = np.linalg.norm(W_hh,ord=2)
    current_grad = 1.0
    norms = []
    for t in range(T):
        norms.append(current_grad)
        current_grad *= s
    return norms
    
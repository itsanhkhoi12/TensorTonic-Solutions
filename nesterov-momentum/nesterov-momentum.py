import numpy as np

def nesterov_momentum_step(w, v, grad, lr, momentum):
    """
    Perform one Nesterov Momentum update step.
    """
    w = np.array(w, dtype=float)
    v = np.array(v, dtype=float)
    grad = np.array(grad, dtype=float)
    v_new = momentum * v + lr * grad
    w_new = w - v_new
    return np.round(w_new, 6).tolist(), np.round(v_new, 6).tolist()
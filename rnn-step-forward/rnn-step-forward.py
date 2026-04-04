import numpy as np

def rnn_step_forward(x_t, h_prev, Wx, Wh, b):
    """
    Returns: h_t of shape (H,)
    """
    # Write code here
    pre_act = np.array(x_t) @ np.array(Wx) +  np.array(h_prev) @ np.array(Wh) + np.array(b)
    return np.tanh(pre_act)

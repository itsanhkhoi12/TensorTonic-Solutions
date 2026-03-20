import numpy as np

def rmsprop_step(w, g, s, lr=0.001, beta=0.9, eps=1e-8):
    """
    Perform one RMSProp update step.
    """
    # Write code here
    new_s = beta*np.array(s) + (1-beta)*np.square(np.array(g))
    new_w = w -((lr/np.sqrt(np.array(new_s)+eps)) * np.array(g))
    return new_w, new_s
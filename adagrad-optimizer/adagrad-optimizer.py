import numpy as np

def adagrad_step(w, g, G, lr=0.01, eps=1e-8):
    """
    Perform one AdaGrad update step.
    """
    # Write code here
    w,g,G = np.array(w), np.array(g), np.array(G)
    new_G = G + np.square(g)
    new_w = w - (lr *g*(1/np.sqrt(new_G+eps)))
    return (new_w, new_G)
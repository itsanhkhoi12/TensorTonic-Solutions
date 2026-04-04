import math

def xavier_initialization(W, fan_in, fan_out):
    """
    Scale raw weights to Xavier uniform initialization.
    """
    # Write code here
    xavier_uniform = math.sqrt(6/(fan_in + fan_out))
    for i in range(len(W)):
        for j in range(len(W[i])):
            W[i][j] = (W[i][j]*2*xavier_uniform) - xavier_uniform

    return W
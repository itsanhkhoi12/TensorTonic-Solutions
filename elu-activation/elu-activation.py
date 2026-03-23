import math
def elu(x, alpha):
    """
    Apply ELU activation to each element.
    """
    # Write code here
    return [float(val) if val>0 else (alpha*(math.exp(float(val))-1)) for val in x]
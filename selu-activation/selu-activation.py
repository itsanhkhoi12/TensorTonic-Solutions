import numpy as np

def selu(x, lam=1.0507009873554804934193349852946, alpha=1.6732632423543772848170429916717):
    """
    Apply SELU activation element-wise.
    Returns a list of floats rounded to 4 decimal places.
    """
    # Write code here
    return [round(lam*val,4) if val>0 else np.round(lam*alpha*(np.exp(val)-1),4) for val in x]

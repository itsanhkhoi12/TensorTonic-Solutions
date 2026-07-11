import math

def cyclic_encoding(values, period):
    """
    Encode cyclic features as sin/cos pairs.
    """
    # Write code here

    cyclic_vals = []

    for val in values:
        rad = (2*math.pi*val)/ period
        cyclic_vals.append([math.sin(rad),math.cos(rad)])

    return cyclic_vals
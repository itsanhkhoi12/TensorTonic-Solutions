import math

def log_transform(values):
    """
    Apply the log1p transformation to each value.
    """
    return list(map(lambda x: math.log(1+x), values))
    # Write code here
def gradient_descent_quadratic(a, b, c, x0, lr, steps):
    """
    Return final x after 'steps' iterations.
    """
    # Write code 
    for step in range(steps):
        deriative_point = (2*a*x0)+b
        x0 = x0 - lr*deriative_point
    return x0
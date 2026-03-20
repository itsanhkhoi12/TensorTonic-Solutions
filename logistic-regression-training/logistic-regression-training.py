import numpy as np

def _sigmoid(z):
    """Numerically stable sigmoid implementation."""
    return np.where(z >= 0, 1/(1+np.exp(-z)), np.exp(z)/(1+np.exp(z)))

def train_logistic_regression(X, y, lr=0.1, steps=1000):
    """
    Train logistic regression via gradient descent.
    Return (w, b).
    """
    
    # Write code here
    m, n = X.shape
    w = np.zeros(n)
    b = 0
    for step in range(steps):
        model = np.dot(X,w)+b
        p = _sigmoid(model)
        loss_vector = np.array(p-y)
        weight_gradient = (1/m)*(np.dot(X.T,loss_vector))
        bias_gradient = (1/m)*(np.sum(loss_vector))
        w = w - lr*weight_gradient
        b = b - lr*bias_gradient
    return w,b
    
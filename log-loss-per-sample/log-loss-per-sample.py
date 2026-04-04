import math

def log_loss(y_true, y_pred, eps=1e-15):
    """
    Compute per-sample log loss.
    """
    # Write code here

    log_loss_values = []
    
    for idx in range(len(y_true)):
        y_clipped = max(eps, min(1-eps,y_pred[idx]))
        log_loss_value = -(y_true[idx]*math.log(y_clipped) +  (1-y_true[idx])*math.log(1-y_clipped))
        log_loss_values.append(log_loss_value)

    return log_loss_values
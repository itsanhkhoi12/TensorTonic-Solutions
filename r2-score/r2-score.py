import numpy as np

def r2_score(y_true, y_pred) -> float:
    """
    Compute R² (coefficient of determination) for 1D regression.
    Handle the constant-target edge case:
      - return 1.0 if predictions match exactly,
      - else 0.0.
    """
    # Write code here
    if len(set(y_true)) == 1: 
            if np.array_equal(np.array(y_true), np.array(y_pred)):
               return 1.0
            else:
                 return 0.0
    else:
        y_true = np.array(y_true)
        y_mean = np.mean(y_true)
        y_pred = np.array(y_pred)
        rss = np.sum(np.square(y_true-y_pred))
        tss = np.sum(np.square(y_true-y_mean))
        return 1- rss/tss
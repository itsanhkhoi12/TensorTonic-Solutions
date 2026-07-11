from collections import defaultdict
import numpy as np

def detect_skew(train_dist, serving_dist, threshold=0.2, eps=1e-10):
    """
    Detect train-serving skew using PSI.
    """
    # Write code here
    out = defaultdict(dict,{k:{} for k in train_dist.keys()})
    for feat in train_dist.keys():
        p_train = np.asarray(train_dist[feat])
        p_serving = np.asarray(serving_dist[feat])
        p_train+=eps
        p_serving+=eps
        psi = np.sum(
            (p_serving - p_train)
            * np.log(p_serving / p_train)
        )
        out[feat] = {
            "psi": float(psi),
            "skewed": bool(psi >= threshold),
        }        
    return dict(out)
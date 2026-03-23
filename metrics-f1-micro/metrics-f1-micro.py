def f1_micro(y_true, y_pred) -> float:
    """
    Compute micro-averaged F1 for multi-class integer labels.
    """
    # Write code here
    tp, fp, fn = (0,0,0)
    for i in range(len(y_true)):
        if y_true[i] == y_pred[i]:
            tp+=1
        if y_true[i] != y_pred[i]:
            fp +=1
    fn = len(y_true) - tp
    return (2*tp)/((2*tp)+fp+fn)
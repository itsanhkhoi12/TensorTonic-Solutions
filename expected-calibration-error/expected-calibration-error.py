def expected_calibration_error(y_true, y_pred, n_bins):
    """
    Compute Expected Calibration Error.
    """
    # Write code here
    n = len(y_true)

    bins = [[] for _ in range(n_bins)]

    for y,p in zip(y_true,y_pred):
        bin_idx = min(int(p * n_bins), n_bins - 1)
        bins[bin_idx].append((y, p))
    ece = 0.0
    for b in bins:
        if not b:
            continue
        acc = sum(y for y, p in b) / len(b)
        conf = sum(p for y, p in b) / len(b)
        ece += (len(b) / n) * abs(acc - conf)
    return ece
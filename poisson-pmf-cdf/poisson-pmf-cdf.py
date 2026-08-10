import numpy as np

def poisson_pmf_cdf(lam, k):
    """
    Compute Poisson PMF and CDF.
    """
    # Write code here
    log_pmf = -lam + k * np.log(lam) - np.sum(np.log(np.arange(1, k + 1)))
    pmf = np.exp(log_pmf)
    cdf = 0.0
    for i in range(k + 1):
        if i == 0:
            log_pmf_i = -lam
        else:
            log_pmf_i = -lam + i * np.log(lam) - np.sum(np.log(np.arange(1, i + 1)))
        cdf += np.exp(log_pmf_i)
    return float(pmf), float(cdf)
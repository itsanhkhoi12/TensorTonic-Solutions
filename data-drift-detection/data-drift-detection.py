def detect_drift(reference_counts, production_counts, threshold):
    """
    Compare reference and production distributions to detect data drift.
    """
    # Write code here
    prob_refs = [ref/sum(reference_counts) for ref in reference_counts]
    prob_prod = [prod/sum(production_counts) for prod in production_counts]
    tvd = 1/2*sum([abs(ref-prod) for ref, prod in zip(prob_refs,prob_prod)])
    return {'score': tvd,
           'drift_detected': tvd>threshold}
import numpy as np

def cohens_kappa(rater1, rater2):
    """
    Compute Cohen's Kappa coefficient.
    """
    # Write code here
    p_e = 0
    total_samples = len(rater1) 
    agreements = 0
    
    for i in range(len(rater1)):
        if rater1[i] == rater2[i]:
            agreements += 1

    if agreements == len(rater1):
        return 1.0
    else:
        p_o = agreements/total_samples
        for label in set(rater1):
            p_e += (rater1.count(label)/total_samples) * (rater2.count(label)/total_samples)
        if p_e == 1.0:
            return p_e
        else:
            return (p_o-p_e)/(1-p_e)
        
    
    
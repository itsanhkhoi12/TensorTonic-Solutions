import math

def perplexity(prob_distributions, actual_tokens):
    """
    Compute the perplexity of a token sequence given predicted distributions.
    """
    # Write code here
    actual_probs = []

    for i in range(len(prob_distributions)):
        actual_probs.append(math.log(prob_distributions[i][actual_tokens[i]]))

    return math.exp(-(1/len(prob_distributions))*sum(actual_probs))
        
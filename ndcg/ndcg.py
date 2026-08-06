import math

def ndcg(relevance_scores, k):
    """
    Compute NDCG@k.
    """
    # Write code here
    if all(score==0 for score in relevance_scores):
        return 0.0
    ndcg, dcg = 0, 0
    desc_scores = sorted(relevance_scores,reverse=True)
    
    if k > len(relevance_scores):
        k = len(relevance_scores)
        
    for i in range(1,k+1):
        dcg_gain = (2**relevance_scores[i-1]) - 1
        ndcg_gain = (2**desc_scores[i-1]) - 1
        dcg+= (dcg_gain/math.log2(i+1))
        ndcg+= (ndcg_gain/math.log2(i+1))

    return dcg/ndcg
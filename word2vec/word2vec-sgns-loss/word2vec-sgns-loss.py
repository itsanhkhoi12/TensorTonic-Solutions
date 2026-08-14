import torch
import torch.nn.functional as F

def sgns_loss(center_vec: torch.Tensor, pos_vec: torch.Tensor, neg_vecs: torch.Tensor) -> torch.Tensor:
    """
    Returns a scalar torch.Tensor: the SGNS loss.
    """
    # YOUR CODE HERE
    center_vec = torch.as_tensor(center_vec, dtype=torch.float64)
    pos_vec = torch.as_tensor(pos_vec, dtype=torch.float64)
    neg_vecs = torch.as_tensor(neg_vecs, dtype=torch.float64)
    pos_scores = torch.dot(center_vec,pos_vec)
    neg_scores = neg_vecs@center_vec
    pos_loss = F.softplus(-pos_scores)
    neg_loss = torch.sum(F.softplus(neg_scores))

    return pos_loss + neg_loss
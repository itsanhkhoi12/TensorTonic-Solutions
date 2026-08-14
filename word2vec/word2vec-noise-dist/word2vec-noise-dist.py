import torch

def noise_distribution(counts: torch.Tensor, alpha: float = 0.75) -> torch.Tensor:
    """
    Returns torch.Tensor of shape (vocab_size,), a probability distribution that sums to 1.
    """
    # YOUR CODE HERE
    counts = torch.as_tensor(counts, dtype = torch.float64)
    exp_counts  = torch.pow(counts,alpha)
    sum_exp_counts = torch.sum(exp_counts)
    
    return exp_counts/sum_exp_counts

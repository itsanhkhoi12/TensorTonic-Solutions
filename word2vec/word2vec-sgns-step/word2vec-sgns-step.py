import torch

def sgns_sgd_step(W_in: torch.Tensor, W_out: torch.Tensor, center_id: int, pos_id: int,
                  neg_ids: torch.Tensor, lr: float) -> tuple:
    """
    Returns tuple (W_in_updated, W_out_updated), each the same shape as the inputs, after one SGNS SGD step.
    """
    # YOUR CODE HERE
    W_in = W_in.clone()
    W_out = W_out.clone()
    neg_ids = torch.as_tensor(neg_ids, dtype=torch.int64)
    c = int(center_id)
    o = int(pos_id)

    v_c = W_in[c].clone()

    score_o = torch.sigmoid(torch.dot(v_c, W_out[o]))
    grad_vc = (score_o - 1.0) * W_out[o].clone()
    grad_out = {o: (score_o - 1.0) * v_c}

    for ni in neg_ids.tolist():
        s = torch.sigmoid(torch.dot(v_c, W_out[ni]))
        grad_vc = grad_vc + s * W_out[ni].clone()
        grad_out[ni] = grad_out.get(ni, torch.zeros_like(v_c)) + s * v_c

    for idx, g in grad_out.items():
        W_out[idx] = W_out[idx] - lr * g
    W_in[c] = W_in[c] - lr * grad_vc
    return W_in, W_out
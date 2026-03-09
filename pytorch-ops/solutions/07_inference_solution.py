"""Solution for Exercise 7: Inference & Generation"""

import math
import torch
import torch.nn.functional as F


def temperature_scaling(logits, temperature):
    scaled = logits / temperature
    probs = F.softmax(scaled, dim=-1)
    return {'scaled_logits': scaled, 'probs': probs}


def top_k_filtering(logits, k):
    top_k_vals, _ = torch.topk(logits, k, dim=-1)
    threshold = top_k_vals[..., -1:]
    filtered = logits.clone()
    filtered[logits < threshold] = float('-inf')
    return filtered


def top_p_filtering(logits, p):
    sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
    sorted_probs = F.softmax(sorted_logits, dim=-1)
    cumulative_probs = torch.cumsum(sorted_probs, dim=-1)

    # Mask where cumulative prob exceeds p (keep at least top-1)
    sorted_mask = cumulative_probs - sorted_probs >= p
    sorted_logits[sorted_mask] = float('-inf')

    # Unsort
    filtered = torch.zeros_like(logits)
    filtered.scatter_(-1, sorted_indices, sorted_logits)
    return filtered


def greedy_decode(logits_fn, start_token, max_len, eos_token=None):
    token_ids = [start_token]
    for _ in range(max_len - 1):
        logits = logits_fn(torch.tensor([token_ids]))
        next_token = logits[0, -1].argmax().item()
        token_ids.append(next_token)
        if eos_token is not None and next_token == eos_token:
            break
    return {'token_ids': token_ids, 'length': len(token_ids)}


def kv_cache_attention(Q, K_new, V_new, K_cache=None, V_cache=None):
    if K_cache is not None:
        K = torch.cat([K_cache, K_new], dim=-2)
        V = torch.cat([V_cache, V_new], dim=-2)
    else:
        K = K_new
        V = V_new

    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    weights = F.softmax(scores, dim=-1)
    output = weights @ V

    return {'output': output, 'K_cache': K, 'V_cache': V}


def sample_with_strategy(logits, strategy='greedy', temperature=1.0,
                         top_k=0, top_p=1.0):
    if strategy == 'greedy':
        return logits.argmax(dim=-1).item()

    # Apply temperature
    scaled = logits / temperature

    # Apply top-k
    if top_k > 0:
        scaled = top_k_filtering(scaled, top_k)

    # Apply top-p
    if top_p < 1.0:
        scaled = top_p_filtering(scaled, top_p)

    probs = F.softmax(scaled, dim=-1)
    return torch.multinomial(probs, 1).item()

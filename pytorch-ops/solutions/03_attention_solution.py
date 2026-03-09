"""Solution for Exercise 3: Attention from Scratch"""

import math
import torch
import torch.nn.functional as F


def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask, -1e9)
    weights = F.softmax(scores, dim=-1)
    output = weights @ V
    return {'output': output, 'weights': weights}


def create_causal_mask(seq_len):
    return torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()


def multi_head_split(x, n_heads):
    batch, seq, d_model = x.shape
    d_head = d_model // n_heads
    return x.reshape(batch, seq, n_heads, d_head).transpose(1, 2)


def multi_head_merge(x):
    batch, n_heads, seq, d_head = x.shape
    return x.transpose(1, 2).reshape(batch, seq, n_heads * d_head)


def multi_head_attention(Q, K, V, n_heads, mask=None):
    Q_split = multi_head_split(Q, n_heads)
    K_split = multi_head_split(K, n_heads)
    V_split = multi_head_split(V, n_heads)

    result = scaled_dot_product_attention(Q_split, K_split, V_split, mask)
    output = multi_head_merge(result['output'])
    return {'output': output, 'weights': result['weights']}


def attention_patterns(seq_len):
    # Causal: standard lower-triangular
    causal = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()

    # Sliding window: attend to self and 2 before
    sliding = torch.ones(seq_len, seq_len, dtype=torch.bool)
    for i in range(seq_len):
        for j in range(max(0, i - 2), i + 1):
            sliding[i, j] = False

    # Prefix: first seq_len//4 tokens attend to all, rest are causal
    prefix_len = seq_len // 4
    prefix = causal.clone()
    prefix[:prefix_len, :] = False

    return {'causal': causal, 'sliding_window': sliding, 'prefix': prefix}

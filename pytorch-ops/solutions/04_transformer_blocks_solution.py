"""Solution for Exercise 4: Transformer Building Blocks"""

import math
import torch
import torch.nn as nn


def token_embedding(vocab_size, d_model, token_ids):
    emb = nn.Embedding(vocab_size, d_model)
    embedded = emb(token_ids)
    return {'embedding_layer': emb, 'embedded': embedded}


def positional_encoding(seq_len, d_model):
    pe = torch.zeros(seq_len, d_model)
    position = torch.arange(0, seq_len, dtype=torch.float32).unsqueeze(1)
    div_term = torch.exp(
        torch.arange(0, d_model, 2, dtype=torch.float32)
        * (-math.log(10000.0) / d_model)
    )
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe


def layer_norm(x, eps=1e-5):
    mean = x.mean(dim=-1, keepdim=True)
    std = x.std(dim=-1, keepdim=True, unbiased=False)
    output = (x - mean) / (std + eps)
    return {'output': output, 'mean': mean.squeeze(-1), 'std': std.squeeze(-1)}


def feed_forward_network(d_model, d_ff):
    return nn.Sequential(
        nn.Linear(d_model, d_ff),
        nn.GELU(),
        nn.Linear(d_ff, d_model),
    )


def residual_connection(x, sublayer_output):
    return layer_norm(x + sublayer_output)['output']


def transformer_block_forward(x, self_attn_fn, ff_fn):
    attn_out = self_attn_fn(x)
    x = residual_connection(x, attn_out)
    ff_out = ff_fn(x)
    x = residual_connection(x, ff_out)
    return x

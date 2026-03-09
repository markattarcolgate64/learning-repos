"""Solution for Exercise 5: The Transformer"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class TransformerConfig:
    def __init__(self, vocab_size=1000, d_model=64, n_heads=4, d_ff=256,
                 n_layers=2, max_seq_len=128, dropout=0.1):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_ff = d_ff
        self.n_layers = n_layers
        self.max_seq_len = max_seq_len
        self.dropout = dropout


class TransformerBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attn = nn.MultiheadAttention(
            config.d_model, config.n_heads,
            dropout=config.dropout, batch_first=True,
        )
        self.ff = nn.Sequential(
            nn.Linear(config.d_model, config.d_ff),
            nn.GELU(),
            nn.Linear(config.d_ff, config.d_model),
        )
        self.norm1 = nn.LayerNorm(config.d_model)
        self.norm2 = nn.LayerNorm(config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x, mask=None):
        # Pre-norm style
        normed = self.norm1(x)
        attn_out, _ = self.attn(normed, normed, normed, attn_mask=mask)
        x = x + self.dropout(attn_out)

        normed = self.norm2(x)
        ff_out = self.ff(normed)
        x = x + self.dropout(ff_out)
        return x


class MiniTransformer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.token_emb = nn.Embedding(config.vocab_size, config.d_model)
        self.pos_emb = nn.Embedding(config.max_seq_len, config.d_model)
        self.dropout = nn.Dropout(config.dropout)
        self.blocks = nn.ModuleList(
            [TransformerBlock(config) for _ in range(config.n_layers)]
        )
        self.norm = nn.LayerNorm(config.d_model)
        self.output_proj = nn.Linear(config.d_model, config.vocab_size)

    def forward(self, token_ids, mask=None):
        batch, seq = token_ids.shape
        positions = torch.arange(seq, device=token_ids.device).unsqueeze(0)

        x = self.token_emb(token_ids) + self.pos_emb(positions)
        x = self.dropout(x)

        for block in self.blocks:
            x = block(x, mask=mask)

        x = self.norm(x)
        logits = self.output_proj(x)
        return logits


def compute_loss(logits, targets):
    batch, seq, vocab = logits.shape
    logits_flat = logits.reshape(batch * seq, vocab)
    targets_flat = targets.reshape(batch * seq)
    return nn.CrossEntropyLoss()(logits_flat, targets_flat)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

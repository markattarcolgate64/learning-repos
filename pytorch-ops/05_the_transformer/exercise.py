"""
The Transformer
Difficulty: 3/5

Put it ALL together into a working transformer model. You'll build a complete
mini-transformer from scratch that can process token sequences and produce
logits for next-token prediction.

All exercises use PyTorch. No external data files needed.
"""

import torch
import torch.nn as nn
import math


class TransformerConfig:
    """
    Configuration for the MiniTransformer.

    Default hyperparameters:
        vocab_size:   1000
        d_model:      64
        n_heads:      4
        d_ff:         256
        n_layers:     2
        max_seq_len:  128
        dropout:      0.1
    """
    # TODO: Store all config values as attributes.
    # Accept them as __init__ keyword arguments with the defaults above.
    pass


class TransformerBlock(nn.Module):
    """
    A single transformer block with pre-norm architecture.

    Components:
        - Multi-head self-attention (nn.MultiheadAttention)
        - Position-wise feed-forward network (Linear -> GELU -> Linear)
        - Two LayerNorms (one before attention, one before FFN)
        - Dropout after attention and FFN

    Forward pass (pre-norm style):
        x -> norm1 -> self_attn -> dropout -> + x (residual)
          -> norm2 -> ffn       -> dropout -> + x (residual)
    """

    def __init__(self, config):
        """
        Args:
            config: TransformerConfig instance
        """
        # TODO: Initialize:
        #   self.attn = nn.MultiheadAttention(d_model, n_heads, dropout, batch_first=True)
        #   self.ff = nn.Sequential(Linear(d_model, d_ff), GELU(), Linear(d_ff, d_model))
        #   self.norm1, self.norm2 = two nn.LayerNorm(d_model)
        #   self.dropout = nn.Dropout(dropout)
        pass

    def forward(self, x, mask=None):
        """
        Args:
            x: (batch, seq_len, d_model)
            mask: optional attention mask

        Returns:
            Output tensor of shape (batch, seq_len, d_model)
        """
        # TODO: Implement pre-norm transformer block.
        # 1. normed = self.norm1(x)
        # 2. attn_out, _ = self.attn(normed, normed, normed, attn_mask=mask)
        # 3. x = x + self.dropout(attn_out)
        # 4. normed = self.norm2(x)
        # 5. ff_out = self.ff(normed)
        # 6. x = x + self.dropout(ff_out)
        # 7. return x
        pass


class MiniTransformer(nn.Module):
    """
    A complete mini-transformer for language modeling.

    Components:
        - Token embedding (nn.Embedding)
        - Positional embedding (nn.Embedding)
        - Stack of TransformerBlocks
        - Final LayerNorm
        - Output projection to vocabulary logits
    """

    def __init__(self, config):
        """
        Args:
            config: TransformerConfig instance
        """
        # TODO: Initialize:
        #   self.token_emb = nn.Embedding(vocab_size, d_model)
        #   self.pos_emb = nn.Embedding(max_seq_len, d_model)
        #   self.blocks = nn.ModuleList([TransformerBlock(config) for _ in range(n_layers)])
        #   self.norm = nn.LayerNorm(d_model)
        #   self.proj = nn.Linear(d_model, vocab_size, bias=False)
        #   self.dropout = nn.Dropout(dropout)
        pass

    def forward(self, token_ids, mask=None):
        """
        Args:
            token_ids: (batch, seq_len) integer tensor
            mask: optional attention mask

        Returns:
            Logits of shape (batch, seq_len, vocab_size)
        """
        # TODO: Implement forward pass.
        # 1. token embeddings = self.token_emb(token_ids)
        # 2. positions = torch.arange(seq_len, device=token_ids.device)
        # 3. pos embeddings = self.pos_emb(positions)
        # 4. x = self.dropout(token_emb + pos_emb)
        # 5. for block in self.blocks: x = block(x, mask)
        # 6. x = self.norm(x)
        # 7. logits = self.proj(x)
        # 8. return logits
        pass


def compute_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """
    Compute cross-entropy loss for language modeling.

    Args:
        logits: (batch, seq_len, vocab_size) — model output
        targets: (batch, seq_len) — integer target token IDs

    Returns:
        Scalar loss tensor
    """
    # TODO: Reshape logits to (batch*seq_len, vocab_size) and targets to (batch*seq_len).
    # Use nn.CrossEntropyLoss() to compute and return the loss.
    pass


def count_parameters(model: nn.Module) -> int:
    """
    Count the total number of trainable parameters in a model.

    Args:
        model: Any nn.Module

    Returns:
        Integer count of trainable parameters
    """
    # TODO: Sum p.numel() for all parameters where p.requires_grad is True.
    pass

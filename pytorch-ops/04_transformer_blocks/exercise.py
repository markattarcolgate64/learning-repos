"""
Transformer Building Blocks
Difficulty: 2/5

The components that make up every transformer model. You'll implement each
building block individually, then combine them into a full transformer block.

All exercises use PyTorch. No external data files needed.
"""

import torch
import torch.nn as nn
import math


def token_embedding(vocab_size: int, d_model: int, token_ids: torch.Tensor) -> dict:
    """
    Create an embedding layer and look up token embeddings.

    Args:
        vocab_size: Size of the vocabulary
        d_model: Dimension of the embedding vectors
        token_ids: Integer tensor of shape (batch, seq_len) with token indices

    Returns:
        Dict with:
            'embedding_layer': the nn.Embedding module
            'embedded': output tensor of shape (batch, seq_len, d_model)
    """
    # TODO: Create nn.Embedding(vocab_size, d_model), look up token_ids,
    # return dict with 'embedding_layer' and 'embedded'.
    pass


def positional_encoding(seq_len: int, d_model: int) -> torch.Tensor:
    """
    Compute sinusoidal positional encoding.

    For each position pos and dimension i:
        PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
        PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

    Args:
        seq_len: Length of the sequence
        d_model: Dimension of the model

    Returns:
        Tensor of shape (seq_len, d_model) with positional encodings
    """
    # TODO: Implement sinusoidal positional encoding.
    # Even dimensions get sin, odd dimensions get cos.
    # Frequencies: pos / 10000^(2i/d_model)
    pass


def layer_norm(x: torch.Tensor, eps: float = 1e-5) -> dict:
    """
    Implement layer normalization manually (do NOT use nn.LayerNorm).

    Normalize over the last dimension so that each position has mean ~0 and var ~1.

    Args:
        x: Input tensor of any shape (..., features)
        eps: Small constant for numerical stability

    Returns:
        Dict with:
            'output': normalized tensor (same shape as x)
            'mean': per-position means (shape ..., 1)
            'std': per-position stds (shape ..., 1)
    """
    # TODO: Compute mean and variance over the last dimension.
    # Normalize: (x - mean) / (std + eps)
    # Return dict with 'output', 'mean', 'std'.
    pass


def feed_forward_network(d_model: int, d_ff: int) -> nn.Sequential:
    """
    Build the position-wise feed-forward network used in transformers.

    Architecture: Linear(d_model, d_ff) -> GELU -> Linear(d_ff, d_model)

    Args:
        d_model: Input and output dimension
        d_ff: Hidden dimension (typically 4 * d_model)

    Returns:
        nn.Sequential module implementing the FFN
    """
    # TODO: Return nn.Sequential(Linear, GELU, Linear)
    pass


def residual_connection(x: torch.Tensor, sublayer_output: torch.Tensor) -> torch.Tensor:
    """
    Implement Add & Norm: layer_norm(x + sublayer_output).

    Args:
        x: Original input tensor
        sublayer_output: Output from a sublayer (attention or FFN)

    Returns:
        Normalized residual output (same shape as x)
    """
    # TODO: Add x + sublayer_output, then apply your layer_norm function.
    # Return just the 'output' key from layer_norm.
    pass


def transformer_block_forward(
    x: torch.Tensor,
    self_attn_fn: callable,
    ff_fn: callable,
) -> torch.Tensor:
    """
    Execute a full transformer block: self-attention with residual, then FFN with residual.

    Args:
        x: Input tensor of shape (batch, seq_len, d_model)
        self_attn_fn: Callable that takes x and returns attention output (same shape)
        ff_fn: Callable that takes x and returns FFN output (same shape)

    Returns:
        Output tensor of shape (batch, seq_len, d_model)
    """
    # TODO: Apply self_attn_fn with residual connection, then ff_fn with residual connection.
    # Use your residual_connection function for both.
    pass

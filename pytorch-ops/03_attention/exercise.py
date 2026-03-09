"""
Attention from Scratch
Difficulty: 3/5

THE core operation of transformers. If you understand attention, you understand
the heart of GPT, BERT, and every LLM. This exercise builds it up piece by piece.
"""

import torch
import torch.nn.functional as F


def scaled_dot_product_attention(
    Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, mask: torch.Tensor = None
) -> dict:
    """
    Compute scaled dot-product attention.

    Args:
        Q: Query tensor of shape (batch, seq_q, d_k)
        K: Key tensor of shape (batch, seq_k, d_k)
        V: Value tensor of shape (batch, seq_k, d_v)
        mask: Optional boolean mask of shape broadcastable to (batch, seq_q, seq_k).
              True means "mask this position" (set to -1e9 before softmax).

    Returns dict with:
        'output': attention output of shape (batch, seq_q, d_v)
        'weights': attention weights of shape (batch, seq_q, seq_k), rows sum to 1

    The formula: Attention(Q, K, V) = softmax(Q @ K^T / sqrt(d_k)) @ V
    This is equation (1) from "Attention Is All You Need".
    """
    # TODO: implement
    return None


def create_causal_mask(seq_len: int) -> torch.Tensor:
    """
    Create a causal (autoregressive) mask for self-attention.

    Returns a boolean tensor of shape (seq_len, seq_len) where True means
    "mask this position" (i.e., future tokens).

    Position (i, j) is True when j > i (token i should not attend to token j).
    This is the upper triangle (excluding diagonal).

    Example for seq_len=4:
        [[False,  True,  True,  True],
         [False, False,  True,  True],
         [False, False, False,  True],
         [False, False, False, False]]
    """
    # TODO: implement
    return None


def multi_head_split(x: torch.Tensor, n_heads: int) -> torch.Tensor:
    """
    Split the last dimension of x into multiple attention heads.

    Given x of shape (batch, seq, d_model), reshape and transpose to
    (batch, n_heads, seq, d_head) where d_head = d_model // n_heads.

    Steps:
        1. Reshape: (batch, seq, d_model) -> (batch, seq, n_heads, d_head)
        2. Transpose: (batch, seq, n_heads, d_head) -> (batch, n_heads, seq, d_head)

    This is how transformers process multiple attention patterns in parallel.
    """
    # TODO: implement
    return None


def multi_head_merge(x: torch.Tensor) -> torch.Tensor:
    """
    Reverse of multi_head_split. Merge attention heads back together.

    Given x of shape (batch, n_heads, seq, d_head), transpose and reshape to
    (batch, seq, d_model) where d_model = n_heads * d_head.

    Steps:
        1. Transpose: (batch, n_heads, seq, d_head) -> (batch, seq, n_heads, d_head)
        2. Reshape: (batch, seq, n_heads, d_head) -> (batch, seq, d_model)

    Use .contiguous() before reshape if needed (transpose makes tensors non-contiguous).
    """
    # TODO: implement
    return None


def multi_head_attention(
    Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, n_heads: int, mask: torch.Tensor = None
) -> dict:
    """
    Full multi-head attention.

    Args:
        Q, K, V: shape (batch, seq, d_model)
        n_heads: number of attention heads
        mask: optional boolean mask, shape broadcastable to (batch, n_heads, seq_q, seq_k)

    Steps:
        1. Split Q, K, V into heads using multi_head_split
        2. Apply scaled_dot_product_attention (it handles the batch*heads dimension)
        3. Merge heads back using multi_head_merge

    Returns dict with:
        'output': shape (batch, seq, d_model)
        'weights': shape (batch, n_heads, seq_q, seq_k)
    """
    # TODO: implement
    return None


def attention_patterns(seq_len: int) -> dict:
    """
    Create three different attention mask patterns used in practice.
    All masks are boolean tensors of shape (seq_len, seq_len) where True = masked.

    Return dict with:
        'causal': Standard causal mask — each token attends to itself and all
                  previous tokens. Future tokens are masked.

        'sliding_window': Each token attends to itself and up to 2 tokens before it.
                         Everything else is masked. This limits the attention window,
                         used in models like Mistral for efficiency.
                         Position (i, j) is masked if j > i (future) OR j < i - 2
                         (too far in the past).

        'prefix': The first seq_len // 4 tokens can attend to all positions (like
                  an encoder). The remaining tokens use causal masking.
                  This is prefix-LM attention, used in T5 and PaLM.
    """
    # TODO: implement
    return None

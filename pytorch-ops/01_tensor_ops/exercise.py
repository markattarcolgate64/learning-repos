"""
Tensor Operations Bootcamp
Difficulty: 1/5

The operations you'll use every day reading transformer code.
Master these and the rest of PyTorch becomes much easier to follow.
"""

import torch


def reshape_and_view(x: torch.Tensor) -> dict:
    """
    Given x of shape (12,), return it reshaped two ways:
      - 'view_34': shape (3, 4) using .view()
      - 'reshape_26': shape (2, 6) using .reshape()

    view() requires contiguous memory; reshape() is more flexible.
    In transformer code, you'll see both used to split/merge attention heads.
    """
    # TODO: implement
    return None


def transpose_and_permute(x: torch.Tensor) -> dict:
    """
    Given x of shape (2, 3, 4), return:
      - 'transposed': swap dims 1 and 2 -> shape (2, 4, 3) using .transpose()
      - 'permuted': reorder to (4, 2, 3) using .permute(2, 0, 1)

    Transpose swaps exactly two dimensions. Permute reorders all dimensions.
    In attention, we permute between (batch, seq, heads, d) and (batch, heads, seq, d).
    """
    # TODO: implement
    return None


def broadcasting_add(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Given a of shape (3, 1) and b of shape (1, 4), return their sum of shape (3, 4).

    Broadcasting is how biases work in neural networks: a bias of shape (d,)
    gets added to every element in a batch of shape (batch, seq, d).
    """
    # TODO: implement
    return None


def batched_matmul(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    """
    Given a of shape (batch, n, m) and b of shape (batch, m, p),
    compute batched matrix multiplication. Return shape (batch, n, p).

    Use torch.bmm or the @ operator. This is how Q @ K^T works in attention.
    """
    # TODO: implement
    return None


def indexing_and_masking(x: torch.Tensor, threshold: float) -> dict:
    """
    Given x (any shape) and a threshold value, return:
      - 'mask': boolean tensor where x > threshold
      - 'selected': values where mask is True (flattened to 1D)
      - 'count': number of elements above threshold (as Python int)

    Masking is used everywhere in transformers: padding masks, causal masks,
    attention masks. Understanding boolean indexing is essential.
    """
    # TODO: implement
    return None


def einsum_operations(a: torch.Tensor, b: torch.Tensor) -> dict:
    """
    Given a of shape (batch, seq, d) and b of shape (d, d):
      - 'linear': batch matrix multiply a @ b using einsum 'bsd,dd->bsd'
      - 'similarity': compute pairwise similarity a @ a^T using einsum 'bsd,btd->bst'
        (this is the attention score pattern)

    Einstein summation is the swiss army knife of tensor operations.
    Once you learn it, you can express any linear algebra operation in one line.
    """
    # TODO: implement
    return None

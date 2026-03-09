"""Solution for Exercise 1: Tensor Operations Bootcamp"""

import torch


def reshape_and_view(x):
    return {
        'view_34': x.view(3, 4),
        'reshape_26': x.reshape(2, 6),
    }


def transpose_and_permute(x):
    return {
        'transposed': x.transpose(1, 2),
        'permuted': x.permute(2, 0, 1),
    }


def broadcasting_add(a, b):
    return a + b


def batched_matmul(a, b):
    return a @ b


def indexing_and_masking(x, threshold):
    mask = x > threshold
    return {
        'mask': mask,
        'selected': x[mask],
        'count': int(mask.sum().item()),
    }


def einsum_operations(a, b):
    return {
        'linear': torch.einsum('bsd,dd->bsd', a, b),
        'similarity': torch.einsum('bsd,btd->bst', a, a),
    }

"""
Data loading and preprocessing for CIFAR-10.

Downloads CIFAR-10 and creates train/val splits with transforms.

NOTE: There are bugs in this file. The model architecture is fine —
      the problems are in how data is prepared.
"""

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader, Subset
import torchvision
import torchvision.transforms as T


class NormalizedDataset(Dataset):
    """Wraps a dataset with pre-computed normalization stats."""

    def __init__(self, subset, mean, std, augment=False):
        self.subset = subset
        self.mean = mean
        self.std = std
        self.augment = augment

    def __len__(self):
        return len(self.subset)

    def __getitem__(self, idx):
        img, label = self.subset[idx]
        # Convert PIL to tensor
        img = T.functional.to_tensor(img)
        # Normalize with pre-computed stats
        img = T.functional.normalize(img, self.mean, self.std)
        if self.augment:
            img = T.functional.hflip(img) if torch.rand(1).item() > 0.5 else img
        return img, label


def create_data_loaders(
    batch_size: int = 128,
    val_fraction: float = 0.1,
    seed: int = 42,
) -> tuple[DataLoader, DataLoader]:
    """Create train and validation data loaders.

    Downloads CIFAR-10 and splits the training set into train/val.

    Args:
        batch_size: Batch size for both loaders.
        val_fraction: Fraction of training data to use for validation.
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (train_loader, val_loader).
    """
    # Download raw CIFAR-10 (no transforms yet — we'll apply them later)
    full_dataset = torchvision.datasets.CIFAR10(
        root="./cifar10_data",
        train=True,
        download=True,
        transform=None,  # Raw PIL images
    )

    n_total = len(full_dataset)
    n_val = int(n_total * val_fraction)
    n_train = n_total - n_val

    # --- BUG 1: Compute normalization on the FULL dataset before splitting ---
    # This leaks validation statistics into training normalization.
    # Should only compute mean/std on the training split.
    all_images = np.stack([np.array(full_dataset[i][0]) for i in range(n_total)]) / 255.0
    mean = all_images.mean(axis=(0, 2, 3)).tolist() if all_images.ndim == 4 else [0.5, 0.5, 0.5]
    # Fix: compute per-channel mean correctly for (N, H, W, C) layout
    mean = [all_images[:, :, :, c].mean() for c in range(3)]
    std = [all_images[:, :, :, c].std() for c in range(3)]

    # Split indices
    rng = np.random.RandomState(seed)
    indices = rng.permutation(n_total)

    # --- BUG 2: Overlapping indices — val indices are a SUBSET of train indices ---
    # train gets the first n_train, val gets the last n_val.
    # But n_train + n_val == n_total only if there's no overlap... and there isn't
    # in the indices, BUT we're going to shuffle labels below which breaks things.
    train_indices = indices[:n_train].tolist()
    val_indices = indices[n_train:].tolist()

    train_subset = Subset(full_dataset, train_indices)
    val_subset = Subset(full_dataset, val_indices)

    # --- BUG 3: Shuffle labels independently of images ---
    # This creates a random label mapping that destroys the signal.
    # The comment says "shuffle for better training" but it shuffles LABELS not order.
    all_labels = [full_dataset.targets[i] for i in range(n_total)]
    rng2 = np.random.RandomState(seed + 1)
    rng2.shuffle(all_labels)
    # Overwrite the dataset's targets with shuffled labels
    full_dataset.targets = all_labels

    train_data = NormalizedDataset(train_subset, mean, std, augment=True)
    val_data = NormalizedDataset(val_subset, mean, std, augment=False)

    train_loader = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_data,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=True,
    )

    print(f"Dataset: CIFAR-10")
    print(f"  Training samples:   {len(train_data)}")
    print(f"  Validation samples: {len(val_data)}")
    print(f"  Normalization mean: {[f'{m:.4f}' for m in mean]}")
    print(f"  Normalization std:  {[f'{s:.4f}' for s in std]}")

    return train_loader, val_loader

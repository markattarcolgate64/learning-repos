"""
Training script for CIFAR-10 image classifier.

Expected result: ~92% validation accuracy after 30 epochs.
Current result:  ~51% (barely above random for 10 classes).

The model architecture (model.py) is correct. The bugs are in
data preparation and this training loop.

Usage:
    python train.py
"""

import time
import torch
import torch.nn as nn
import torch.optim as optim

from model import SimpleCNN
from data import create_data_loaders


def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)

        # --- BUG 4: softmax on wrong axis before cross-entropy ---
        # CrossEntropyLoss already applies log_softmax internally.
        # Applying softmax first with dim=0 (batch dimension) is wrong:
        #   - dim=0 normalizes across the BATCH for each class
        #   - Should be dim=1 if you were to apply it (but you shouldn't)
        # This double-softmax with wrong axis severely hurts training.
        outputs = torch.softmax(outputs, dim=0)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)

    avg_loss = total_loss / total
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        # Same bug here — softmax on dim=0 before cross-entropy
        outputs = torch.softmax(outputs, dim=0)
        loss = criterion(outputs, labels)

        total_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total += labels.size(0)

    avg_loss = total_loss / total
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


def main():
    # Hyperparameters (these are fine — don't change them)
    epochs = 30
    batch_size = 128
    learning_rate = 0.001
    weight_decay = 1e-4

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    train_loader, val_loader = create_data_loaders(batch_size=batch_size)

    model = SimpleCNN(num_classes=10).to(device)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss()

    print(f"\nTraining for {epochs} epochs...")
    print(f"{'Epoch':>5} | {'Train Loss':>10} | {'Train Acc':>9} | {'Val Loss':>8} | {'Val Acc':>7} | {'Time':>6}")
    print("-" * 65)

    for epoch in range(1, epochs + 1):
        start = time.time()

        train_loss, train_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        scheduler.step()

        elapsed = time.time() - start
        print(f"{epoch:5d} | {train_loss:10.4f} | {train_acc:8.2f}% | {val_loss:8.4f} | {val_acc:6.2f}% | {elapsed:5.1f}s")

    print(f"\nFinal validation accuracy: {val_acc:.2f}%")
    if val_acc < 85:
        print("WARNING: Accuracy is well below expected ~92%. Something is wrong.")


if __name__ == "__main__":
    main()

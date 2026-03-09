"""Solution for Exercise 6: Training at Scale"""

import math
import torch
import torch.nn as nn
import torch.optim as optim


def gradient_clipping_demo(model, X, y, max_norm=1.0):
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    optimizer.zero_grad()
    preds = model(X)
    loss = criterion(preds, y)
    loss.backward()

    # Compute norm before clipping
    grad_norm_before = torch.nn.utils.clip_grad_norm_(
        model.parameters(), max_norm=float('inf'))

    # Actually clip
    # Need to re-backward since clip_grad_norm_ modifies grads in-place only
    # when max_norm < current norm. But we already called it with inf.
    # Let's redo properly:
    optimizer.zero_grad()
    preds = model(X)
    loss = criterion(preds, y)
    loss.backward()

    total_norm = 0.0
    for p in model.parameters():
        if p.grad is not None:
            total_norm += p.grad.data.norm(2).item() ** 2
    grad_norm_before = total_norm ** 0.5

    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_norm)

    total_norm_after = 0.0
    for p in model.parameters():
        if p.grad is not None:
            total_norm_after += p.grad.data.norm(2).item() ** 2
    grad_norm_after = total_norm_after ** 0.5

    optimizer.step()

    return {
        'grad_norm_before': grad_norm_before,
        'grad_norm_after': grad_norm_after,
        'loss': loss.item(),
    }


def learning_rate_schedules(total_steps=1000, warmup_steps=100):
    peak_lr = 0.001
    cosine_lrs = []
    linear_lrs = []

    for step in range(total_steps):
        if step < warmup_steps:
            lr = peak_lr * step / warmup_steps
        else:
            progress = (step - warmup_steps) / (total_steps - warmup_steps)
            lr_cos = peak_lr * 0.5 * (1 + math.cos(math.pi * progress))
            lr_lin = peak_lr * (1 - progress)
            cosine_lrs.append(lr_cos)
            linear_lrs.append(lr_lin)
            continue
        cosine_lrs.append(lr)
        linear_lrs.append(lr)

    return {'cosine': cosine_lrs, 'linear': linear_lrs}


def gradient_accumulation_training(model, batches, accumulation_steps=4,
                                   lr=0.01):
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=lr)

    losses = []
    accumulated_loss = 0.0

    optimizer.zero_grad()
    for i, (X, y) in enumerate(batches):
        preds = model(X)
        loss = criterion(preds, y) / accumulation_steps
        loss.backward()
        accumulated_loss += loss.item() * accumulation_steps

        if (i + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
            losses.append(accumulated_loss)
            accumulated_loss = 0.0

    return {
        'losses': losses,
        'n_optimizer_steps': len(losses),
    }


def mixed_precision_concepts():
    return {
        'float32_size': torch.tensor(1.0, dtype=torch.float32).element_size(),
        'float16_size': torch.tensor(1.0, dtype=torch.float16).element_size(),
        'bfloat16_size': torch.tensor(1.0, dtype=torch.bfloat16).element_size(),
        'float16_max': float(torch.finfo(torch.float16).max),
        'bfloat16_max': float(torch.finfo(torch.bfloat16).max),
    }


def weight_decay_comparison(X, y, steps=200):
    torch.manual_seed(42)
    model_no_decay = nn.Linear(4, 1)
    torch.manual_seed(42)
    model_with_decay = nn.Linear(4, 1)

    opt_no = optim.Adam(model_no_decay.parameters(), lr=0.01)
    opt_wd = optim.AdamW(model_with_decay.parameters(), lr=0.01,
                         weight_decay=0.1)
    criterion = nn.MSELoss()

    for _ in range(steps):
        opt_no.zero_grad()
        loss = criterion(model_no_decay(X), y)
        loss.backward()
        opt_no.step()

        opt_wd.zero_grad()
        loss = criterion(model_with_decay(X), y)
        loss.backward()
        opt_wd.step()

    return {
        'no_decay_weights': model_no_decay.weight.detach(),
        'with_decay_weights': model_with_decay.weight.detach(),
        'no_decay_norm': model_no_decay.weight.detach().norm().item(),
        'with_decay_norm': model_with_decay.weight.detach().norm().item(),
    }


def cosine_annealing_with_restarts(total_steps=400, T_0=100):
    peak_lr = 0.001
    lrs = []
    for step in range(total_steps):
        lr = peak_lr * 0.5 * (1 + math.cos(math.pi * (step % T_0) / T_0))
        lrs.append(lr)
    return lrs

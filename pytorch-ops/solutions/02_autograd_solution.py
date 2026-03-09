"""Solution for Exercise 2: Autograd & Computation Graphs"""

import torch
import torch.nn as nn
import torch.optim as optim


def manual_gradient_check(x_val):
    x = torch.tensor(float(x_val), requires_grad=True)
    y = x**3 - 2*x**2 + x
    y.backward()
    analytical = 3*x_val**2 - 4*x_val + 1
    return {
        'y': y.item(),
        'grad': x.grad.item(),
        'analytical': float(analytical),
    }


def gradient_accumulation(model, X_batches, y_batches):
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    optimizer.zero_grad()
    total_loss = 0.0
    for X, y in zip(X_batches, y_batches):
        preds = model(X)
        loss = criterion(preds, y)
        loss.backward()
        total_loss += loss.item()

    grad_norm = model.weight.grad.norm().item()
    optimizer.step()

    return {'loss': total_loss, 'grad_norm': grad_norm}


def detach_and_no_grad(x):
    detached = x.detach()
    with torch.no_grad():
        no_grad_result = x * 2
    return {
        'detached': detached,
        'no_grad_result': no_grad_result,
        'requires_grad_detached': detached.requires_grad,
        'requires_grad_no_grad': no_grad_result.requires_grad,
    }


def custom_function(x):
    output = torch.clamp(x, min=0)
    output.sum().backward()
    return {'output': output, 'grad': x.grad}


def higher_order_gradients(x_val):
    x = torch.tensor(float(x_val), requires_grad=True)
    y = x**4
    first = torch.autograd.grad(y, x, create_graph=True)[0]
    second = torch.autograd.grad(first, x)[0]
    return {
        'first': first.item(),
        'second': second.item(),
    }

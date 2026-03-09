# PyTorch Ops: The Operations Behind Transformers & LLMs

Learn PyTorch by implementing the exact operations used in modern transformers,
LLMs, and reasoning models. No toy datasets — pure tensor operations.

## Prerequisites

```bash
pip install torch numpy
```

## Exercises

| # | Exercise | Difficulty | What You'll Learn |
|---|----------|------------|-------------------|
| 01 | Tensor Operations Bootcamp | \* | reshape, view, transpose, permute, broadcasting, einsum, masking |
| 02 | Autograd & Computation Graphs | \*\* | gradients, accumulation, detach, no_grad, higher-order derivatives |
| 03 | Attention from Scratch | \*\*\* | scaled dot-product attention, causal masks, multi-head attention |
| 04 | Transformer Building Blocks | \*\* | embeddings, positional encoding, layer norm, FFN, residual connections |
| 05 | The Transformer | \*\*\* | TransformerBlock, full MiniTransformer, forward pass, loss |
| 06 | Training at Scale | \*\*\* | gradient clipping, LR schedules, grad accumulation, mixed precision, weight decay |
| 07 | Inference & Generation | \*\*\* | temperature, top-k, top-p, greedy decode, KV caching |

## How to Use

```bash
cd pytorch-ops

# Work on an exercise
# 1. Read exercise.py — comments explain WHY, not just how
# 2. Fill in the TODO stubs
# 3. Run tests to verify
python -m pytest 01_tensor_ops/test_exercise.py -v

# Or with unittest
python -m unittest 01_tensor_ops.test_exercise -v
```

## Why This Order

The exercises follow the data flow of a transformer:

```
Tokens → Embeddings + Position → [Attention → FFN] × N → Logits → Sampling
  (04)      (04)        (04)       (03)    (04)  (05)    (05)      (07)
```

Exercises 01-02 give you the foundation (tensor ops, autograd).
Exercise 06 covers the training loop.
Exercise 07 covers inference — how LLMs actually generate text.

## Structure

```
pytorch-ops/
├── README.md
├── 01_tensor_ops/          # reshape, broadcast, einsum
├── 02_autograd/            # gradients, computation graphs
├── 03_attention/           # scaled dot-product, multi-head
├── 04_transformer_blocks/  # embeddings, layernorm, FFN
├── 05_the_transformer/     # full transformer model
├── 06_training/            # clipping, scheduling, accumulation
├── 07_inference/           # sampling, KV cache, generation
└── solutions/              # reference implementations
```

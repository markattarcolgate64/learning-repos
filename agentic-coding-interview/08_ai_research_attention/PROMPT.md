# Multi-Head Self-Attention from Scratch

**Category:** AI Research Engineering
**Difficulty:** ★★★★★
**Time:** ~75 min

---

## The Prompt

Read the "Attention Is All You Need" paper and implement multi-head self-attention from scratch in NumPy — no PyTorch, no TensorFlow. Validate your implementation against PyTorch's `nn.MultiheadAttention` for correctness. Benchmark both for speed on varying sequence lengths.

---

<details>
<summary>Evaluation Criteria (open after attempting)</summary>

### What They're Really Testing

- Ability to read and comprehend a research paper, then translate math notation to working code
- Numerical programming discipline (floating point tolerance, proper matrix operations)
- Benchmarking methodology

### Strong Signals

- Correct scaled dot-product attention (`Q K^T / sqrt(d_k)`)
- Proper multi-head splitting and concatenation
- Projection matrices (`W_Q`, `W_K`, `W_V`, `W_O`) implemented correctly
- Attention mask support
- Numerically matches PyTorch output within float32 tolerance (~1e-6)
- Benchmark shows expected O(n^2) scaling with sequence length
- Clean, readable code with comments mapping to paper equations

### Red Flags

- Wrong or missing scaling factor
- No attention mask support
- Doesn't validate against a reference implementation
- Copy-pastes without understanding the math
- No benchmarking
- Ignores numerical precision issues

### Suggested Tools

- **Web search** to find the paper and blog explanations
- **NumPy** for implementation
- **PyTorch** for reference validation
- **matplotlib** for benchmark plots
- **time/timeit** for benchmarking

</details>

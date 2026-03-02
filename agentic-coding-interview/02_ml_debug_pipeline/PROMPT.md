# Fix a Broken Training Pipeline

## The Prompt

> This image classifier should reach ~92% validation accuracy but it's stuck
> at 51% — barely above random. The model architecture and hyperparameters are
> fine. Something else is wrong. Find and fix the bugs.

**Time budget:** ~50 minutes
**Difficulty:** ★★★★

Starter code is in `pipeline/`. Run with:

```bash
cd pipeline && pip install -r requirements.txt
python train.py
```

---

<details>
<summary>Evaluation Criteria (open after attempting)</summary>

### What they're really testing

- **ML debugging intuition** — do you look at the data before tweaking the model?
- **Systematic investigation** — hypothesis → experiment → conclusion, not random changes
- **Knowledge of common ML pitfalls** — data leakage, preprocessing errors, label corruption
- **Tool usage** — do you add logging, visualize distributions, inspect batches?

### Strong signals

- Inspects the data first (visualize samples, check label distributions, verify shapes)
- Checks for data leakage between train and validation sets
- Adds validation loss/accuracy logging to spot issues during training
- Identifies bugs one at a time and re-trains to confirm each fix helps
- Finds all 4 bugs: data leakage, label shuffle, normalization leak, wrong softmax axis
- Final accuracy reaches the expected ~92%

### Red flags

- Immediately tweaks hyperparameters (learning rate, batch size) without investigating
- Changes the model architecture ("maybe we need more layers")
- Doesn't look at the actual data or label distributions
- Makes all changes at once so can't tell which one helped
- Gives up and says "the dataset is too hard"

### Suggested tools & approaches

- `matplotlib` to visualize training samples and label distributions
- Add print/logging statements to inspect batch shapes and loss values
- Web search for "common PyTorch training bugs" or specific error patterns
- Run training for just 1-2 epochs to iterate quickly
- Check train vs val accuracy curves for signs of data leakage

### The 4 bugs (spoilers)

1. **Data leakage** — validation images appear in the training set (indices overlap)
2. **Label shuffle** — labels are shuffled independently of images after the split
3. **Normalization leak** — mean/std computed on the full dataset before splitting
4. **Wrong softmax axis** — softmax applied on dim=0 (batch) instead of dim=1 (classes)

</details>

# ML Learning: End-to-End Model Training

You know the math behind ML. Now learn the **workflow**.

These exercises teach you the full pipeline of training a machine learning model:
load data, preprocess, train, evaluate, iterate. Each exercise builds on the last,
starting from the simplest possible case and ending with a neural network from scratch.

## Prerequisites

- Python 3.8+
- numpy, pandas, scikit-learn

```bash
pip install numpy pandas scikit-learn
```

## Running Tests

```bash
# Run tests for a specific exercise
cd ml-learning
python -m unittest 01_first_pipeline.test_exercise -v

# Run all tests
python -m unittest discover -s . -p "test_exercise.py" -v
```

## Exercises

| # | Exercise | Difficulty | What You'll Learn |
|---|----------|------------|-------------------|
| 01 | Your First ML Pipeline | \* | Load data, train/test split, fit/predict, accuracy |
| 02 | Data Preprocessing | \*\* | Missing values, encoding, scaling, data leakage |
| 03 | Model Evaluation & Comparison | \*\* | Confusion matrix, precision/recall, cross-validation, model selection |
| 04 | The Full Pipeline | \*\*\* | End-to-end workflow, sklearn Pipeline, EDA, iteration |
| 05 | Neural Network from Scratch | \*\*\* | Forward prop, backprop, training loop, numpy only |
| 06 | Computer Vision | \*\* | Images as arrays, pixel normalization, digit classification, misclassification analysis |

## How to Use

1. Open `exercise.py` in the exercise directory
2. Read the comments — they explain WHY each step matters, not just how
3. Fill in the TODO stubs (replace `None` or `pass` with your code)
4. Run the file directly (`python exercise.py`) to see your output
5. Run the tests to verify: `python -m unittest XX_name.test_exercise -v`
6. Check `solutions/` only after completing or when truly stuck

## Difficulty Ratings

- \* Easy — the basics, ~20 minutes
- \*\* Medium — core skills, ~30-45 minutes
- \*\*\* Hard — putting it all together, ~45-60 minutes

## Structure

```
ml-learning/
├── README.md
├── datasets/
│   ├── generate_data.py          # Regenerate CSVs if needed
│   ├── student_performance.csv   # Classification (exercises 1 & 3)
│   ├── housing_prices.csv        # Regression with messy data (exercise 2)
│   └── bike_rentals.csv          # Mixed features (exercise 4)
├── 01_first_pipeline/
│   ├── exercise.py               # Your implementation goes here
│   └── test_exercise.py          # Tests to verify correctness
├── ...
└── solutions/                    # Reference implementations (no peeking!)
```

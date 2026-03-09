"""
Solution for Exercise 4: The Full ML Pipeline
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "bike_rentals.csv")


def load_data():
    return pd.read_csv(DATA_PATH)


def eda(df):
    return {
        'n_rows': df.shape[0],
        'n_cols': df.shape[1],
        'missing_cols': list(df.columns[df.isnull().any()]),
        'categorical_cols': list(df.select_dtypes(include='object').columns),
        'target_mean': df['rentals'].mean(),
    }


def preprocess(df):
    df = df.copy()

    # Fill missing values in numeric columns with median
    for col in df.select_dtypes(include=np.number).columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # One-hot encode categorical columns
    cat_cols = list(df.select_dtypes(include='object').columns)
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    y = df['rentals']
    X = df.drop(columns=['rentals'])

    return X, y


def build_pipeline(model):
    return Pipeline([
        ('scaler', StandardScaler()),
        ('model', model),
    ])


def evaluate_pipeline(pipeline, X, y, cv=5):
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring='r2')
    return {
        'cv_scores': scores,
        'mean_score': np.mean(scores),
        'std_score': np.std(scores),
    }


def run_experiment(X, y):
    results = []

    configs = [
        ('Linear Regression', LinearRegression()),
        ('Ridge Regression', Ridge(alpha=1.0)),
        ('Decision Tree', DecisionTreeRegressor(random_state=42)),
        ('Random Forest', RandomForestRegressor(n_estimators=50, random_state=42)),
    ]

    for name, model in configs:
        pipe = build_pipeline(model)
        eval_result = evaluate_pipeline(pipe, X, y)
        results.append({
            'name': name,
            'mean_score': eval_result['mean_score'],
            'std_score': eval_result['std_score'],
        })

    return results


def summarize_findings(results):
    if not results:
        return "No experiments were run."

    best = max(results, key=lambda r: r['mean_score'])
    worst = min(results, key=lambda r: r['mean_score'])

    return (
        f"Tested {len(results)} models on the bike rental dataset. "
        f"The best model was {best['name']} with R2={best['mean_score']:.3f} "
        f"(+/- {best['std_score']:.3f}). "
        f"The worst was {worst['name']} with R2={worst['mean_score']:.3f}. "
        f"Tree-based models tend to perform well because they can capture "
        f"nonlinear relationships between weather features and rental counts."
    )

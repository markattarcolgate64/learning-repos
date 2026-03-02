"""
Solution for Exercise 2: Data Preprocessing and Feature Engineering
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "housing_prices.csv")


def load_data():
    return pd.read_csv(DATA_PATH)


def handle_missing_values(df):
    df = df.copy()
    for col in df.select_dtypes(include=np.number).columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    return df


def encode_categoricals(df):
    df = df.copy()
    cat_cols = list(df.select_dtypes(include='object').columns)
    if cat_cols:
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    return df


def engineer_features(df):
    df = df.copy()
    df['age'] = 2024 - df['year_built']
    df['sqft_per_bedroom'] = df['square_feet'] / df['num_bedrooms']
    return df


def scale_features(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def train_and_evaluate(X_train, X_test, y_train, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return model, mse, r2

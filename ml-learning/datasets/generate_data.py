"""
Generate practice datasets for ML learning exercises.
Run this script first: python generate_data.py
"""

import numpy as np
import os

np.random.seed(42)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_student_performance(n=200):
    """Generate a clean binary classification dataset: predict pass/fail.

    Used in exercises 1 and 3. All numeric, no missing values.
    Features have intuitive relationships with the target.
    """
    study_hours = np.random.uniform(0, 40, n)
    attendance_rate = np.random.uniform(0.0, 1.0, n)
    previous_gpa = np.random.uniform(0.0, 4.0, n)
    sleep_hours = np.random.uniform(3, 10, n)
    practice_tests = np.random.randint(0, 11, n)

    # Create a logistic relationship: higher study, attendance, gpa, sleep -> pass
    z = (
        0.08 * study_hours
        + 1.5 * attendance_rate
        + 0.6 * previous_gpa
        + 0.15 * sleep_hours
        + 0.2 * practice_tests
        - 3.5  # bias to get ~60% pass rate
    )
    prob = 1 / (1 + np.exp(-z))
    # Add noise
    prob = np.clip(prob + np.random.normal(0, 0.1, n), 0.01, 0.99)
    passed = (np.random.uniform(0, 1, n) < prob).astype(int)

    # Write CSV manually (no pandas dependency for generation)
    header = "study_hours,attendance_rate,previous_gpa,sleep_hours,practice_tests,passed"
    filepath = os.path.join(SCRIPT_DIR, "student_performance.csv")
    with open(filepath, "w") as f:
        f.write(header + "\n")
        for i in range(n):
            f.write(
                f"{study_hours[i]:.2f},{attendance_rate[i]:.3f},"
                f"{previous_gpa[i]:.2f},{sleep_hours[i]:.1f},"
                f"{practice_tests[i]},{passed[i]}\n"
            )

    pass_rate = np.mean(passed)
    print(f"Created: student_performance.csv ({n} rows, {pass_rate:.0%} pass rate)")
    return n


def generate_housing_prices(n=150):
    """Generate a messy regression dataset: predict house price.

    Used in exercise 2. Has missing values, categorical columns, and
    features at different scales. Intentionally requires preprocessing.
    """
    square_feet = np.random.randint(600, 3501, n)
    num_bedrooms = np.random.randint(1, 6, n)
    num_bathrooms = np.random.randint(1, 4, n)
    year_built = np.random.randint(1950, 2024, n)
    lot_size = np.round(np.random.uniform(0.1, 2.0, n), 2)

    neighborhoods = np.random.choice(["downtown", "suburbs", "rural"], n, p=[0.3, 0.5, 0.2])
    conditions = np.random.choice(["poor", "fair", "good", "excellent"], n, p=[0.1, 0.25, 0.4, 0.25])

    garage_spaces = np.random.randint(0, 4, n).astype(float)
    # Add ~10% missing values to garage_spaces
    missing_garage = np.random.choice(n, size=int(n * 0.1), replace=False)
    garage_spaces[missing_garage] = np.nan

    # Add ~8% missing values to lot_size
    lot_size_with_missing = lot_size.copy()
    missing_lot = np.random.choice(n, size=int(n * 0.08), replace=False)
    lot_size_with_missing[missing_lot] = np.nan

    # Generate price based on features
    neighborhood_bonus = np.where(neighborhoods == "downtown", 80, np.where(neighborhoods == "suburbs", 40, 0))
    condition_bonus = np.where(
        conditions == "excellent", 60,
        np.where(conditions == "good", 30, np.where(conditions == "fair", 10, 0))
    )

    price = (
        square_feet * 0.15
        + num_bedrooms * 20
        + num_bathrooms * 15
        + (year_built - 1950) * 0.8
        + lot_size * 30
        + np.where(np.isnan(garage_spaces), 1, garage_spaces) * 25
        + neighborhood_bonus
        + condition_bonus
        + np.random.normal(0, 40, n)
    )
    price = np.round(np.maximum(price, 50), 1)  # in thousands

    # Write CSV
    header = "square_feet,num_bedrooms,num_bathrooms,year_built,lot_size,neighborhood,condition,garage_spaces,price"
    filepath = os.path.join(SCRIPT_DIR, "housing_prices.csv")
    with open(filepath, "w") as f:
        f.write(header + "\n")
        for i in range(n):
            lot_val = "" if np.isnan(lot_size_with_missing[i]) else f"{lot_size_with_missing[i]:.2f}"
            garage_val = "" if np.isnan(garage_spaces[i]) else f"{int(garage_spaces[i])}"
            f.write(
                f"{square_feet[i]},{num_bedrooms[i]},{num_bathrooms[i]},"
                f"{year_built[i]},{lot_val},{neighborhoods[i]},{conditions[i]},"
                f"{garage_val},{price[i]}\n"
            )

    n_missing = int(np.isnan(garage_spaces).sum() + np.isnan(lot_size_with_missing).sum())
    print(f"Created: housing_prices.csv ({n} rows, {n_missing} missing values)")
    return n


def generate_bike_rentals(n=200):
    """Generate a mixed-type regression dataset: predict daily bike rentals.

    Used in exercise 4. Has categorical + numeric features, some missing
    values. Requires the full preprocessing + modeling pipeline.
    """
    temperature = np.round(np.random.uniform(0, 40, n), 1)
    humidity = np.round(np.random.uniform(20, 100, n), 1)
    wind_speed = np.round(np.random.uniform(0, 50, n), 1)

    seasons = np.random.choice(["spring", "summer", "fall", "winter"], n, p=[0.25, 0.3, 0.25, 0.2])
    is_holiday = np.random.choice([0, 1], n, p=[0.9, 0.1])
    is_weekend = np.random.choice([0, 1], n, p=[0.71, 0.29])
    weather = np.random.choice(["clear", "cloudy", "rainy"], n, p=[0.5, 0.35, 0.15])

    # Add ~8% missing values to humidity and wind_speed
    humidity_with_missing = humidity.copy()
    missing_hum = np.random.choice(n, size=int(n * 0.08), replace=False)
    humidity_with_missing[missing_hum] = np.nan

    wind_with_missing = wind_speed.copy()
    missing_wind = np.random.choice(n, size=int(n * 0.08), replace=False)
    wind_with_missing[missing_wind] = np.nan

    # Generate rentals based on features
    season_effect = np.where(
        seasons == "summer", 200,
        np.where(seasons == "fall", 100, np.where(seasons == "spring", 50, 0))
    )
    weather_effect = np.where(weather == "clear", 150, np.where(weather == "cloudy", 50, 0))

    rentals = (
        temperature * 15
        + season_effect
        + weather_effect
        - humidity * 2
        - wind_speed * 3
        + is_weekend * 80
        - is_holiday * 30
        + np.random.normal(0, 60, n)
        + 300  # base
    )
    rentals = np.round(np.maximum(rentals, 10)).astype(int)

    # Write CSV
    header = "temperature,humidity,wind_speed,season,is_holiday,is_weekend,weather,rentals"
    filepath = os.path.join(SCRIPT_DIR, "bike_rentals.csv")
    with open(filepath, "w") as f:
        f.write(header + "\n")
        for i in range(n):
            hum_val = "" if np.isnan(humidity_with_missing[i]) else f"{humidity_with_missing[i]}"
            wind_val = "" if np.isnan(wind_with_missing[i]) else f"{wind_with_missing[i]}"
            f.write(
                f"{temperature[i]},{hum_val},{wind_val},"
                f"{seasons[i]},{is_holiday[i]},{is_weekend[i]},"
                f"{weather[i]},{rentals[i]}\n"
            )

    print(f"Created: bike_rentals.csv ({n} rows)")
    return n


if __name__ == "__main__":
    print("Generating ML learning datasets...\n")

    generate_student_performance()
    generate_housing_prices()
    generate_bike_rentals()

    print("\nDone! Datasets ready in datasets/ folder.")

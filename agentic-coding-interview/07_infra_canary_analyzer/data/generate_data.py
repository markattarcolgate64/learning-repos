#!/usr/bin/env python3
"""Generate synthetic canary deployment metric CSVs for the infra canary analyzer exercise."""

import csv
import os
from datetime import datetime, timedelta, timezone

import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
START_TIME = datetime(2025, 1, 15, 14, 0, 0, tzinfo=timezone.utc)
NUM_MINUTES = 60
DEPLOY_MINUTE = 15  # Deploy happens at minute 15
WARMUP_MINUTES = 3  # First 3 minutes after deploy have slightly elevated metrics

COLUMNS = ["timestamp", "latency_p50", "latency_p99", "error_rate", "cpu_percent", "memory_mb"]


def clamp(value, lo, hi):
    """Clamp a value to [lo, hi]."""
    return max(lo, min(hi, value))


def generate_timestamps():
    """Generate 60 ISO-format timestamps at 1-minute intervals."""
    return [(START_TIME + timedelta(minutes=i)).strftime("%Y-%m-%dT%H:%M:%SZ") for i in range(NUM_MINUTES)]


def warmup_factor(minute_index):
    """Return a warmup multiplier for the first few minutes after deploy.

    minute_index is relative to deploy (0 = first minute after deploy).
    Returns a value that decays from ~1.15 down to 1.0 over WARMUP_MINUTES.
    """
    if minute_index >= WARMUP_MINUTES:
        return 1.0
    # Linear decay from 1.15 to 1.0
    return 1.0 + 0.15 * (1.0 - minute_index / WARMUP_MINUTES)


def generate_baseline_row(rng):
    """Generate one row of baseline (pre-deploy) metrics."""
    return {
        "latency_p50": clamp(45.0 + rng.normal(0, 5), 20, 80),
        "latency_p99": clamp(120.0 + rng.normal(0, 15), 60, 200),
        "error_rate": clamp(0.001 + rng.normal(0, 0.0005), 0.0, 0.01),
        "cpu_percent": clamp(35.0 + rng.normal(0, 5), 5, 80),
        "memory_mb": clamp(512.0 + rng.normal(0, 20), 300, 800),
    }


def generate_clean_canary_row(rng, minutes_after_deploy):
    """Generate one row for a clean (healthy) canary deploy."""
    wf = warmup_factor(minutes_after_deploy)
    return {
        "latency_p50": clamp((45.0 + rng.normal(0, 5)) * wf, 20, 100),
        "latency_p99": clamp((120.0 + rng.normal(0, 15)) * wf, 60, 250),
        "error_rate": clamp((0.001 + rng.normal(0, 0.0005)) * wf, 0.0, 0.01),
        "cpu_percent": clamp((35.0 + rng.normal(0, 5)) * wf, 5, 85),
        "memory_mb": clamp((512.0 + rng.normal(0, 20)) * wf, 300, 850),
    }


def generate_latency_regression_row(rng, minutes_after_deploy):
    """Generate one row for a latency regression canary.

    latency_p99 jumps to ~350ms, p50 to ~80ms. Other metrics stay normal.
    """
    wf = warmup_factor(minutes_after_deploy)
    return {
        "latency_p50": clamp((80.0 + rng.normal(0, 8)) * wf, 40, 150),
        "latency_p99": clamp((350.0 + rng.normal(0, 30)) * wf, 200, 600),
        "error_rate": clamp((0.001 + rng.normal(0, 0.0005)) * wf, 0.0, 0.01),
        "cpu_percent": clamp((35.0 + rng.normal(0, 5)) * wf, 5, 85),
        "memory_mb": clamp((512.0 + rng.normal(0, 20)) * wf, 300, 850),
    }


def generate_error_spike_row(rng, minutes_after_deploy):
    """Generate one row for an error spike canary.

    error_rate jumps to ~0.05 (5%), cpu goes up slightly to ~45%.
    """
    wf = warmup_factor(minutes_after_deploy)
    return {
        "latency_p50": clamp((45.0 + rng.normal(0, 5)) * wf, 20, 100),
        "latency_p99": clamp((120.0 + rng.normal(0, 15)) * wf, 60, 250),
        "error_rate": clamp((0.05 + rng.normal(0, 0.008)) * wf, 0.005, 0.15),
        "cpu_percent": clamp((45.0 + rng.normal(0, 6)) * wf, 10, 90),
        "memory_mb": clamp((512.0 + rng.normal(0, 20)) * wf, 300, 850),
    }


def generate_file(filename, seed, canary_row_fn):
    """Generate a single CSV file.

    Args:
        filename: Output CSV filename.
        seed: Random seed for reproducibility.
        canary_row_fn: Function(rng, minutes_after_deploy) -> dict of metrics for canary period.
    """
    rng = np.random.default_rng(seed)
    timestamps = generate_timestamps()
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()

        for i in range(NUM_MINUTES):
            if i < DEPLOY_MINUTE:
                # Baseline period
                row = generate_baseline_row(rng)
            else:
                # Canary period
                minutes_after_deploy = i - DEPLOY_MINUTE
                row = canary_row_fn(rng, minutes_after_deploy)

            row["timestamp"] = timestamps[i]

            # Round values for readability
            row["latency_p50"] = round(row["latency_p50"], 2)
            row["latency_p99"] = round(row["latency_p99"], 2)
            row["error_rate"] = round(row["error_rate"], 6)
            row["cpu_percent"] = round(row["cpu_percent"], 2)
            row["memory_mb"] = round(row["memory_mb"], 2)

            writer.writerow(row)

    print(f"Generated {filepath}")


def verify_files():
    """Verify each CSV has the right structure."""
    files = [
        "deploy_01_clean.csv",
        "deploy_02_clean.csv",
        "deploy_03_clean.csv",
        "deploy_04_latency_regression.csv",
        "deploy_05_error_spike.csv",
    ]
    all_ok = True
    for filename in files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Check columns
        expected_cols = set(COLUMNS)
        actual_cols = set(reader.fieldnames)
        if actual_cols != expected_cols:
            print(f"FAIL {filename}: columns mismatch. Expected {expected_cols}, got {actual_cols}")
            all_ok = False
            continue

        # Check row count
        if len(rows) != NUM_MINUTES:
            print(f"FAIL {filename}: expected {NUM_MINUTES} rows, got {len(rows)}")
            all_ok = False
            continue

        # Check first and last timestamps
        first_ts = rows[0]["timestamp"]
        last_ts = rows[-1]["timestamp"]
        expected_first = "2025-01-15T14:00:00Z"
        expected_last = "2025-01-15T14:59:00Z"
        if first_ts != expected_first:
            print(f"FAIL {filename}: first timestamp {first_ts} != {expected_first}")
            all_ok = False
        if last_ts != expected_last:
            print(f"FAIL {filename}: last timestamp {last_ts} != {expected_last}")
            all_ok = False

        # Check no negative values and error_rate in [0, 1]
        for j, row in enumerate(rows):
            for col in ["latency_p50", "latency_p99", "cpu_percent", "memory_mb"]:
                if float(row[col]) < 0:
                    print(f"FAIL {filename} row {j}: {col} is negative ({row[col]})")
                    all_ok = False
            er = float(row["error_rate"])
            if er < 0 or er > 1:
                print(f"FAIL {filename} row {j}: error_rate out of range ({er})")
                all_ok = False

        # Print summary stats for canary period (minutes 15-59)
        canary_rows = rows[DEPLOY_MINUTE:]
        p50_avg = sum(float(r["latency_p50"]) for r in canary_rows) / len(canary_rows)
        p99_avg = sum(float(r["latency_p99"]) for r in canary_rows) / len(canary_rows)
        er_avg = sum(float(r["error_rate"]) for r in canary_rows) / len(canary_rows)
        cpu_avg = sum(float(r["cpu_percent"]) for r in canary_rows) / len(canary_rows)
        mem_avg = sum(float(r["memory_mb"]) for r in canary_rows) / len(canary_rows)

        print(f"OK {filename}: {len(rows)} rows | canary avg: "
              f"p50={p50_avg:.1f}ms p99={p99_avg:.1f}ms err={er_avg:.4f} "
              f"cpu={cpu_avg:.1f}% mem={mem_avg:.0f}MB")

    if all_ok:
        print("\nAll files verified successfully.")
    else:
        print("\nSome files had issues.")


def main():
    # File 1: Clean deploy (seed 42)
    generate_file("deploy_01_clean.csv", seed=42, canary_row_fn=generate_clean_canary_row)

    # File 2: Clean deploy (seed 123)
    generate_file("deploy_02_clean.csv", seed=123, canary_row_fn=generate_clean_canary_row)

    # File 3: Clean deploy (seed 777)
    generate_file("deploy_03_clean.csv", seed=777, canary_row_fn=generate_clean_canary_row)

    # File 4: Latency regression (seed 2024)
    generate_file("deploy_04_latency_regression.csv", seed=2024, canary_row_fn=generate_latency_regression_row)

    # File 5: Error spike (seed 9999)
    generate_file("deploy_05_error_spike.csv", seed=9999, canary_row_fn=generate_error_spike_row)

    print()
    verify_files()


if __name__ == "__main__":
    main()

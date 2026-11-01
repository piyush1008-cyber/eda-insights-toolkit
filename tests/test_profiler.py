"""Unit tests for statistical profiler and collinearity checks."""

import numpy as np
import pandas as pd
from src.profiler import DatasetProfiler


def test_profiler_basic_metrics():
    data = {
        "num1": [10.0, 20.0, 30.0, 40.0, 50.0],
        "cat1": ["A", "B", "A", "A", "C"],
    }
    df = pd.DataFrame(data)

    profiler = DatasetProfiler()
    profile = profiler.profile_dataframe(df)

    assert profile.row_count == 5
    assert profile.col_count == 2
    assert profile.duplicated_rows == 0
    assert "num1" in profile.numeric_columns
    assert profile.numeric_columns["num1"]["mean"] == 30.0
    assert profile.numeric_columns["num1"]["min"] == 10.0
    assert profile.numeric_columns["num1"]["max"] == 50.0

    assert "cat1" in profile.categorical_columns
    assert profile.categorical_columns["cat1"]["unique"] == 3
    assert profile.categorical_columns["cat1"]["top"] == "A"


def test_profiler_missing_values_and_duplicates():
    data = {
        "feature_a": [1, 2, np.nan, 4, 1],
        "feature_b": ["x", "y", "z", "w", "x"],
    }
    df = pd.DataFrame(data)

    profiler = DatasetProfiler()
    profile = profiler.profile_dataframe(df)

    assert profile.duplicated_rows == 1  # Row 0 and Row 4 are duplicates
    assert profile.missing_summary["feature_a"]["missing_count"] == 1
    assert profile.missing_summary["feature_a"]["missing_pct"] == 20.0


def test_collinear_pair_detection():
    x = np.linspace(1, 100, 50)
    y = x * 2.5 + np.random.normal(0, 0.1, 50)  # Near perfect correlation r ~ 1.0

    df = pd.DataFrame({"x": x, "y": y, "z": np.random.uniform(0, 1, 50)})
    profiler = DatasetProfiler(collinear_threshold=0.90)
    profile = profiler.profile_dataframe(df)

    assert len(profile.collinear_pairs) == 1
    c1, c2, r = profile.collinear_pairs[0]
    assert set([c1, c2]) == {"x", "y"}
    assert r > 0.95

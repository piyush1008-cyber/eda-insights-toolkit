"""Statistical profiling and dataset diagnostics engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


@dataclass
class DatasetProfile:
    """Encapsulates comprehensive EDA metrics for a dataset."""
    row_count: int
    col_count: int
    memory_kb: float
    duplicated_rows: int
    numeric_columns: Dict[str, Dict]
    categorical_columns: Dict[str, Dict]
    missing_summary: Dict[str, Dict]
    correlations: Dict[str, Dict[str, float]]
    collinear_pairs: List[Tuple[str, str, float]]


class DatasetProfiler:
    """Profiles tabular datasets and extracts statistical distributions."""

    def __init__(self, collinear_threshold: float = 0.80):
        self.collinear_threshold = collinear_threshold

    def profile_dataframe(self, df: pd.DataFrame) -> DatasetProfile:
        """Profiles a pandas DataFrame across all dimensions."""
        row_count, col_count = df.shape
        memory_kb = round(df.memory_usage(deep=True).sum() / 1024, 2)
        duplicated = int(df.duplicated().sum())

        numeric_cols: Dict[str, Dict] = {}
        categorical_cols: Dict[str, Dict] = {}
        missing_summary: Dict[str, Dict] = {}

        # 1. Missingness & Type Profiling
        for col in df.columns:
            null_count = int(df[col].isnull().sum())
            null_pct = round((null_count / max(1, row_count)) * 100, 2)
            missing_summary[col] = {
                "missing_count": null_count,
                "missing_pct": null_pct,
                "dtype": str(df[col].dtype),
            }

            if pd.api.types.is_numeric_dtype(df[col]):
                series = df[col].dropna()
                if len(series) > 0:
                    numeric_cols[col] = {
                        "count": int(series.count()),
                        "mean": round(float(series.mean()), 2),
                        "std": round(float(series.std()), 2) if len(series) > 1 else 0.0,
                        "min": round(float(series.min()), 2),
                        "q25": round(float(series.quantile(0.25)), 2),
                        "median": round(float(series.median()), 2),
                        "q75": round(float(series.quantile(0.75)), 2),
                        "max": round(float(series.max()), 2),
                        "skewness": round(float(series.skew()), 2) if len(series) > 2 else 0.0,
                    }
            else:
                series = df[col].astype(str)
                counts = series.value_counts()
                top_val = counts.index[0] if len(counts) > 0 else "-"
                top_freq = int(counts.iloc[0]) if len(counts) > 0 else 0
                top_5 = {str(k): int(v) for k, v in counts.head(5).items()}

                categorical_cols[col] = {
                    "count": int(series.count()),
                    "unique": int(df[col].nunique()),
                    "top": top_val,
                    "top_freq": top_freq,
                    "distribution": top_5,
                }

        # 2. Correlation Matrix for Numeric Features
        correlations: Dict[str, Dict[str, float]] = {}
        collinear_pairs: List[Tuple[str, str, float]] = []

        num_df = df.select_dtypes(include=[np.number])
        if num_df.shape[1] > 1:
            corr_matrix = num_df.corr().round(3)
            for c1 in corr_matrix.columns:
                correlations[c1] = {}
                for c2 in corr_matrix.columns:
                    correlations[c1][c2] = float(corr_matrix.loc[c1, c2])

            cols = list(corr_matrix.columns)
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    val = corr_matrix.iloc[i, j]
                    if abs(val) >= self.collinear_threshold and not np.isnan(val):
                        collinear_pairs.append((cols[i], cols[j], float(val)))

        return DatasetProfile(
            row_count=row_count,
            col_count=col_count,
            memory_kb=memory_kb,
            duplicated_rows=duplicated,
            numeric_columns=numeric_cols,
            categorical_columns=categorical_cols,
            missing_summary=missing_summary,
            correlations=correlations,
            collinear_pairs=collinear_pairs,
        )

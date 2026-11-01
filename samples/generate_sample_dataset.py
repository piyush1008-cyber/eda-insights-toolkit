"""Generates a synthetic e-commerce / customer churn CSV dataset for testing."""

import random
from pathlib import Path
import numpy as np
import pandas as pd


def generate_sample_csv(output_path: Path, n_rows: int = 250) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)
    random.seed(42)

    genders = ["Female", "Male"]
    contracts = ["Month-to-month", "One year", "Two year"]
    payment_methods = ["Electronic check", "Mailed check", "Bank transfer", "Credit card"]

    data = {
        "customer_id": [f"CUST_{i:04d}" for i in range(1, n_rows + 1)],
        "gender": [random.choice(genders) for _ in range(n_rows)],
        "senior_citizen": [random.choice([0, 1]) for _ in range(n_rows)],
        "tenure_months": np.random.randint(1, 72, size=n_rows),
        "contract": [random.choice(contracts) for _ in range(n_rows)],
        "payment_method": [random.choice(payment_methods) for _ in range(n_rows)],
        "monthly_charges": np.round(np.random.uniform(20.0, 118.0, size=n_rows), 2),
    }

    # Add collinear feature (total_charges strongly correlates with monthly_charges * tenure)
    data["total_charges"] = np.round(data["monthly_charges"] * data["tenure_months"] * np.random.uniform(0.95, 1.05, size=n_rows), 2)
    data["churn"] = [random.choice(["Yes", "No", "No", "No"]) for _ in range(n_rows)]

    df = pd.DataFrame(data)

    # Introduce realistic missing values (5%)
    for col in ["contract", "monthly_charges"]:
        mask = np.random.rand(n_rows) < 0.05
        df.loc[mask, col] = np.nan

    # Add 2 duplicate rows
    df = pd.concat([df, df.iloc[:2]], ignore_index=True)

    df.to_csv(output_path, index=False)
    print(f"Generated sample dataset: {output_path} ({df.shape[0]} rows, {df.shape[1]} columns)")


if __name__ == "__main__":
    generate_sample_csv(Path("samples/customers.csv"))

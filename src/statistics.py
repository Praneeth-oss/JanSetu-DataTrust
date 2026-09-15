from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_public_service_records.csv"
)


def main():
    df = pd.read_csv(INPUT_FILE)

    numeric_columns = [
        "age",
        "annual_income",
        "service_requests",
    ]

    print("\n=== JANSETU STATISTICAL PROFILE ===")

    for column in numeric_columns:
        series = df[column].dropna()

        print(f"\n--- {column} ---")
        print(f"Count: {len(series)}")
        print(f"Mean: {series.mean():.2f}")
        print(f"Median: {series.median():.2f}")
        print(f"Std Dev: {series.std():.2f}")
        print(f"Minimum: {series.min():.2f}")
        print(f"Maximum: {series.max():.2f}")

        print(
            f"25th Percentile: "
            f"{series.quantile(0.25):.2f}"
        )

        print(
            f"75th Percentile: "
            f"{series.quantile(0.75):.2f}"
        )


if __name__ == "__main__":
    main()
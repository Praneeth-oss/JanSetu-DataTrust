from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "public_service_records.csv"


def profile_data(df: pd.DataFrame) -> dict:
    profile = {}

    profile["rows"] = len(df)
    profile["columns"] = len(df.columns)
    profile["duplicate_rows"] = int(df.duplicated().sum())

    missing = df.isna().sum()
    profile["missing_values"] = {
        column: int(count)
        for column, count in missing.items()
        if count > 0
    }

    profile["age_out_of_range"] = int(
        ((df["age"] < 18) | (df["age"] > 100)).sum()
    )

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    invalid_email = (
        df["email"]
        .notna()
        & ~df["email"].astype(str).str.match(email_pattern)
    )
    profile["invalid_emails"] = int(invalid_email.sum())

    phone_pattern = r"^[6-9]\d{9}$"
    invalid_phone = (
        df["phone"]
        .notna()
        & ~df["phone"].astype(str).str.match(phone_pattern)
    )
    profile["invalid_phones"] = int(invalid_phone.sum())

    valid_states = {
        "Andhra Pradesh",
        "Telangana",
        "Karnataka",
        "Tamil Nadu",
        "Maharashtra",
    }

    profile["inconsistent_states"] = int(
        (
            df["state"].notna()
            & ~df["state"].astype(str).isin(valid_states)
        ).sum()
    )

    valid_departments = {
        "Health",
        "Education",
        "Rural Development",
        "Social Welfare",
        "Transport",
    }

    profile["inconsistent_departments"] = int(
        (
            df["department"].notna()
            & ~df["department"].astype(str).isin(valid_departments)
        ).sum()
    )

    parsed_dates = pd.to_datetime(
        df["registration_date"],
        errors="coerce",
        format="mixed",
    )

    profile["invalid_dates"] = int(parsed_dates.isna().sum())

    profile["numeric_summary"] = (
        df[
            [
                "age",
                "annual_income",
                "service_requests",
            ]
        ]
        .describe()
        .round(2)
        .to_dict()
    )

    return profile


def main():
    df = pd.read_csv(INPUT_FILE)
    profile = profile_data(df)

    print("\n=== JANSETU DATA QUALITY PROFILE ===")
    print(f"Rows: {profile['rows']}")
    print(f"Columns: {profile['columns']}")
    print(f"Duplicate rows: {profile['duplicate_rows']}")

    print("\nMissing values:")
    for column, count in profile["missing_values"].items():
        print(f"  {column}: {count}")

    print(f"\nAge out of range: {profile['age_out_of_range']}")
    print(f"Invalid emails: {profile['invalid_emails']}")
    print(f"Invalid phones: {profile['invalid_phones']}")
    print(f"Inconsistent states: {profile['inconsistent_states']}")
    print(f"Inconsistent departments: {profile['inconsistent_departments']}")
    print(f"Invalid dates: {profile['invalid_dates']}")


if __name__ == "__main__":
    main()
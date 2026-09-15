from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "public_service_records.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "cleaned_public_service_records.csv"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


VALID_STATES = {
    "Andhra Pradesh",
    "Telangana",
    "Karnataka",
    "Tamil Nadu",
    "Maharashtra",
}

VALID_DEPARTMENTS = {
    "Health",
    "Education",
    "Rural Development",
    "Social Welfare",
    "Transport",
}


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    # ---------------------------------------------------------
    # 1. TEXT STANDARDIZATION
    # ---------------------------------------------------------

    df["record_id"] = (
        df["record_id"]
        .astype("string")
        .str.strip()
    )

    df["full_name"] = (
        df["full_name"]
        .astype("string")
        .str.strip()
    )

    df["email"] = (
        df["email"]
        .astype("string")
        .str.strip()
    )

    df["phone"] = (
        df["phone"]
        .astype("string")
        .str.strip()
    )

    df["state"] = (
        df["state"]
        .astype("string")
        .str.strip()
    )

    df["department"] = (
        df["department"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    # ---------------------------------------------------------
    # 2. STANDARDIZE KNOWN STATE SPELLING
    # ---------------------------------------------------------

    state_corrections = {
        "Andhra pradesh": "Andhra Pradesh",
    }

    df["state"] = df["state"].replace(
        state_corrections
    )

    # ---------------------------------------------------------
    # 3. STANDARDIZE DATES
    # ---------------------------------------------------------

    parsed_dates = pd.to_datetime(
        df["registration_date"],
        errors="coerce",
        format="mixed",
    )

    df["registration_date"] = (
        parsed_dates.dt.strftime("%Y-%m-%d")
    )

    # ---------------------------------------------------------
    # 4. NUMERIC FIELDS
    # ---------------------------------------------------------

    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce",
    )

    df["annual_income"] = pd.to_numeric(
        df["annual_income"],
        errors="coerce",
    )

    df["service_requests"] = pd.to_numeric(
        df["service_requests"],
        errors="coerce",
    )

    # ---------------------------------------------------------
    # 5. AGE VALIDATION
    # Invalid values become missing.
    # We do not invent replacement ages.
    # ---------------------------------------------------------

    invalid_age = (
        df["age"].notna()
        & ~df["age"].between(18, 100)
    )

    df.loc[invalid_age, "age"] = pd.NA

    # ---------------------------------------------------------
    # 6. EMAIL VALIDATION
    # ---------------------------------------------------------

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    invalid_email = (
        df["email"].notna()
        & ~df["email"].str.match(
            email_pattern,
            na=False,
        )
    )

    df.loc[invalid_email, "email"] = pd.NA

    # ---------------------------------------------------------
    # 7. PHONE VALIDATION
    # Explicit string handling prevents numeric .0 problems.
    # ---------------------------------------------------------

    phone_pattern = r"^[6-9]\d{9}$"

    invalid_phone = (
        df["phone"].notna()
        & ~df["phone"].str.match(
            phone_pattern,
            na=False,
        )
    )

    df.loc[invalid_phone, "phone"] = pd.NA

    # ---------------------------------------------------------
    # 8. CATEGORY VALIDATION
    # ---------------------------------------------------------

    invalid_state = (
        df["state"].notna()
        & ~df["state"].isin(VALID_STATES)
    )

    df.loc[invalid_state, "state"] = pd.NA

    invalid_department = (
        df["department"].notna()
        & ~df["department"].isin(
            VALID_DEPARTMENTS
        )
    )

    df.loc[invalid_department, "department"] = pd.NA

    # ---------------------------------------------------------
    # 9. REMOVE EXACT DUPLICATES
    # ---------------------------------------------------------

    df = (
        df
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return df


def main():

    # Explicitly preserve email and phone as text.
    df = pd.read_csv(
        INPUT_FILE,
        dtype={
            "email": "string",
            "phone": "string",
        },
    )

    original_rows = len(df)

    cleaned_df = clean_data(df)

    cleaned_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n=== JANSETU DATA CLEANING ===")
    print(f"Original rows: {original_rows}")
    print(f"Cleaned rows: {len(cleaned_df)}")
    print(
        "Rows removed as duplicates: "
        f"{original_rows - len(cleaned_df)}"
    )
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
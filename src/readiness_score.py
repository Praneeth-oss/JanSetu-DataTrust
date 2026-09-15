from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_public_service_records.csv"
)


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


def calculate_completeness(df: pd.DataFrame) -> float:
    """
    Measures the percentage of cells containing data.
    """

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = int(
        df.isna().sum().sum()
    )

    return (
        1 - (missing_cells / total_cells)
    ) * 100


def calculate_validity(df: pd.DataFrame) -> float:
    """
    Measures validity of values that are actually present.

    Missing values are NOT counted as invalid here because
    missingness is measured separately by completeness.
    """

    # Age
    age_present = df["age"].notna()

    valid_age = (
        df.loc[age_present, "age"]
        .between(18, 100)
    )

    # Email
    email_present = df["email"].notna()

    valid_email = (
        df.loc[email_present, "email"]
        .str.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            na=False,
        )
    )

    # Phone
    phone_present = df["phone"].notna()

    valid_phone = (
        df.loc[phone_present, "phone"]
        .str.match(
            r"^[6-9]\d{9}$",
            na=False,
        )
    )

    valid_count = (
        int(valid_age.sum())
        + int(valid_email.sum())
        + int(valid_phone.sum())
    )

    present_count = (
        int(age_present.sum())
        + int(email_present.sum())
        + int(phone_present.sum())
    )

    if present_count == 0:
        return 0.0

    return (
        valid_count / present_count
    ) * 100


def calculate_consistency(df: pd.DataFrame) -> float:
    """
    Measures whether populated categorical fields follow
    the approved controlled vocabulary.
    """

    state_present = df["state"].notna()

    valid_state = (
        df.loc[state_present, "state"]
        .isin(VALID_STATES)
    )

    department_present = df["department"].notna()

    valid_department = (
        df.loc[department_present, "department"]
        .isin(VALID_DEPARTMENTS)
    )

    valid_count = (
        int(valid_state.sum())
        + int(valid_department.sum())
    )

    present_count = (
        int(state_present.sum())
        + int(department_present.sum())
    )

    if present_count == 0:
        return 0.0

    return (
        valid_count / present_count
    ) * 100


def calculate_uniqueness(df: pd.DataFrame) -> float:
    """
    Measures the proportion of records that are not duplicates.
    """

    duplicate_rows = int(
        df.duplicated().sum()
    )

    return (
        1 - (duplicate_rows / len(df))
    ) * 100


def calculate_schema_readiness(df: pd.DataFrame) -> float:
    """
    Measures whether the expected analytical fields exist.
    """

    expected_fields = {
        "record_id",
        "full_name",
        "age",
        "state",
        "department",
        "annual_income",
        "service_requests",
        "registration_date",
        "email",
        "phone",
    }

    matching_fields = (
        expected_fields.intersection(
            df.columns
        )
    )

    return (
        len(matching_fields)
        / len(expected_fields)
    ) * 100


def main():

    # Preserve email and phone as text.
    df = pd.read_csv(
        INPUT_FILE,
        dtype={
            "email": "string",
            "phone": "string",
        },
    )

    completeness = calculate_completeness(df)
    validity = calculate_validity(df)
    consistency = calculate_consistency(df)
    uniqueness = calculate_uniqueness(df)
    schema_readiness = calculate_schema_readiness(df)

    # ---------------------------------------------------------
    # Weighted AI Readiness Score
    #
    # Completeness:   30%
    # Validity:       25%
    # Consistency:    20%
    # Uniqueness:     15%
    # Schema:         10%
    # ---------------------------------------------------------

    overall_score = (
        completeness * 0.30
        + validity * 0.25
        + consistency * 0.20
        + uniqueness * 0.15
        + schema_readiness * 0.10
    )

    print("\n=== JANSETU AI READINESS SCORE ===")

    print(
        f"Completeness: "
        f"{completeness:.2f}%"
    )

    print(
        f"Validity: "
        f"{validity:.2f}%"
    )

    print(
        f"Consistency: "
        f"{consistency:.2f}%"
    )

    print(
        f"Uniqueness: "
        f"{uniqueness:.2f}%"
    )

    print(
        f"Schema Readiness: "
        f"{schema_readiness:.2f}%"
    )

    print(
        f"Overall AI Readiness: "
        f"{overall_score:.2f}%"
    )

    print(
        f"\nFinal AI Readiness Score: "
        f"{overall_score:.2f}/100"
    )


if __name__ == "__main__":
    main()
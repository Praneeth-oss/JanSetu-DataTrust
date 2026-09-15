from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "public_service_records.csv"
)

CLEAN_FILE = (
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


def assess_quality(df: pd.DataFrame) -> dict:

    duplicate_rows = int(
        df.duplicated().sum()
    )

    missing_values = int(
        df.isna().sum().sum()
    )

    age_out_of_range = int(
        (
            df["age"].notna()
            & ~df["age"].between(18, 100)
        ).sum()
    )

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    invalid_emails = int(
        (
            df["email"].notna()
            & ~df["email"].str.match(
                email_pattern,
                na=False,
            )
        ).sum()
    )

    phone_pattern = r"^[6-9]\d{9}$"

    invalid_phones = int(
        (
            df["phone"].notna()
            & ~df["phone"].str.match(
                phone_pattern,
                na=False,
            )
        ).sum()
    )

    inconsistent_states = int(
        (
            df["state"].notna()
            & ~df["state"].isin(
                VALID_STATES
            )
        ).sum()
    )

    inconsistent_departments = int(
        (
            df["department"].notna()
            & ~df["department"].isin(
                VALID_DEPARTMENTS
            )
        ).sum()
    )

    total_issues = (
        duplicate_rows
        + missing_values
        + age_out_of_range
        + invalid_emails
        + invalid_phones
        + inconsistent_states
        + inconsistent_departments
    )

    return {
        "rows": len(df),
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "age_out_of_range": age_out_of_range,
        "invalid_emails": invalid_emails,
        "invalid_phones": invalid_phones,
        "inconsistent_states": inconsistent_states,
        "inconsistent_departments": inconsistent_departments,
        "total_issues": total_issues,
    }


def print_report(
    title: str,
    report: dict,
):

    print(f"\n=== {title} ===")
    print(f"Rows: {report['rows']}")
    print(
        f"Missing values: "
        f"{report['missing_values']}"
    )
    print(
        f"Duplicate rows: "
        f"{report['duplicate_rows']}"
    )
    print(
        f"Age out of range: "
        f"{report['age_out_of_range']}"
    )
    print(
        f"Invalid emails: "
        f"{report['invalid_emails']}"
    )
    print(
        f"Invalid phones: "
        f"{report['invalid_phones']}"
    )
    print(
        f"Inconsistent states: "
        f"{report['inconsistent_states']}"
    )
    print(
        f"Inconsistent departments: "
        f"{report['inconsistent_departments']}"
    )
    print(
        f"Total detected issues: "
        f"{report['total_issues']}"
    )


def main():

    # Keep phone and email fields as text.
    raw_df = pd.read_csv(
        RAW_FILE,
        dtype={
            "email": "string",
            "phone": "string",
        },
    )

    clean_df = pd.read_csv(
        CLEAN_FILE,
        dtype={
            "email": "string",
            "phone": "string",
        },
    )

    before = assess_quality(raw_df)
    after = assess_quality(clean_df)

    print_report(
        "BEFORE CLEANING",
        before,
    )

    print_report(
        "AFTER CLEANING",
        after,
    )

    issues_reduced = (
        before["total_issues"]
        - after["total_issues"]
    )

    print("\n=== QUALITY IMPROVEMENT ===")
    print(
        f"Issues before: "
        f"{before['total_issues']}"
    )
    print(
        f"Issues after: "
        f"{after['total_issues']}"
    )
    print(
        f"Issues reduced: "
        f"{issues_reduced}"
    )


if __name__ == "__main__":
    main()
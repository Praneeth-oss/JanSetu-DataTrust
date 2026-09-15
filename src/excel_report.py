from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "jansetu.db"
)

CLEAN_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_public_service_records.csv"
)

ANOMALY_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "anomaly_review.csv"
)

DICTIONARY_FILE = (
    PROJECT_ROOT
    / "docs"
    / "data_dictionary.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "JanSetu_Data_Quality_Report.xlsx"
)


def main():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------
    # Load cleaned dataset.
    # ---------------------------------------------------------

    df = pd.read_csv(
        CLEAN_FILE,
        dtype={
            "email": "string",
            "phone": "string",
        },
    )

    # ---------------------------------------------------------
    # Quality summary.
    # ---------------------------------------------------------

    quality_summary = pd.DataFrame(
        {
            "Metric": [
                "Total Records",
                "Total Columns",
                "Missing Cells",
                "Duplicate Records",
                "Missing Age",
                "Missing State",
                "Missing Income",
                "Missing Email",
                "Missing Phone",
            ],
            "Value": [
                len(df),
                len(df.columns),
                int(df.isna().sum().sum()),
                int(df.duplicated().sum()),
                int(df["age"].isna().sum()),
                int(df["state"].isna().sum()),
                int(df["annual_income"].isna().sum()),
                int(df["email"].isna().sum()),
                int(df["phone"].isna().sum()),
            ],
        }
    )

    # ---------------------------------------------------------
    # State analysis using SQLite.
    # ---------------------------------------------------------

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    state_analysis = pd.read_sql_query(
        """
        SELECT
            state,
            COUNT(*) AS record_count,
            ROUND(AVG(annual_income), 2)
                AS average_income,
            SUM(service_requests)
                AS total_service_requests
        FROM public_service_records
        GROUP BY state
        ORDER BY record_count DESC
        """,
        connection,
    )

    # ---------------------------------------------------------
    # Department analysis.
    # ---------------------------------------------------------

    department_analysis = pd.read_sql_query(
        """
        SELECT
            department,
            COUNT(*) AS record_count,
            ROUND(AVG(service_requests), 2)
                AS average_requests,
            SUM(service_requests)
                AS total_service_requests
        FROM public_service_records
        GROUP BY department
        ORDER BY total_service_requests DESC
        """,
        connection,
    )

    connection.close()

    # ---------------------------------------------------------
    # Load data dictionary.
    # ---------------------------------------------------------

    data_dictionary = pd.read_csv(
        DICTIONARY_FILE
    )

    # ---------------------------------------------------------
    # Load anomaly review.
    # ---------------------------------------------------------

    if ANOMALY_FILE.exists():

        anomaly_review = pd.read_csv(
            ANOMALY_FILE,
            dtype={
                "email": "string",
                "phone": "string",
            },
        )

    else:

        anomaly_review = pd.DataFrame(
            {
                "Status": [
                    "Anomaly review file not found."
                ]
            }
        )

    # ---------------------------------------------------------
    # Write Excel workbook.
    # ---------------------------------------------------------

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl",
    ) as writer:

        quality_summary.to_excel(
            writer,
            sheet_name="Quality Summary",
            index=False,
        )

        data_dictionary.to_excel(
            writer,
            sheet_name="Data Dictionary",
            index=False,
        )

        state_analysis.to_excel(
            writer,
            sheet_name="State Analysis",
            index=False,
        )

        department_analysis.to_excel(
            writer,
            sheet_name="Department Analysis",
            index=False,
        )

        anomaly_review.to_excel(
            writer,
            sheet_name="Anomaly Review",
            index=False,
        )

    print("\n=== JANSETU EXCEL REPORT ===")
    print(f"Workbook created: {OUTPUT_FILE}")
    print("Sheets created: 5")


if __name__ == "__main__":
    main()
from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_public_service_records.csv"
)

DATABASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "jansetu.db"
)


def main():
    df = pd.read_csv(INPUT_FILE)

    connection = sqlite3.connect(DATABASE_FILE)

    df.to_sql(
        "public_service_records",
        connection,
        if_exists="replace",
        index=False,
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_state
        ON public_service_records(state)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_department
        ON public_service_records(department)
        """
    )

    connection.commit()

    cursor.execute(
        "SELECT COUNT(*) FROM public_service_records"
    )

    row_count = cursor.fetchone()[0]

    connection.close()

    print("\n=== JANSETU SQLITE DATABASE ===")
    print(f"Rows loaded: {row_count}")
    print(f"Database: {DATABASE_FILE}")


if __name__ == "__main__":
    main()
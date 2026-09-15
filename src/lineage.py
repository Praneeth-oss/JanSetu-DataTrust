from pathlib import Path
from datetime import datetime, timezone
import json


PROJECT_ROOT = Path(__file__).resolve().parent.parent

LINEAGE_FILE = (
    PROJECT_ROOT
    / "docs"
    / "data_lineage.jsonl"
)


def record_operation(
    operation,
    input_records,
    output_records,
    records_affected,
    reason,
):
    event = {
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "operation": operation,
        "input_records": input_records,
        "output_records": output_records,
        "records_affected": records_affected,
        "reason": reason,
    }

    with open(
        LINEAGE_FILE,
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(event)
            + "\n"
        )

    return event


def main():

    LINEAGE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Start with a clean lineage file
    # for this project run.
    if LINEAGE_FILE.exists():
        LINEAGE_FILE.unlink()

    record_operation(
        operation="INGESTION",
        input_records=1003,
        output_records=1003,
        records_affected=0,
        reason=(
            "Loaded synthetic public-sector "
            "records for quality assessment."
        ),
    )

    record_operation(
        operation="CLEANING",
        input_records=1003,
        output_records=1000,
        records_affected=3,
        reason=(
            "Removed three exact duplicate "
            "records."
        ),
    )

    record_operation(
        operation="STANDARDIZATION",
        input_records=1000,
        output_records=1000,
        records_affected=6,
        reason=(
            "Standardized categories, dates, "
            "and invalid values for analyst review."
        ),
    )

    record_operation(
        operation="SQL_LOAD",
        input_records=1000,
        output_records=1000,
        records_affected=0,
        reason=(
            "Loaded cleaned records into "
            "SQLite for analytical queries."
        ),
    )

    print("\n=== JANSETU DATA LINEAGE ===")
    print(f"Lineage file: {LINEAGE_FILE}")

    with open(
        LINEAGE_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        events = file.readlines()

    print(f"Events recorded: {len(events)}")

    for line in events:
        event = json.loads(line)

        print(
            f"{event['operation']}: "
            f"{event['input_records']} -> "
            f"{event['output_records']} | "
            f"Affected: "
            f"{event['records_affected']}"
        )


if __name__ == "__main__":
    main()
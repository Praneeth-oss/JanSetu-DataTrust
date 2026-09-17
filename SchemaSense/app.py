import csv
import re
from pathlib import Path
from html import escape


def detect_type(column, values):
    """Detect a practical field type using column semantics and value patterns."""

    clean = [v.strip() for v in values if v and v.strip()]

    if not clean:
        return "Unknown"

    column_name = column.lower().strip()

    # Identifier and personal/contact fields should be treated as text.
    # Phone numbers and IDs are identifiers, not quantities for mathematical analysis.
    text_fields = [
        "id",
        "record_id",
        "email",
        "phone",
        "mobile",
        "address",
        "name",
    ]

    if any(
        field == column_name or column_name.endswith(f"_{field}")
        or column_name.startswith(f"{field}_")
        for field in text_fields
    ):
        return "Text"

    # Detect ISO date format.
    date_count = sum(
        1 for v in clean
        if re.match(r"^\d{4}-\d{2}-\d{2}$", v)
    )

    if date_count / len(clean) >= 0.95:
        return "Date"

    # Detect numeric fields.
    numeric_count = 0

    for value in clean:
        try:
            float(value)
            numeric_count += 1
        except ValueError:
            pass

    if numeric_count / len(clean) >= 0.95:
        return "Numeric"

    # Low-cardinality fields are treated as categorical.
    unique_ratio = len(set(clean)) / len(clean)

    if unique_ratio < 0.20:
        return "Categorical"

    return "Text"


def sensitive_flag(column):
    """Return heuristic governance indicators for analyst review."""

    name = column.lower().strip()

    personal_fields = [
        "email",
        "phone",
        "mobile",
        "address",
        "name",
    ]

    financial_fields = [
        "income",
        "salary",
        "financial",
    ]

    if any(field in name for field in personal_fields):
        return "Potential Personal Data"

    if any(field in name for field in financial_fields):
        return "Potential Financial Data"

    return "No obvious flag"


def main():
    root = Path(__file__).resolve().parent

    input_file = root / "sample_data.csv"
    profile_file = root / "schema_profile.csv"
    dictionary_file = root / "data_dictionary.csv"
    report_file = root / "schemasense_report.html"

    # ---------------------------------------------------------
    # LOAD DATASET
    # ---------------------------------------------------------

    with open(
        input_file,
        newline="",
        encoding="utf-8"
    ) as f:

        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames

    if not columns:
        raise ValueError("No columns found in the input dataset.")

    if not rows:
        raise ValueError("The input dataset contains no records.")

    # ---------------------------------------------------------
    # PROFILE COLUMNS
    # ---------------------------------------------------------

    profiles = []

    for column in columns:

        values = [
            row.get(column, "")
            for row in rows
        ]

        missing = sum(
            1
            for value in values
            if not value or not value.strip()
        )

        non_missing = [
            value.strip()
            for value in values
            if value and value.strip()
        ]

        unique = len(set(non_missing))

        duplicates = len(non_missing) - unique

        detected_type = detect_type(
            column,
            values
        )

        governance = sensitive_flag(column)

        profiles.append(
            {
                "column": column,
                "data_type": detected_type,
                "records": len(values),
                "missing": missing,
                "missing_pct": round(
                    (missing / len(values)) * 100,
                    2
                ),
                "unique_values": unique,
                "duplicate_values": duplicates,
                "governance_flag": governance,
            }
        )

    # ---------------------------------------------------------
    # DATASET COMPLETENESS
    # ---------------------------------------------------------

    total_cells = len(rows) * len(columns)

    missing_cells = sum(
        profile["missing"]
        for profile in profiles
    )

    completeness = (
        (total_cells - missing_cells)
        / total_cells
    ) * 100

    # ---------------------------------------------------------
    # WRITE SCHEMA PROFILE
    # ---------------------------------------------------------

    with open(
        profile_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=profiles[0].keys()
        )

        writer.writeheader()
        writer.writerows(profiles)

    # ---------------------------------------------------------
    # WRITE DATA DICTIONARY
    # ---------------------------------------------------------

    with open(
        dictionary_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        fieldnames = [
            "column",
            "data_type",
            "description",
            "missing_pct",
            "unique_values",
            "governance_flag",
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for profile in profiles:

            description = (
                f"Detected "
                f"{profile['data_type'].lower()} field "
                f"with {profile['records']} records"
            )

            writer.writerow(
                {
                    "column": profile["column"],
                    "data_type": profile["data_type"],
                    "description": description,
                    "missing_pct": profile["missing_pct"],
                    "unique_values": profile["unique_values"],
                    "governance_flag": profile["governance_flag"],
                }
            )

    # ---------------------------------------------------------
    # BUILD HTML TABLE
    # ---------------------------------------------------------

    html_rows = ""

    for profile in profiles:

        html_rows += f"""
        <tr>
            <td>{escape(str(profile['column']))}</td>
            <td>{escape(str(profile['data_type']))}</td>
            <td>{profile['records']}</td>
            <td>{profile['missing']}</td>
            <td>{profile['missing_pct']}%</td>
            <td>{profile['unique_values']}</td>
            <td>{escape(str(profile['governance_flag']))}</td>
        </tr>
        """

    # ---------------------------------------------------------
    # GENERATE HTML REPORT
    # ---------------------------------------------------------

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="utf-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>SchemaSense Data Quality Report</title>

<style>

body {{
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;

    background: #f7f8fa;
    color: #1f2937;
    margin: 0;
    padding: 40px;
}}

.container {{
    max-width: 1200px;
    margin: auto;
}}

.header {{
    margin-bottom: 30px;
}}

h1 {{
    margin-bottom: 8px;
    font-size: 32px;
}}

.subtitle {{
    color: #6b7280;
    font-size: 16px;
}}

.cards {{
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(190px, 1fr));

    gap: 16px;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    padding: 22px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    box-shadow:
        0 2px 8px rgba(0, 0, 0, 0.04);
}}

.card-title {{
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 8px;
}}

.card-value {{
    font-size: 28px;
    font-weight: 700;
}}

.section {{
    background: white;
    padding: 24px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    box-shadow:
        0 2px 8px rgba(0, 0, 0, 0.04);
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin-top: 10px;
}}

th,
td {{
    border-bottom: 1px solid #e5e7eb;
    padding: 12px;
    text-align: left;
    font-size: 14px;
}}

th {{
    background: #f3f4f6;
    font-weight: 600;
}}

tr:hover {{
    background: #f9fafb;
}}

.note {{
    margin-top: 22px;
    padding: 14px 16px;
    background: #f3f4f6;
    border-radius: 8px;
    color: #4b5563;
    font-size: 13px;
}}

.footer {{
    margin-top: 24px;
    color: #9ca3af;
    font-size: 12px;
}}

@media (max-width: 700px) {{

    body {{
        padding: 20px;
    }}

    h1 {{
        font-size: 26px;
    }}

    .section {{
        overflow-x: auto;
    }}

}}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <h1>
            SchemaSense — Automated Dataset Profile
        </h1>

        <div class="subtitle">
            Schema and data-quality assessment
            generated from the supplied dataset.
        </div>

    </div>

    <div class="cards">

        <div class="card">
            <div class="card-title">
                Records
            </div>

            <div class="card-value">
                {len(rows)}
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                Columns
            </div>

            <div class="card-value">
                {len(columns)}
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                Missing Cells
            </div>

            <div class="card-value">
                {missing_cells}
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                Completeness
            </div>

            <div class="card-value">
                {completeness:.2f}%
            </div>
        </div>

    </div>

    <div class="section">

        <h2>
            Schema & Governance Profile
        </h2>

        <table>

            <thead>

                <tr>
                    <th>Column</th>
                    <th>Detected Type</th>
                    <th>Records</th>
                    <th>Missing</th>
                    <th>Missing %</th>
                    <th>Unique Values</th>
                    <th>Governance Flag</th>
                </tr>

            </thead>

            <tbody>

                {html_rows}

            </tbody>

        </table>

        <div class="note">

            <strong>Note:</strong>
            Governance flags are heuristic indicators
            for analyst review; they are not legal classifications.

        </div>

    </div>

    <div class="footer">

        SchemaSense — Automated Dataset Profiling Utility

    </div>

</div>

</body>

</html>
"""

    # ---------------------------------------------------------
    # WRITE HTML REPORT
    # ---------------------------------------------------------

    report_file.write_text(
        html,
        encoding="utf-8"
    )

    # ---------------------------------------------------------
    # CONSOLE OUTPUT
    # ---------------------------------------------------------

    print()
    print("=== SCHEMASENSE — COMPLETE ===")
    print(f"Records: {len(rows)}")
    print(f"Columns: {len(columns)}")
    print(f"Missing cells: {missing_cells}")
    print(f"Completeness: {completeness:.2f}%")
    print()

    print("Generated:")

    print(f"  {profile_file}")
    print(f"  {dictionary_file}")
    print(f"  {report_file}")

    print()
    print("SchemaSense completed successfully.")


if __name__ == "__main__":
    main()
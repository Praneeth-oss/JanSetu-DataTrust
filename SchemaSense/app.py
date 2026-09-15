import csv
import re
from pathlib import Path
from collections import Counter

def detect_type(values):
    clean = [v.strip() for v in values if v.strip()]
    if not clean:
        return "Unknown"

    numeric = 0
    dates = 0

    for v in clean:
        try:
            float(v)
            numeric += 1
        except ValueError:
            pass

        if re.match(r"^\d{4}-\d{2}-\d{2}$", v):
            dates += 1

    if numeric / len(clean) >= 0.95:
        return "Numeric"
    if dates / len(clean) >= 0.95:
        return "Date"

    unique_ratio = len(set(clean)) / len(clean)
    if unique_ratio < 0.20:
        return "Categorical"
    return "Text"

def sensitive_flag(column):
    name = column.lower()
    if any(x in name for x in ["email", "phone", "mobile", "address", "name"]):
        return "Potential Personal Data"
    if any(x in name for x in ["income", "salary", "financial"]):
        return "Potential Financial Data"
    return "No obvious flag"

def main():
    root = Path(__file__).resolve().parent
    input_file = root / "sample_data.csv"
    profile_file = root / "schema_profile.csv"
    dictionary_file = root / "data_dictionary.csv"
    report_file = root / "schemasense_report.html"

    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames

    profiles = []

    for column in columns:
        values = [row.get(column, "") for row in rows]
        missing = sum(1 for v in values if not v.strip())
        non_missing = [v for v in values if v.strip()]
        unique = len(set(non_missing))
        duplicates = len(non_missing) - unique

        profiles.append({
            "column": column,
            "data_type": detect_type(values),
            "records": len(values),
            "missing": missing,
            "missing_pct": round((missing / len(values)) * 100, 2),
            "unique_values": unique,
            "duplicate_values": duplicates,
            "governance_flag": sensitive_flag(column)
        })

    total_cells = len(rows) * len(columns)
    missing_cells = sum(p["missing"] for p in profiles)
    completeness = ((total_cells - missing_cells) / total_cells) * 100

    with open(profile_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=profiles[0].keys())
        writer.writeheader()
        writer.writerows(profiles)

    with open(dictionary_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "column",
                "data_type",
                "description",
                "missing_pct",
                "unique_values",
                "governance_flag"
            ]
        )
        writer.writeheader()

        for p in profiles:
            description = (
                f"Detected {p['data_type'].lower()} field "
                f"with {p['records']} records"
            )

            writer.writerow({
                "column": p["column"],
                "data_type": p["data_type"],
                "description": description,
                "missing_pct": p["missing_pct"],
                "unique_values": p["unique_values"],
                "governance_flag": p["governance_flag"]
            })

    html_rows = ""

    for p in profiles:
        html_rows += f"""
        <tr>
            <td>{p['column']}</td>
            <td>{p['data_type']}</td>
            <td>{p['records']}</td>
            <td>{p['missing']}</td>
            <td>{p['missing_pct']}%</td>
            <td>{p['unique_values']}</td>
            <td>{p['governance_flag']}</td>
        </tr>
        """

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SchemaSense Data Quality Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; }}
h1 {{ margin-bottom: 5px; }}
.card {{ display: inline-block; padding: 18px; margin: 8px;
         border: 1px solid #ddd; border-radius: 8px; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 25px; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f2f2f2; }}
</style>
</head>
<body>
<h1>SchemaSense — Automated Dataset Profile</h1>
<p>Schema and data-quality assessment generated from the supplied dataset.</p>

<div class="card"><b>Records</b><br>{len(rows)}</div>
<div class="card"><b>Columns</b><br>{len(columns)}</div>
<div class="card"><b>Missing Cells</b><br>{missing_cells}</div>
<div class="card"><b>Completeness</b><br>{completeness:.2f}%</div>

<table>
<tr>
<th>Column</th>
<th>Detected Type</th>
<th>Records</th>
<th>Missing</th>
<th>Missing %</th>
<th>Unique Values</th>
<th>Governance Flag</th>
</tr>
{html_rows}
</table>

<p>
<b>Note:</b> Governance flags are heuristic indicators for analyst review;
they are not legal classifications.
</p>
</body>
</html>
"""

    report_file.write_text(html, encoding="utf-8")

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


from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_FILE = PROJECT_ROOT / "data" / "jansetu.db"
SQL_FILE = PROJECT_ROOT / "sql" / "analytics.sql"


def run_query(connection, query):
    cursor = connection.execute(query)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    return columns, rows


def print_results(title, columns, rows, limit=None):
    print(f"\n=== {title} ===")

    display_rows = rows if limit is None else rows[:limit]

    print(" | ".join(columns))
    print("-" * 70)

    for row in display_rows:
        print(" | ".join(str(value) for value in row))

    if limit is not None and len(rows) > limit:
        print(f"... showing first {limit} of {len(rows)} rows")


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    sql_text = SQL_FILE.read_text(encoding="utf-8")

    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    titles = [
        "Records by State",
        "Records by Department",
        "Average Income by State",
        "Service Requests by Department",
        "High Service-Request Records",
        "Missing-Value Summary",
    ]

    for index, query in enumerate(queries):
        columns, rows = run_query(connection, query)

        limit = 10 if index == 4 else None

        print_results(
            titles[index],
            columns,
            rows,
            limit=limit,
        )

    connection.close()


if __name__ == "__main__":
    main()
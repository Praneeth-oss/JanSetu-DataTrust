from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_public_service_records.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "docs"
    / "data_dictionary.csv"
)


def build_data_dictionary(df: pd.DataFrame) -> pd.DataFrame:

    rows = []

    for column in df.columns:

        series = df[column]

        missing_count = int(
            series.isna().sum()
        )

        non_null = series.dropna()

        example_value = (
            str(non_null.iloc[0])
            if len(non_null) > 0
            else ""
        )

        rows.append(
            {
                "column_name": column,
                "data_type": str(series.dtype),
                "record_count": len(series),
                "missing_count": missing_count,
                "missing_percentage": round(
                    (missing_count / len(series)) * 100,
                    2,
                ),
                "unique_values": int(
                    series.nunique(dropna=True)
                ),
                "example_value": example_value,
            }
        )

    return pd.DataFrame(rows)


def main():

    df = pd.read_csv(
        INPUT_FILE,
        dtype={
            "email": "string",
            "phone": "string",
        },
    )

    dictionary = build_data_dictionary(df)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dictionary.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n=== JANSETU DATA DICTIONARY ===")
    print(
        f"Columns documented: "
        f"{len(dictionary)}"
    )
    print(
        f"Output: {OUTPUT_FILE}"
    )

    print("\nDictionary preview:")
    print(
        dictionary.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()
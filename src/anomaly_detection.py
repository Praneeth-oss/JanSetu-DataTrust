from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cleaned_public_service_records.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "anomaly_review.csv"
)


def main():
    df = pd.read_csv(INPUT_FILE)

    features = [
        "age",
        "annual_income",
        "service_requests",
    ]

    X = df[features]

    # Fill missing numeric values using the median.
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)

    # Put features on comparable scales.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Identify statistically unusual records.
    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42,
    )

    predictions = model.fit_predict(X_scaled)
    anomaly_scores = model.decision_function(X_scaled)

    result = df.copy()

    result["anomaly_flag"] = predictions == -1
    result["anomaly_score"] = anomaly_scores.round(4)

    review = (
        result[result["anomaly_flag"]]
        .sort_values("anomaly_score")
        .copy()
    )

    review.to_csv(OUTPUT_FILE, index=False)

    print("\n=== JANSETU ANOMALY DETECTION ===")
    print(f"Records analysed: {len(result)}")
    print(f"Records flagged for review: {len(review)}")
    print(f"Review file: {OUTPUT_FILE}")

    print("\nTop records for analyst review:")

    print(
        review[
            [
                "record_id",
                "age",
                "annual_income",
                "service_requests",
                "anomaly_score",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
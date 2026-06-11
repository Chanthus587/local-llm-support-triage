from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report


DATA_PATH = Path("data/sample_tickets.csv")
MODEL_PATH = Path("artifacts/baseline_ticket_classifier.joblib")


def main() -> None:
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)
    text = df["subject"].fillna("") + " " + df["body"].fillna("")
    predictions = model.predict(text)
    print(classification_report(df["category"], predictions))


if __name__ == "__main__":
    main()

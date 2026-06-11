from pathlib import Path

import joblib
import mlflow
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from support_triage.core.config import settings


DATA_PATH = Path("data/sample_tickets.csv")
ARTIFACT_PATH = Path("artifacts/baseline_ticket_classifier.joblib")


def main() -> None:
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment("ticket-category-baseline")

    df = pd.read_csv(DATA_PATH)
    df["text"] = df["subject"].fillna("") + " " + df["body"].fillna("")

    train_df, test_df = train_test_split(
        df,
        test_size=0.4,
        random_state=42,
        stratify=df["category"],
    )

    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    with mlflow.start_run():
        model.fit(train_df["text"], train_df["category"])
        predictions = model.predict(test_df["text"])

        accuracy = accuracy_score(test_df["category"], predictions)
        macro_f1 = f1_score(test_df["category"], predictions, average="macro")

        mlflow.log_param("model_type", "tfidf_logistic_regression")
        mlflow.log_param("training_rows", len(train_df))
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("macro_f1", macro_f1)

        ARTIFACT_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, ARTIFACT_PATH)
        mlflow.log_artifact(str(ARTIFACT_PATH))

    print(f"Saved baseline model to {ARTIFACT_PATH}")
    print(f"accuracy={accuracy:.3f} macro_f1={macro_f1:.3f}")


if __name__ == "__main__":
    main()

import os
import json
import pickle
import pandas as pd

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score


# =====================================
# Paths
# =====================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "mental_health",
    "balanced_stress_dataset.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "models", "mental_health")
os.makedirs(MODEL_DIR, exist_ok=True)


# =====================================
# Load Dataset
# =====================================
df = pd.read_csv(DATA_PATH)

print("Dataset Loaded:", df.shape)


# =====================================
# Text Cleaning
# =====================================
df = df.dropna(subset=["text"])
df["text"] = df["text"].astype(str)
df["text"] = df["text"].str.strip()
df = df[df["text"] != ""]

print("After Cleaning:", df.shape)


# =====================================
# Features & Labels
# =====================================
X = df["text"]
y = df["label"]


# =====================================
# Train/Test Split
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =====================================
# NLP Pipeline
# =====================================
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words="english",
        lowercase=True
    )),
    ("clf", LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        solver="lbfgs"
    ))
])


# =====================================
# Train Model
# =====================================
print("\nTraining model...")
pipeline.fit(X_train, y_train)


# =====================================
# Evaluation
# =====================================
y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

print("\n============================")
print("MODEL PERFORMANCE")
print("============================")
print("Accuracy:", round(accuracy, 4))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# =====================================
# Save Versioned Model
# =====================================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
model_filename = f"stress_model_{timestamp}.pkl"
MODEL_PATH = os.path.join(MODEL_DIR, model_filename)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(pipeline, f)

print("\n✅ Model saved at:")
print(MODEL_PATH)


# =====================================
# Save Metrics
# =====================================
metrics_path = os.path.join(MODEL_DIR, "metrics.json")

with open(metrics_path, "w") as f:
    json.dump({
        "accuracy": accuracy,
        "report": report,
        "model_version": model_filename
    }, f, indent=4)

print("\n📊 Metrics saved at:")
print(metrics_path)

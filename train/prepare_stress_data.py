import os
import pandas as pd
from data_utils import clean_text, normalize_label

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_PATH = os.path.join(PROJECT_ROOT, "data", "mental_health")

print("Loading datasets...")

# -----------------------------
# Load Dataset 1
# -----------------------------
df1 = pd.read_csv(os.path.join(DATA_PATH, "mental_health_text_classification.csv"))
print("Dataset 1 Columns:", df1.columns)

df1 = df1.rename(columns={
    "statement": "text",
    "status": "label"
})

df1 = df1[["text", "label"]]

# -----------------------------
# Load Dataset 2
# -----------------------------
df2 = pd.read_csv(os.path.join(DATA_PATH, "sentiment_analysis_mental_health.csv"))
print("Dataset 2 Columns:", df2.columns)

df2 = df2.rename(columns={
    "statement": "text",
    "status": "label"
})

df2 = df2[["text", "label"]]

# -----------------------------
# Load Dataset 3 (Excel)
# -----------------------------
df3 = pd.read_excel(os.path.join(DATA_PATH, "student_depression_text.xlsx"))
print("Dataset 3 Columns:", df3.columns)

df3 = df3[["text", "label"]]

# -----------------------------
# Merge Datasets
# -----------------------------
df = pd.concat([df1, df2, df3], ignore_index=True)

print("\nCombined Shape:", df.shape)

# -----------------------------
# Clean Data
# -----------------------------
df.dropna(subset=["text"], inplace=True)
df["text"] = df["text"].apply(clean_text)
df["label"] = df["label"].apply(normalize_label)

df = df[df["text"].str.len() > 5]

print("\nAfter Cleaning:", df.shape)

# -----------------------------
# Save Final Dataset
# -----------------------------
final_path = os.path.join(DATA_PATH, "final_stress_dataset.csv")
df.to_csv(final_path, index=False)

print("\nClass Distribution:")
print(df["label"].value_counts())

print("\nFinal dataset saved at:", final_path)

# -----------------------------
# Balance Dataset
# -----------------------------
min_count = df["label"].value_counts().min()

balanced_df = df.groupby("label").sample(min_count, random_state=42)

balanced_path = os.path.join(DATA_PATH, "balanced_stress_dataset.csv")
balanced_df.to_csv(balanced_path, index=False)

print("\nBalanced Distribution:")
print(balanced_df["label"].value_counts())

print("\nBalanced dataset saved at:", balanced_path)

import re
import pandas as pd


# -----------------------------
# Clean Text
# -----------------------------
def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Normalize Label
# -----------------------------
def normalize_label(label):
    """
    Map various dataset labels into:
    0 = Low
    1 = Moderate
    2 = High
    """

    label = str(label).lower()

    if label in ["0", "low", "normal", "no stress"]:
        return 0

    elif label in ["1", "moderate", "medium"]:
        return 1

    else:
        return 2

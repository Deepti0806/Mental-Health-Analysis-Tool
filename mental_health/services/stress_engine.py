import os
import pickle
import glob
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

MODEL_DIR = os.path.join(BASE_DIR, "models", "mental_health")

# -------------------------------------------------
# Global Model Cache (Lazy Load)
# -------------------------------------------------
_model = None


# -------------------------------------------------
# Text Preprocessing
# -------------------------------------------------
def clean_text(text: str) -> str:
    import re

    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -------------------------------------------------
# Load Latest Model (Only Once)
# -------------------------------------------------
def load_latest_model():
    global _model

    if _model is not None:
        return _model

    model_files = glob.glob(os.path.join(MODEL_DIR, "stress_model_*.pkl"))

    if not model_files:
        raise FileNotFoundError(
            f"No trained stress model found in {MODEL_DIR}"
        )

    latest_model = max(model_files, key=os.path.getctime)

    logger.info(f"Loading model: {os.path.basename(latest_model)}")

    with open(latest_model, "rb") as f:
        _model = pickle.load(f)

    return _model


# -------------------------------------------------
# Stress Prediction
# -------------------------------------------------
def predict_stress(text: str) -> Tuple[str, float]:
    model = load_latest_model()

    # Clean input text
    processed_text = clean_text(text)

    prediction = model.predict([processed_text])[0]
    probabilities = model.predict_proba([processed_text])[0]

    confidence = round(max(probabilities) * 100, 2)

    label_map = {
        0: "Low",
        1: "Moderate",
        2: "High"
    }

    level = label_map.get(prediction, "Unknown")

    logger.info(f"Prediction: {level} ({confidence}%)")

    return level, confidence

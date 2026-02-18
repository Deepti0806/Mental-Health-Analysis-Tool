import os
import pickle
from datetime import datetime


def save_model(model, model_dir, model_name="stress_model"):
    """
    Save model with versioning
    """
    os.makedirs(model_dir, exist_ok=True)

    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{model_name}_{version}.pkl"

    path = os.path.join(model_dir, file_name)

    with open(path, "wb") as f:
        pickle.dump(model, f)

    print(f"\nModel saved at: {path}")

    return path

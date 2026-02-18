import json
import os
from sklearn.metrics import accuracy_score, classification_report


def evaluate_model(model, X_test, y_test, model_dir):

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)

    print("\n======================")
    print("MODEL PERFORMANCE")
    print("======================")
    print("Accuracy:", round(accuracy, 4))
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    # Save metrics
    metrics_path = os.path.join(model_dir, "metrics.json")

    with open(metrics_path, "w") as f:
        json.dump({
            "accuracy": accuracy,
            "report": report
        }, f, indent=4)

    print("\nMetrics saved at:", metrics_path)

    return accuracy

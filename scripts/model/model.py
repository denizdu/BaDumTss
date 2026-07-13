import os
import json
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from label_validation import validate_training_labels

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Prepare the data.
def prepare_data(data, verified_labels):
    features = []
    labels = []

    for file_path, analysis in data.items():
        # Select a subset of the core features.
        main_features = analysis["Main Features"]
        tempo = main_features.get("Tempo (BPM)", 0)
        loudness = main_features.get("Loudness (dB)", 0)
        dynamics = main_features.get("Dynamics", 0)

        # Calculate the mean of the frequency spectrum.
        spectrum = analysis["Frequency and Spectrum"].get("Frequency Spectrum", [])
        spectrum_mean = sum(spectrum) / len(spectrum) if spectrum else 0

        label = verified_labels.get(file_path)
        if not isinstance(label, str) or not label.strip():
            continue
        label = label.strip()

        features.append([tempo, loudness, dynamics, spectrum_mean])
        labels.append(label)

    return pd.DataFrame(features, columns=["Tempo", "Loudness", "Dynamics", "Spectrum Mean"]), labels

def load_training_inputs(analysis_dir):
    analysis_dir = Path(analysis_dir)
    with (analysis_dir / "analysis_output.json").open(encoding="utf-8") as file:
        data = json.load(file)
    with (analysis_dir / "drum_kit_labels.json").open(encoding="utf-8") as file:
        verified_labels = json.load(file)
    return data, verified_labels


def train_model(data, verified_labels):
    features, labels = prepare_data(data, verified_labels)
    validate_training_labels(labels)
    test_size = max(len(set(labels)), round(len(labels) * 0.2))
    training_features, test_features, training_labels, test_labels = train_test_split(
        features,
        labels,
        test_size=test_size,
        random_state=42,
        stratify=labels,
    )
    model = RandomForestClassifier(random_state=42)
    model.fit(training_features, training_labels)
    predictions = model.predict(test_features)
    report = classification_report(test_labels, predictions, zero_division=0)
    return model, report


def run_training(analysis_dir, model_dir):
    data, verified_labels = load_training_inputs(analysis_dir)
    model, report = train_model(data, verified_labels)
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    output_file = model_dir / "drum_kit_recommendation_model.pkl"
    joblib.dump(model, output_file)
    print("Classification Report:")
    print(report)
    print("Model trained and saved successfully.")
    return output_file


def required_environment_path(variable_name):
    value = os.getenv(variable_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {variable_name}")
    path = Path(value).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    run_training(
        required_environment_path("DIR_OUTPUT_ANALYSIS"),
        required_environment_path("DIR_OUTPUT_MODEL"),
    )


if __name__ == "__main__":
    main()

import os
import json
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from label_validation import validate_training_labels

# Load environment variables.
load_dotenv()

# Directories.
DIR_OUTPUT_ANALYSIS = os.getenv("DIR_OUTPUT_ANALYSIS")
DIR_OUTPUT_MODEL = os.getenv("DIR_OUTPUT_MODEL")

input_data_file = os.path.join(DIR_OUTPUT_ANALYSIS, "analysis_output.json")
input_labels_file = os.path.join(DIR_OUTPUT_ANALYSIS, "drum_kit_labels.json")
output_file = os.path.join(DIR_OUTPUT_MODEL, "drum_kit_recommendation_model.pkl")

# Create the analysis directory.
os.makedirs(DIR_OUTPUT_ANALYSIS, exist_ok=True)

# Load data.
with open(input_data_file, 'r') as file:
    data = json.load(file)
with open(input_labels_file, 'r') as file:
    verified_labels = json.load(file)

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

# Process the data.
X, y = prepare_data(data, verified_labels)
validate_training_labels(y)

# Split the dataset into training and test sets.
test_size = max(len(set(y)), round(len(y) * 0.2))
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42, stratify=y
)

# Train the model.
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model.
y_pred = model.predict(X_test)

# Print the results.
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model.
import joblib
joblib.dump(model, output_file)

print("Model trained and saved successfully.")

import os
import json
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load environment variables.
load_dotenv()

# Directories.
DIR_OUTPUT_ANALYSIS = os.getenv("DIR_OUTPUT_ANALYSIS")
DIR_OUTPUT_MODEL = os.getenv("DIR_OUTPUT_MODEL")

input_data_file = os.path.join(DIR_OUTPUT_ANALYSIS, "analysis_output.json")
output_file = os.path.join(DIR_OUTPUT_MODEL, "drum_kit_recommendation_model.pkl")

# Create the analysis directory.
os.makedirs(DIR_OUTPUT_ANALYSIS, exist_ok=True)

# Load data.
with open(input_data_file, 'r') as file:
    data = json.load(file)

# Prepare the data.
def prepare_data(data):
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

        # Add a placeholder drum-kit label (for example, "Rock" or "Hip-Hop").
        # Production training data must provide verified labels instead.
        label = "Rock" if tempo > 120 else "Jazz"  # Placeholder only.

        features.append([tempo, loudness, dynamics, spectrum_mean])
        labels.append(label)

    return pd.DataFrame(features, columns=["Tempo", "Loudness", "Dynamics", "Spectrum Mean"]), labels

# Process the data.
X, y = prepare_data(data)

# Split the dataset into training and test sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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

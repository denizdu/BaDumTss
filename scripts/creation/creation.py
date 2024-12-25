import json
import os
import subprocess
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Dizinler
DIR_OUTPUT_MODEL = os.getenv("DIR_OUTPUT_MODEL")

def load_model_output(file_path):
    """Load the JSON file containing analysis data."""
    with open(file_path, 'r') as f:
        return json.load(f)

def call_script(script_name, *args):
    """Call another script in the same directory."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    subprocess.run(["python", script_path, *args])

def process_reaper(model_data):
    """Generate a Reaper project based on model data."""
    # Example: Retrieve tempo and key from model data
    tempo = model_data["Main Features"].get("Tempo (BPM)", 120)
    key = model_data["Main Features"].get("Key (Tonalite)", "C")

    print(f"Setting up Reaper project with Tempo: {tempo} BPM and Key: {key}")

    # TODO: Add more Reaper automation here, such as track creation or MIDI mapping

def main():
    # Define the path to the model output JSON
    model_output_path = os.path.join(DIR_OUTPUT_MODEL, f"model_output.json")

    # Load the analysis data
    model_data = load_model_output(model_output_path)

    # Process the Reaper project setup
    for track, track_data in model_data.items():
        print(f"Processing track: {track}")
        process_reaper(track_data)

    # Example: Call other scripts if needed
    # call_script("other_script.py", "arg1", "arg2")

if __name__ == "__main__":
    main()

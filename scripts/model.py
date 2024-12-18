import json
import os
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Directory containing the exported playlist files
playlists_directory = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/export"

# Function to load and process playlist files
def load_playlists(directory):
    all_tracks = []
    for filename in os.listdir(directory):
        if filename.endswith("_tracks.json"):
            filepath = os.path.join(directory, filename)
            print(f"Loading file: {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f:
                tracks = json.load(f)
                for track in tracks:
                    # Debugging: Print track to check available keys
                    print(f"Track: {track}")
                    if 'tempo' in track and 'energy' in track and 'danceability' in track:
                        all_tracks.append([track['tempo'], track['energy'], track['danceability'], random.choice([0, 1])])
                    else:
                        print(f"Missing features in track: {track}")
    return all_tracks

# Load all tracks from the playlist files
tracks = load_playlists(playlists_directory)
print(f"Loaded {len(tracks)} tracks from playlists.")

# Check if tracks are loaded
if len(tracks) == 0:
    print("No tracks were loaded. Please ensure the JSON files contain 'tempo', 'energy', and 'danceability' features.")
else:
    # Prepare data for training
    X = [row[:-1] for row in tracks]
    y = [row[-1] for row in tracks]

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

    # Generate new beat suggestions
    new_beat = [[130, 0.7, 0.6]]  # Tempo, energy, danceability
    print("Beğenme olasılığı:", model.predict(new_beat))

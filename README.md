# README for Spotify to Reaper Workflow

This workflow processes Spotify playlist data and generates track combinations in REAPER using several scripts. Below is a detailed guide on the functionality and usage of each script.

---

## Prerequisites

1. **Python Environment**:
   - Python 3.8 or above.
   - Required Python libraries:
     - `requests`
     - `json`
     - `librosa`
     - `mutagen`
     - `re`
     - `os`
     - `subprocess`
   - Install dependencies using:
     ```bash
     pip install requests librosa mutagen
     ```

2. **JSONLint**:
   - Install JSONLint using npm:
     ```bash
     npm install -g jsonlint
     ```
   - Ensure `jsonlint` is in the system PATH.

3. **Reaper**:
   - Reaper must be installed for Lua scripts to function.

---

## Workflow Steps

### 1. Fetch Spotify Data
**Script**: `spotify_fetch.py`

This script retrieves playlist data from Spotify and saves it in a JSON format for further processing.

#### Usage:
```bash
python spotify_fetch.py
```
- **Input**: Spotify API credentials in the script.
- **Output**: `spotify_tracks.json` in the output directory.

#### Notes:
- Ensure Spotify API credentials are correctly configured.
- Modify the script to target specific playlists or user data if needed.

### 2. Analyze Tracks
**Script**: `track_analysis.py`

This script downloads, cleans, and analyzes tracks for tempo, energy, chroma mean, and other features using Librosa.

#### Usage:
```bash
python track_analysis.py
```
- **Input**: `spotify_tracks.json` (output from Step 1).
- **Output**:
  - `cleaned_tracks.json` (analyzed data).
  - `removed_tracks.json` (failed tracks).

#### Notes:
- Temporary files are stored in the system's temp directory.
- Tracks with missing or invalid data are moved to `removed_tracks.json`.

### 3. Generate Track Combinations
**Script**: `track_combinations.py`

This script processes the cleaned track data and generates combinations of features like tempo and energy.

#### Usage:
```bash
python track_combinations.py
```
- **Input**: `cleaned_tracks.json` (output from Step 2).
- **Output**: `track_combinations.json`.

### 4. Clean JSON Files
**Script**: `clean_json.py`

This script validates and cleans JSON files, ensuring they are properly formatted for further processing.

#### Usage:
```bash
python clean_json.py <input_file> <output_file>
```
- **Input**: `track_combinations.json` (output from Step 3).
- **Output**: `cleaned_track_combinations.json`.

#### Notes:
- If JSONLint is installed, the script validates the output JSON.

### 5. Create Tracks in Reaper
**Script**: `track_combinations.lua`

This Lua script reads the cleaned JSON data and creates corresponding tracks in Reaper.

#### Usage:
1. Copy the `track_combinations.lua` file to your REAPER Scripts directory.
2. Run the script from REAPER's Actions List.

- **Input**: `cleaned_track_combinations.json` (output from Step 4).
- **Output**: Tracks created in REAPER.

#### Notes:
- Ensure `cleaned_track_combinations.json` is correctly formatted.
- Debugging can be done by checking REAPER’s console output.

---

## Debugging and Tips

1. **General Troubleshooting**:
   - Ensure all input/output file paths are correct.
   - Validate JSON files manually using `jsonlint`:
     ```bash
     jsonlint <file_path>
     ```

2. **Spotify API**:
   - Check Spotify API rate limits.
   - Ensure the correct scopes are set in the Spotify developer dashboard.

3. **Reaper Lua Scripts**:
   - Check for Lua script errors in REAPER’s console.
   - Ensure the JSON parser in Lua is working with simplified JSON formats.

4. **File Paths**:
   - Use absolute paths to avoid file not found errors.
   - Ensure temp files are cleaned up after each script.

---

## Directory Structure
```
BaDumTss/
├── output/
│   ├── spotify_tracks.json
│   ├── cleaned/
│   │   ├── cleaned_tracks.json
│   │   ├── removed_tracks.json
│   ├── analysis/
│   │   ├── track_combinations.json
│   │   ├── cleaned_track_combinations.json
├── scripts/
│   ├── spotify_fetch.py
│   ├── track_analysis.py
│   ├── track_combinations.py
│   ├── clean_json.py
│   ├── track_combinations.lua
```

---

## Dependencies
- Python 3.8+
- Node.js (for JSONLint)
- REAPER (with Lua scripting enabled)

---

## Future Improvements
- Automate the entire pipeline with a master script.
- Enhance error logging and reporting.
- Introduce a GUI for user-friendly interaction.

---

For further assistance, contact the developer or refer to the documentation of the respective tools.


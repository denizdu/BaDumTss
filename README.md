# BaDumTss

BaDumTss is an experimental music-analysis and beat-reconstruction pipeline. It can collect playlist metadata, fetch authorized audio, extract musical features, classify drum transients, and generate MIDI data for later use in REAPER.

## Project structure

- `scripts/fetch/`: Spotify metadata and audio-fetching utilities.
- `scripts/analysis/`: tempo, key, rhythm, spectral, and drum analysis.
- `scripts/creation/`: MIDI and REAPER project-generation experiments.
- `scripts/model/`: early recommendation-model experiments.
- `tests/`: regression and unit tests.
- `doc/`: design notes and technical background.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Create a local `.env` file. Never commit credentials or browser cookies.

```dotenv
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
DIR_DOWNLOAD=downloads
DIR_OUTPUT_FETCH=output/fetch
DIR_OUTPUT_ANALYSIS=output/analysis
DIR_OUTPUT_MODEL=output/model
DIR_OUTPUT_CREATION=output/creation
```

Audio assets are deliberately excluded from Git. Configure local drum samples
for REAPER with absolute paths in your shell environment:

```dotenv
BADUMTSS_KICK_SAMPLE=D:/audio-assets/kick.wav
BADUMTSS_SNARE_SAMPLE=D:/audio-assets/snare.wav
BADUMTSS_HIHAT_SAMPLE=D:/audio-assets/hihat.wav
```

See [`sample/README.md`](sample/README.md) for the asset policy and manifest
format. Reference songs and third-party sample packs must remain outside the
repository.

Run the test suite:

```bash
python -m pytest -q
```

Run the current analysis entry point:

```bash
python scripts/analysis/analysis.py
```

## Input and output

Playlist JSON files contain track and artist metadata. Audio, downloads, and
generated `output/` and `export/` directories are intentionally ignored by Git.
Analysis workers write isolated partial JSON files, and the parent process
merges them atomically into the final analysis output.

## Current status

The repository is under active development. Key estimation, frequency-based drum classification, single-load audio analysis, safe JSON merging, and basic Format 1 MIDI generation have regression tests. REAPER integration, stem separation, production-grade model training, and end-to-end orchestration remain experimental.

## Legal and security notes

Only fetch or process media you are authorized to use. Spotify credentials belong in `.env`; browser-cookie exports must never be committed. Spotify metadata does not provide downloadable full-track audio.

## Contributing

Create a focused branch, add tests for behavior changes, run the complete test suite, and open a pull request with a concise explanation of the change.

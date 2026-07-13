import os
import logging
import librosa
import hashlib
from dataclasses import dataclass
from pathlib import Path
from multiprocessing import Pool
from dotenv import load_dotenv
from scripts.fetch.audio_sources import resolve_audio_source
from derived_features import process_derived_features
from extra_features import process_extra_features
from freq_and_spectrum import process_freq_and_spectrum
from main_features import process_main_features
from rhythm import process_rhythm
from spectral_features import process_spectral_features
from drum_analysis import process_drum_analysis
from analysis_store import merge_analysis_files, read_json

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class AnalysisPipelineError(RuntimeError):
    """Raised when a track cannot complete the analysis pipeline."""


def required_project_path(variable_name, environment=None):
    environment = os.environ if environment is None else environment
    value = environment.get(variable_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {variable_name}")
    path = Path(value).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


@dataclass(frozen=True)
class AnalysisConfig:
    download_dir: Path
    fetch_output_dir: Path
    analysis_output_dir: Path
    playlists: tuple[str, ...]

    @property
    def output_file(self):
        return self.analysis_output_dir / "analysis_output.json"

    @property
    def partial_output_dir(self):
        return self.analysis_output_dir / ".partial"


def load_analysis_config(environment=None):
    """Build validated configuration without mutating the filesystem."""
    environment = os.environ if environment is None else environment
    playlist_setting = environment.get("PLAYLIST_TOBE_ANALYZED")
    if not playlist_setting:
        raise RuntimeError(
            "Missing required environment variable: PLAYLIST_TOBE_ANALYZED"
        )
    playlists = tuple(name.strip() for name in playlist_setting.split(",") if name.strip())
    if not playlists:
        raise RuntimeError("PLAYLIST_TOBE_ANALYZED must contain at least one playlist")
    return AnalysisConfig(
        download_dir=required_project_path("DIR_DOWNLOAD", environment),
        fetch_output_dir=required_project_path("DIR_OUTPUT_FETCH", environment),
        analysis_output_dir=required_project_path("DIR_OUTPUT_ANALYSIS", environment),
        playlists=playlists,
    )

# Analyze a song and remove the downloaded file afterward
def analyze_and_delete_song(song_file, song_output_file, delete_after_analysis=True):
    try:
        print(f"Analyzing: {song_file}")
        # Load the audio only once and share it across all analysis modules.
        y, sr = librosa.load(song_file, sr=None)
        process_main_features(song_file, song_output_file, y=y, sr=sr)
        process_freq_and_spectrum(song_file, song_output_file, y=y, sr=sr)
        process_rhythm(song_file, song_output_file, y=y, sr=sr)
        process_spectral_features(song_file, song_output_file, y=y, sr=sr)
        process_extra_features(song_file, song_output_file, y=y, sr=sr)
        process_drum_analysis(song_file, song_output_file, y=y, sr=sr)

        print(f"Analysis completed for: {song_file}")
        return song_output_file
    except Exception as error:
        logging.exception("Analysis failed for %s", song_file)
        raise AnalysisPipelineError(f"Analysis failed for {song_file}") from error
    finally:
        if delete_after_analysis and os.path.exists(song_file):
            os.remove(song_file)
            print(f"Deleted: {song_file}")

def process_track(track, config):
    search_query = f"{track['name']} {track['artist']}"
    print(f"Processing song: {track['name']} by {track['artist']}")

    try:
        audio = resolve_audio_source(track, config.download_dir)
        song_file = str(audio.path)
        print(f"Resolved {track.get('audio_source', 'youtube')} audio: {song_file}")
    except (ValueError, FileNotFoundError) as error:
        logging.exception("Failed to resolve audio for %s", search_query)
        raise AnalysisPipelineError(
            f"Failed to resolve audio for {search_query}"
        ) from error

    if song_file and os.path.exists(song_file):
        os.makedirs(config.partial_output_dir, exist_ok=True)
        track_key = hashlib.sha256(search_query.encode("utf-8")).hexdigest()[:16]
        song_output_file = config.partial_output_dir / f"{track_key}.json"
        if os.path.exists(song_output_file):
            os.remove(song_output_file)
        return analyze_and_delete_song(
            song_file, str(song_output_file), audio.delete_after_analysis
        )
    raise AnalysisPipelineError(f"Resolved audio file does not exist: {song_file}")


def run_pipeline(config, worker_count=4):
    config.download_dir.mkdir(parents=True, exist_ok=True)
    config.analysis_output_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=config.analysis_output_dir / "errors.log",
        level=logging.ERROR,
        format="%(asctime)s - %(message)s",
    )
    for playlist_name in config.playlists:
        print(f"Starting analysis for playlist: {playlist_name}")

        # Validate the playlist file.
        playlist_file = config.fetch_output_dir / f"{playlist_name}_tracks.json"
        if not os.path.exists(playlist_file):
            raise FileNotFoundError(f"Playlist file does not exist: {playlist_file}")

        tracks = read_json(playlist_file, expected_type=list)

        # Process songs in parallel.
        with Pool(processes=worker_count) as pool:
            partial_files = pool.starmap(
                process_track, ((track, config) for track in tracks)
            )

        # Only the parent process merges results; workers never write the same file.
        merge_analysis_files(partial_files, str(config.output_file))

        print(f"Analysis for playlist '{playlist_name}' completed.")


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    run_pipeline(load_analysis_config())


if __name__ == "__main__":
    main()

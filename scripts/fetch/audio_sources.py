from dataclasses import dataclass
from pathlib import Path

from scripts.fetch.youtube_fetch import download_song_as_wav


@dataclass(frozen=True)
class ResolvedAudio:
    path: Path
    delete_after_analysis: bool


def resolve_audio_source(track, download_dir, downloader=download_song_as_wav):
    """Resolve an explicit YouTube or local audio source for a metadata record."""
    source_type = str(track.get("audio_source", "youtube")).strip().lower()

    if source_type == "spotify":
        raise ValueError(
            "Spotify provides metadata, not downloadable full-track audio. "
            "Set audio_source to 'youtube' or 'local'."
        )

    if source_type == "local":
        reference = track.get("audio_reference") or track.get("path")
        if not reference:
            raise ValueError("Local audio requires audio_reference or path")
        local_path = Path(reference).expanduser().resolve()
        if not local_path.is_file():
            raise FileNotFoundError(f"Local audio file does not exist: {local_path}")
        return ResolvedAudio(path=local_path, delete_after_analysis=False)

    if source_type == "youtube":
        reference = track.get("audio_reference")
        if not reference:
            name = track.get("name")
            artist = track.get("artist")
            if not name or not artist:
                raise ValueError(
                    "YouTube audio requires audio_reference or both name and artist"
                )
            reference = f"{name} {artist}"

        downloaded_path = downloader(reference, download_dir)
        if not downloaded_path:
            raise FileNotFoundError(
                f"YouTube downloader did not return an audio file for: {reference}"
            )
        downloaded_path = Path(downloaded_path).resolve()
        if not downloaded_path.is_file():
            raise FileNotFoundError(
                f"YouTube downloader returned a missing file: {downloaded_path}"
            )
        return ResolvedAudio(path=downloaded_path, delete_after_analysis=True)

    raise ValueError(
        f"Unsupported audio_source '{source_type}'. Expected 'youtube' or 'local'."
    )

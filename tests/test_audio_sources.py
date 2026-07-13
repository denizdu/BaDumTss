from pathlib import Path
from unittest.mock import Mock

import pytest

from scripts.fetch.audio_sources import resolve_audio_source


def test_local_audio_is_preserved(tmp_path):
    local_file = tmp_path / "source.wav"
    local_file.write_bytes(b"audio")
    downloader = Mock()

    resolved = resolve_audio_source(
        {"audio_source": "local", "audio_reference": str(local_file)},
        tmp_path / "downloads",
        downloader=downloader,
    )

    assert resolved.path == local_file.resolve()
    assert resolved.delete_after_analysis is False
    downloader.assert_not_called()


def test_youtube_audio_is_marked_as_temporary(tmp_path):
    downloaded_file = tmp_path / "downloads" / "track.wav"
    downloaded_file.parent.mkdir()
    downloaded_file.write_bytes(b"audio")
    downloader = Mock(return_value=str(downloaded_file))

    resolved = resolve_audio_source(
        {
            "audio_source": "youtube",
            "audio_reference": "Artist Track official audio",
        },
        downloaded_file.parent,
        downloader=downloader,
    )

    assert resolved.path == downloaded_file.resolve()
    assert resolved.delete_after_analysis is True
    downloader.assert_called_once_with(
        "Artist Track official audio", downloaded_file.parent
    )


def test_legacy_metadata_defaults_to_a_youtube_search(tmp_path):
    downloaded_file = tmp_path / "legacy.wav"
    downloaded_file.write_bytes(b"audio")
    downloader = Mock(return_value=str(downloaded_file))

    resolve_audio_source(
        {"name": "Track", "artist": "Artist"},
        tmp_path,
        downloader=downloader,
    )

    downloader.assert_called_once_with("Track Artist", tmp_path)


def test_spotify_cannot_be_used_as_a_full_audio_source(tmp_path):
    with pytest.raises(ValueError, match="Spotify provides metadata"):
        resolve_audio_source(
            {"audio_source": "spotify", "audio_reference": "spotify:track:123"},
            tmp_path,
        )


@pytest.mark.parametrize(
    "track,expected_message",
    [
        ({"audio_source": "local"}, "Local audio requires"),
        ({"audio_source": "youtube"}, "YouTube audio requires"),
        ({"audio_source": "unknown"}, "Unsupported audio_source"),
    ],
)
def test_invalid_source_configuration_is_rejected(track, expected_message, tmp_path):
    with pytest.raises(ValueError, match=expected_message):
        resolve_audio_source(track, tmp_path)

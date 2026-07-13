import json

import pytest

from analysis_store import (
    AnalysisStoreError,
    atomic_write_json,
    merge_analysis_files,
    read_analysis,
    update_analysis_section,
)


def test_section_updates_preserve_existing_songs_and_sections(tmp_path):
    output = tmp_path / "analysis.json"
    atomic_write_json(
        output,
        {
            "existing.wav": {"Main Features": {"Tempo (BPM)": 100}},
            "song.wav": {"Rhythm": {"Beat Grid": [0.0]}},
        },
    )

    update_analysis_section(
        output,
        "song.wav",
        "Spectral Features",
        {"Spectral Centroid": 1500.0},
    )

    assert read_analysis(output) == {
        "existing.wav": {"Main Features": {"Tempo (BPM)": 100}},
        "song.wav": {
            "Rhythm": {"Beat Grid": [0.0]},
            "Spectral Features": {"Spectral Centroid": 1500.0},
        },
    }


def test_invalid_existing_json_is_not_overwritten(tmp_path):
    output = tmp_path / "analysis.json"
    output.write_text("{invalid", encoding="utf-8")

    with pytest.raises(AnalysisStoreError, match="Invalid JSON"):
        update_analysis_section(output, "song.wav", "Rhythm", {})

    assert output.read_text(encoding="utf-8") == "{invalid"


def test_non_object_analysis_root_is_rejected(tmp_path):
    output = tmp_path / "analysis.json"
    output.write_text(json.dumps([{"song": "invalid-root"}]), encoding="utf-8")

    with pytest.raises(AnalysisStoreError, match="Expected dict"):
        read_analysis(output)


def test_atomic_write_does_not_leave_temporary_files(tmp_path):
    output = tmp_path / "analysis.json"

    atomic_write_json(output, {"song.wav": {}})

    assert json.loads(output.read_text(encoding="utf-8")) == {"song.wav": {}}
    assert list(tmp_path.glob("*.tmp")) == []
    assert list(tmp_path.glob(".*.tmp")) == []


def test_merge_is_atomic_and_removes_only_completed_partial_files(tmp_path):
    destination = tmp_path / "analysis.json"
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    missing = tmp_path / "missing.json"
    atomic_write_json(destination, {"existing": {"value": 1}})
    atomic_write_json(first, {"song-a": {"tempo": 90}})
    atomic_write_json(second, {"song-b": {"tempo": 120}})

    merge_analysis_files([first, None, missing, second], destination)

    assert read_analysis(destination) == {
        "existing": {"value": 1},
        "song-a": {"tempo": 90},
        "song-b": {"tempo": 120},
    }
    assert not first.exists()
    assert not second.exists()

import json
import os
import tempfile
from pathlib import Path


class AnalysisStoreError(ValueError):
    """Raised when persisted analysis data violates the storage contract."""


def read_json(path, expected_type=None):
    """Read JSON and optionally validate its root type."""
    path = Path(path)
    try:
        with path.open(encoding="utf-8") as file:
            value = json.load(file)
    except json.JSONDecodeError as error:
        raise AnalysisStoreError(f"Invalid JSON in {path}: {error.msg}") from error

    if expected_type is not None and not isinstance(value, expected_type):
        raise AnalysisStoreError(
            f"Expected {expected_type.__name__} at the root of {path}, "
            f"got {type(value).__name__}"
        )
    return value


def read_analysis(path, missing_ok=False):
    """Read an analysis object, optionally treating a missing file as empty."""
    path = Path(path)
    if missing_ok and not path.exists():
        return {}
    return read_json(path, expected_type=dict)


def atomic_write_json(path, value):
    """Persist JSON through a flushed temporary file and atomic replacement."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(value, file, ensure_ascii=False, indent=4)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def update_analysis_section(output_file, song_file, section_name, results):
    """Replace one section of one song record and preserve all other data."""
    if not isinstance(song_file, str) or not song_file:
        raise AnalysisStoreError("song_file must be a non-empty string")
    if not isinstance(section_name, str) or not section_name:
        raise AnalysisStoreError("section_name must be a non-empty string")
    if not isinstance(results, dict):
        raise AnalysisStoreError("analysis section results must be an object")

    data = read_analysis(output_file, missing_ok=True)
    song_record = data.setdefault(song_file, {})
    if not isinstance(song_record, dict):
        raise AnalysisStoreError(f"Analysis record for {song_file} must be an object")
    song_record[section_name] = results
    atomic_write_json(output_file, data)


def merge_analysis_files(partial_files, destination):
    """Merge completed worker objects and remove them after an atomic write."""
    destination = Path(destination)
    merged_data = read_analysis(destination, missing_ok=True)
    completed_files = [
        Path(path) for path in partial_files if path and Path(path).is_file()
    ]
    for partial_file in completed_files:
        merged_data.update(read_analysis(partial_file))

    atomic_write_json(destination, merged_data)
    for partial_file in completed_files:
        partial_file.unlink()

from pathlib import Path

import pytest

from label_validation import validate_training_labels


MODEL_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "model" / "model.py"


def test_placeholder_tempo_labels_are_removed():
    script = MODEL_SCRIPT.read_text(encoding="utf-8")

    assert '"Rock" if tempo > 120 else "Jazz"' not in script
    assert "verified_labels.get(file_path)" in script
    assert "drum_kit_labels.json" in script


def test_training_rejects_an_empty_verified_dataset():
    with pytest.raises(ValueError, match="No verified drum-kit labels matched"):
        validate_training_labels([])


def test_training_requires_two_distinct_labels():
    with pytest.raises(ValueError, match="at least two distinct"):
        validate_training_labels(["Acoustic", "Acoustic"])


def test_training_requires_two_examples_per_label():
    with pytest.raises(ValueError, match="insufficient labels: Electronic"):
        validate_training_labels(["Acoustic", "Acoustic", "Electronic"])


def test_balanced_verified_labels_are_valid():
    validate_training_labels(
        ["Acoustic", "Acoustic", "Electronic", "Electronic"]
    )

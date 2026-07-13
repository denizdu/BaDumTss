import json
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_SCRIPT = PROJECT_ROOT / "scripts" / "model" / "model.py"


def test_model_script_trains_with_verified_labels(tmp_path):
    analysis_dir = tmp_path / "analysis"
    model_dir = tmp_path / "model"
    analysis_dir.mkdir()
    model_dir.mkdir()

    analysis = {}
    labels = {}
    for index in range(8):
        track_id = f"track-{index}"
        analysis[track_id] = {
            "Main Features": {
                "Tempo (BPM)": 90 + index * 8,
                "Loudness (dB)": -18 + index,
                "Dynamics": 0.1 + index / 100,
            },
            "Frequency and Spectrum": {
                "Frequency Spectrum": [float(index), float(index + 1)]
            },
        }
        labels[track_id] = "Acoustic" if index < 4 else "Electronic"

    (analysis_dir / "analysis_output.json").write_text(
        json.dumps(analysis), encoding="utf-8"
    )
    (analysis_dir / "drum_kit_labels.json").write_text(
        json.dumps(labels), encoding="utf-8"
    )

    environment = os.environ.copy()
    environment.update(
        {
            "DIR_OUTPUT_ANALYSIS": str(analysis_dir),
            "DIR_OUTPUT_MODEL": str(model_dir),
        }
    )
    result = subprocess.run(
        [sys.executable, str(MODEL_SCRIPT)],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Model trained and saved successfully." in result.stdout
    assert (model_dir / "drum_kit_recommendation_model.pkl").is_file()

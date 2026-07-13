import json

from midi_creation import main
import midi_creation


def test_main_creates_midi_from_analysis_json(tmp_path, monkeypatch):
    analysis_dir = tmp_path / "output" / "analysis"
    creation_dir = tmp_path / "output" / "creation"
    analysis_dir.mkdir(parents=True)
    creation_dir.mkdir(parents=True)
    analysis = {
        "song.wav": {
            "Drum Analysis": {
                "Tempo (BPM)": 120,
                "Kick Positions": [0.0, 1.0],
                "Snare Positions": [0.5],
                "HiHat Positions": [0.25, 0.75],
            }
        }
    }
    (analysis_dir / "analysis_output.json").write_text(
        json.dumps(analysis), encoding="utf-8"
    )
    monkeypatch.setattr(midi_creation, "PROJECT_ROOT", tmp_path)

    main()

    midi_file = creation_dir / "generated_drums.mid"
    assert midi_file.read_bytes().startswith(b"MThd")


def test_main_rejects_invalid_analysis_json(tmp_path, monkeypatch, capsys):
    analysis_dir = tmp_path / "output" / "analysis"
    analysis_dir.mkdir(parents=True)
    (analysis_dir / "analysis_output.json").write_text("{invalid", encoding="utf-8")
    monkeypatch.setattr(midi_creation, "PROJECT_ROOT", tmp_path)

    main()

    assert "Error: Invalid JSON format" in capsys.readouterr().out
    assert not (tmp_path / "output" / "creation" / "generated_drums.mid").exists()

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLING_SCRIPT = PROJECT_ROOT / "scripts" / "sampling" / "audio_beat_creater.lua"


def test_sampling_script_uses_a_portable_project_root():
    script = SAMPLING_SCRIPT.read_text(encoding="utf-8")

    assert "reaper.get_action_context()" in script
    assert 'get_project_root() .. "/output/analysis/' in script
    assert "C:/Users/" not in script
    assert "OneDrive" not in script


def test_sampling_script_keeps_json_and_reaper_operations_explicit():
    script = SAMPLING_SCRIPT.read_text(encoding="utf-8")

    assert "json.decode(content)" in script
    assert "if err then" in script
    assert "reaper.TrackFX_AddByName" in script
    assert "reaper.CreateNewMIDIItemInProj" in script
    assert "reaper.MIDI_InsertNote" in script

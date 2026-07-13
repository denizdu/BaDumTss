from pathlib import Path


CREATION_SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "creation" / "creation.lua"
)


def test_reaper_items_use_seconds_and_notes_use_converted_ppq_positions():
    script = CREATION_SCRIPT.read_text(encoding="utf-8")

    assert "CreateNewMIDIItemInProj(track, start_seconds, end_seconds" in script
    assert "MIDI_GetPPQPosFromProjTime(take, start_seconds)" in script
    assert "MIDI_GetPPQPosFromProjTime(take, end_seconds)" in script
    assert "MIDI_InsertNote(take, false, false, start_ppq, end_ppq" in script
    assert "CreateNewMIDIItemInProj(track, math.floor(start_position)" not in script


def test_melody_beat_positions_are_converted_to_project_seconds():
    script = CREATION_SCRIPT.read_text(encoding="utf-8")

    assert "local start_seconds = (i - 1) * 60.0 / tempo" in script
    assert "add_midi_note_to_track(track, note, start_seconds, 0.5, tempo)" in script

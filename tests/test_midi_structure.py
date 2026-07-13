import struct

from midi_creation import PPQ, create_midi_file


def test_format_one_header_matches_written_track_count(tmp_path):
    output = tmp_path / "drums.mid"
    create_midi_file(
        output,
        {
            "Tempo (BPM)": 120,
            "Kick Positions": [],
            "Snare Positions": [],
            "HiHat Positions": [],
        },
    )

    midi = output.read_bytes()
    header_length, midi_format, track_count, division = struct.unpack(">IHHH", midi[4:14])
    assert midi[:4] == b"MThd"
    assert (header_length, midi_format, track_count, division) == (6, 1, 4, PPQ)

    offset = 14
    for _ in range(track_count):
        assert midi[offset:offset + 4] == b"MTrk"
        track_length = struct.unpack(">I", midi[offset + 4:offset + 8])[0]
        offset += 8 + track_length
    assert offset == len(midi)


def test_tempo_track_contains_120_bpm_meta_event(tmp_path):
    output = tmp_path / "tempo.mid"
    create_midi_file(output, {"Tempo (BPM)": 120})

    midi = output.read_bytes()
    assert b"\xFF\x51\x03\x07\xA1\x20" in midi

from midi_creation import build_note_events


def decode_vlq(data, offset):
    value = 0
    while True:
        byte = data[offset]
        offset += 1
        value = (value << 7) | (byte & 0x7F)
        if byte & 0x80 == 0:
            return value, offset


def decode_note_events(data):
    events = []
    offset = 0
    absolute_tick = 0
    while offset < len(data):
        delta, offset = decode_vlq(data, offset)
        absolute_tick += delta
        status, pitch, velocity = data[offset:offset + 3]
        offset += 3
        events.append((absolute_tick, status, pitch, velocity))
    return events


def test_note_deltas_preserve_absolute_positions_after_note_off():
    encoded = build_note_events([0.0, 1.0], 36, 100, bpm=60, ppq=960)

    assert decode_note_events(encoded) == [
        (0, 0x90, 36, 100),
        (480, 0x80, 36, 0),
        (960, 0x90, 36, 100),
        (1440, 0x80, 36, 0),
    ]


def test_overlapping_notes_are_written_in_chronological_order():
    encoded = build_note_events([0.5, 0.0], 42, 90, bpm=120, ppq=960)

    assert decode_note_events(encoded) == [
        (0, 0x90, 42, 90),
        (480, 0x80, 42, 0),
        (960, 0x90, 42, 90),
        (1440, 0x80, 42, 0),
    ]


def test_note_off_precedes_note_on_at_the_same_tick():
    encoded = build_note_events([0.0, 0.5], 38, 100, bpm=60, ppq=960)

    assert decode_note_events(encoded)[1:3] == [
        (480, 0x80, 38, 0),
        (480, 0x90, 38, 100),
    ]

import json
import struct
import os
from pathlib import Path

PPQ = 960
DEFAULT_NOTE_DURATION = 480
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def seconds_to_ticks(seconds, bpm, ppq=PPQ):
    """Convert a position in seconds to MIDI PPQ ticks at the given tempo."""
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    if bpm <= 0:
        raise ValueError("bpm must be positive")
    if ppq <= 0:
        raise ValueError("ppq must be positive")
    beats = seconds * bpm / 60.0
    return int(round(beats * ppq))


def read_file(file_path):
    """Reads the content of a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def write_variable_length_quantity(value):
    """Encodes a value as a MIDI Variable Length Quantity (VLQ)."""
    vlq = bytearray()
    vlq.append(value & 0x7F)
    while value > 0x7F:
        value >>= 7
        vlq.insert(0, (value & 0x7F) | 0x80)
    return vlq

def write_midi_notes(midi_file, positions, pitch, velocity, bpm, ppq=PPQ):
    """Write chronologically ordered MIDI note events to a binary stream."""
    midi_file.write(build_note_events(positions, pitch, velocity, bpm, ppq))


def build_note_events(
    positions,
    pitch,
    velocity,
    bpm,
    ppq=PPQ,
    note_duration=DEFAULT_NOTE_DURATION,
):
    """Encode note events using deltas calculated from sorted absolute ticks."""
    if not 0 <= pitch <= 127:
        raise ValueError("pitch must be between 0 and 127")
    if not 0 <= velocity <= 127:
        raise ValueError("velocity must be between 0 and 127")
    if note_duration <= 0:
        raise ValueError("note_duration must be positive")

    events = []
    for position in positions:
        start_tick = seconds_to_ticks(position, bpm, ppq)
        events.append((start_tick, 1, 0x90, pitch, velocity))
        events.append((start_tick + note_duration, 0, 0x80, pitch, 0))

    encoded = bytearray()
    previous_tick = 0
    for absolute_tick, _, status, event_pitch, event_velocity in sorted(events):
        encoded.extend(write_variable_length_quantity(absolute_tick - previous_tick))
        encoded.extend(struct.pack("BBB", status, event_pitch, event_velocity))
        previous_tick = absolute_tick
    return encoded


def write_track_chunk(midi_file, track_data):
    """Write a standard MTrk chunk with an accurate payload length."""
    midi_file.write(b"MTrk")
    midi_file.write(struct.pack(">I", len(track_data)))
    midi_file.write(track_data)


def build_tempo_track(bpm):
    if bpm <= 0:
        raise ValueError("bpm must be positive")
    microseconds_per_beat = int(round(60_000_000 / bpm))
    if microseconds_per_beat > 0xFFFFFF:
        raise ValueError("bpm is outside the MIDI tempo range")
    return (
        b"\x00\xFF\x51\x03"
        + microseconds_per_beat.to_bytes(3, byteorder="big")
        + b"\x00\xFF\x2F\x00"
    )


def create_midi_file(output_path, drum_analysis):
    """Create a Format 1 MIDI file with tempo, kick, snare, and hi-hat tracks."""
    try:
        bpm = float(drum_analysis.get("Tempo (BPM)", 120.0))
        with open(output_path, 'wb') as midi_file:
            # Format 1: conductor/tempo + kick + snare + hi-hat = 4 tracks.
            midi_file.write(b"MThd")
            midi_file.write(struct.pack(">IHHH", 6, 1, 4, PPQ))
            write_track_chunk(midi_file, build_tempo_track(bpm))

            def write_track(positions, pitch, track_name):
                """Writes a single track with given positions and pitch."""
                track_data = bytearray()
                # Write track name meta-event
                track_data.extend(write_variable_length_quantity(0))
                track_data.extend(struct.pack("<BB", 0xFF, 0x03))
                track_data.extend(struct.pack("B", len(track_name)))
                track_data.extend(track_name.encode('ascii'))

                # Calculate deltas only after all absolute note events are sorted.
                track_data.extend(build_note_events(positions, pitch, 100, bpm))

                track_data.extend(b"\x00\xFF\x2F\x00")
                write_track_chunk(midi_file, track_data)

            # Write tracks for kick, snare, and hi-hat
            write_track(drum_analysis.get("Kick Positions", []), 36, "Kick")
            write_track(drum_analysis.get("Snare Positions", []), 38, "Snare")
            write_track(drum_analysis.get("HiHat Positions", []), 42, "HiHat")

        print(f"MIDI file with separate tracks successfully created at {output_path}")
    except IOError as e:
        print(f"Error: Unable to write MIDI file. {e}")

def main():
    midi_output_path = PROJECT_ROOT / "output" / "creation" / "generated_drums.mid"
    json_file = PROJECT_ROOT / "output" / "analysis" / "analysis_output.json"

    # Read JSON file
    json_content = read_file(json_file)
    if not json_content:
        return

    # Decode JSON content
    try:
        json_data = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. {e}")
        return

    # Extract data from JSON
    first_key = next(iter(json_data), None)
    if not first_key or "Drum Analysis" not in json_data.get(first_key, {}):
        print("Error: No drum analysis data found in JSON file.")
        return

    drum_analysis = json_data[first_key]["Drum Analysis"]

    # Debug: Print drum analysis data
    print("Drum Analysis Data:", drum_analysis)

    # Create MIDI file
    create_midi_file(midi_output_path, drum_analysis)

if __name__ == "__main__":
    main()

import json
import struct
import os

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

def write_midi_notes(midi_file, positions, pitch, velocity):
    """Writes MIDI notes to the file."""
    last_position = 0
    for position in positions:
        start_time = int(position * 960)  # MIDI ticks (assuming 960 PPQ)
        delta_time = start_time - last_position  # Calculate delta time
        last_position = start_time

        # Write MIDI note on
        midi_file.write(write_variable_length_quantity(delta_time))
        midi_file.write(struct.pack("<BBB", 0x90, pitch, velocity))

        # Write MIDI note off
        midi_file.write(write_variable_length_quantity(480))  # Note duration
        midi_file.write(struct.pack("<BBB", 0x80, pitch, 0))

def create_midi_file(output_path, drum_analysis):
    """Creates a MIDI file in Format 1 with separate tracks for kick, snare, and hi-hat notes."""
    try:
        with open(output_path, 'wb') as midi_file:
            # Write MIDI header (Format 1, 3 tracks, 960 ticks per quarter note)
            midi_file.write(b"MThd")
            midi_file.write(struct.pack(">IHHH", 6, 1, 3, 960))

            def write_track(positions, pitch, track_name):
                """Writes a single track with given positions and pitch."""
                if positions:
                    midi_file.write(b"MTrk")
                    track_start_position = midi_file.tell()
                    midi_file.write(struct.pack(">I", 0))  # Placeholder for track length

                    # Write track name meta-event
                    midi_file.write(write_variable_length_quantity(0))  # Delta time
                    midi_file.write(struct.pack("<BB", 0xFF, 0x03))  # Track name event
                    midi_file.write(struct.pack("B", len(track_name)))
                    midi_file.write(track_name.encode('ascii'))

                    # Write notes
                    last_position = 0
                    for position in positions:
                        start_time = int(position * 960)
                        delta_time = start_time - last_position
                        last_position = start_time

                        # Note on
                        midi_file.write(write_variable_length_quantity(delta_time))
                        midi_file.write(struct.pack("<BBB", 0x90, pitch, 100))

                        # Note off
                        midi_file.write(write_variable_length_quantity(480))  # Note duration
                        midi_file.write(struct.pack("<BBB", 0x80, pitch, 0))

                    # Write end of track
                    midi_file.write(write_variable_length_quantity(0))
                    midi_file.write(struct.pack("<BBB", 0xFF, 0x2F, 0x00))  # End of track
                    track_end_position = midi_file.tell()

                    # Update track length
                    midi_file.seek(track_start_position)
                    midi_file.write(struct.pack(">I", track_end_position - track_start_position - 4))
                    midi_file.seek(track_end_position)

            # Write tracks for kick, snare, and hi-hat
            write_track(drum_analysis.get("Kick Positions", []), 36, "Kick")
            write_track(drum_analysis.get("Snare Positions", []), 38, "Snare")
            write_track(drum_analysis.get("HiHat Positions", []), 42, "HiHat")

        print(f"MIDI file with separate tracks successfully created at {output_path}")
    except IOError as e:
        print(f"Error: Unable to write MIDI file. {e}")

def main():
    midi_output_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/generated_drums_with_tracks.mid"
    json_file = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/analysis/analysis_output.json"

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

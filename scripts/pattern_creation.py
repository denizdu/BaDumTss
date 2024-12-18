import reapy

# Connect to the current project in REAPER
project = reapy.Project()

# Check if the project has any tracks
if len(project.tracks) > 0:
    # Access the first track
    track = project.tracks[0]
    print(f"Track name: {track.name}")
    # Create a new MIDI item on the track
    start_position = 0
    length = 2
    midi_item = track.add_midi_item(start_position, length)
    print(f"Added new MIDI item from {start_position} to {length} seconds.")
    # MIDI verisi ekle
    # with project.make_current_project():
    # MIDI notalarını yaz
    # take = midi_item.add_take()
    # take.add_note(start=0, end=0.5, pitch=60, velocity=100)  # C (Do)
    # take.add_note(start=0.5, end=1, pitch=62, velocity=100)  # D (Re)
    # take.add_note(start=1, end=1.5, pitch=64, velocity=100)  # E (Mi)
    # Define a simple drum pattern (kick, snare, hi-hat)
    pattern = [ 
               {"start": 0.0, "end": 0.5, "pitch": 60}, # C (Do)
               {"start": 0.5, "end": 1.0, "pitch": 62}, # D (Re)
               {"start": 1.0, "end": 1.5, "pitch": 64}, # E (Mi)
               {"start": 1.5, "end": 2.0, "pitch": 66} # F (Fa)
               ]

    # Optional: Manipulate the MIDI item
    take = midi_item.active_take
    # Add notes to the MIDI item based on the pattern
    for note in pattern:
        take.add_note(start=note["start"], end=note["end"], pitch=note["pitch"], velocity=100)
        print(f"Added note: start={note['start']}, end={note['end']}, pitch={note['pitch']}")
    track.add_fx("VSTi: ReaSynth (Cockos)")
    # Save the project correctly
    project_path = "C:/Users/denizdu/Documents/ordinary/dfdf.rpp"
    project.save(force_save_as=False)
else:
    print("No tracks found in the project.")


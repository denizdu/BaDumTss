-- Reaper Lua Script: Generate and Import MIDI File from Drum Analysis Data
-- Description: Creates a MIDI file from drum analysis data and imports it into Reaper.

local json = require("dkjson")
local reaper = reaper
local midi_output_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/generated_drums.mid"
local json_file = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/analysis/analysis_output.json"

-- Read JSON file
local function read_file(file_path)
    local file = io.open(file_path, "r")
    if not file then return nil end
    local content = file:read("*all")
    file:close()
    return content
end

local json_content = read_file(json_file)
if not json_content then
    reaper.ShowMessageBox("Failed to read JSON file.", "Error", 0)
    return
end

-- Decode JSON content
local json_data, pos, err = json.decode(json_content, 1, nil)
if err then
    reaper.ShowMessageBox("Invalid JSON format: " .. err, "Error", 0)
    return
end

-- Extract data from JSON
local first_key = next(json_data)
local analysis_data = json_data[first_key]
if not analysis_data or not analysis_data["Drum Analysis"] then
    reaper.ShowMessageBox("No drum analysis data found in JSON file.", "Error", 0)
    return
end

local drum_analysis = analysis_data["Drum Analysis"]

-- Helper function to write MIDI notes
local function write_midi_notes(midi_file, positions, pitch, velocity)
    for _, position in ipairs(positions) do
        local start_time = math.floor(position * 960)  -- MIDI ticks (assuming 960 PPQ)
        local end_time = start_time + 480  -- Note length: half note

        -- Write MIDI note on
        midi_file:write(string.char(0x90, pitch, velocity))
        midi_file:write(string.pack("<I4", start_time))

        -- Write MIDI note off
        midi_file:write(string.char(0x80, pitch, 0))
        midi_file:write(string.pack("<I4", end_time))
    end
end

-- Create MIDI file
local midi_file = io.open(midi_output_path, "wb")
if not midi_file then
    reaper.ShowMessageBox("Failed to create MIDI file.", "Error", 0)
    return
end

-- MIDI header
midi_file:write("MThd")
midi_file:write(string.pack("<I4I2I2I2", 6, 1, 1, 960))

-- MIDI track header
midi_file:write("MTrk")
local track_length_position = midi_file:seek()
midi_file:write(string.pack("<I4", 0))  -- Placeholder for track length

-- Write drum notes (only kicks for now)
if drum_analysis["Kick Positions"] then
    write_midi_notes(midi_file, drum_analysis["Kick Positions"], 36, 100)  -- MIDI pitch 36: Kick
end

-- Write end of track
midi_file:write(string.char(0xFF, 0x2F, 0x00))  -- End of track
local track_end_position = midi_file:seek()
midi_file:seek("set", track_length_position)
midi_file:write(string.pack("<I4", track_end_position - track_length_position - 4))
midi_file:seek("end")

midi_file:close()

reaper.ShowMessageBox("MIDI file with kick drums created successfully.", "Success", 0)

-- Lua script to create MIDI tracks in Reaper with a virtual instrument

-- Import dkjson for JSON parsing
local json = require("dkjson")

-- Load and parse JSON file
function load_json(file_path)
    local file = io.open(file_path, "r")
    if not file then
        reaper.ShowConsoleMsg("Failed to open file: " .. file_path .. "\n")
        return nil
    end

    local content = file:read("*a")
    file:close()

    local data, pos, err = json.decode(content)
    if err then
        reaper.ShowConsoleMsg("Error parsing JSON: " .. err .. "\n")
        return nil
    end

    return data
end

-- Add a virtual instrument to the track
function add_virtual_instrument(track, instrument_name)
    local fx_index = reaper.TrackFX_AddByName(track, instrument_name, false, -1)
    if fx_index >= 0 then
        reaper.ShowConsoleMsg("Added virtual instrument: " .. instrument_name .. "\n")
    else
        reaper.ShowConsoleMsg("Failed to add virtual instrument: " .. instrument_name .. "\n")
    end
end

-- Main function to create MIDI tracks from JSON data
function create_midi_tracks_from_json(json_path)
    local data = load_json(json_path)
    if not data then
        return
    end

    -- Iterate through the JSON data
    for i, combination in ipairs(data) do
        local tempo = tonumber(combination.tempo) or 120
        local energy = tonumber(combination.energy) or 80
        local chroma_mean = combination.chroma_mean or {}

        -- Set project tempo
        reaper.SetCurrentBPM(0, tempo, true)
        reaper.ShowConsoleMsg("Set project tempo to " .. tostring(tempo) .. " BPM\n")

        -- Create a new track
        reaper.InsertTrackAtIndex(reaper.CountTracks(0), true)
        local track = reaper.GetTrack(0, reaper.CountTracks(0) - 1)
        reaper.GetSetMediaTrackInfo_String(track, "P_NAME", "Track " .. i, true)
        reaper.ShowConsoleMsg("Created track " .. i .. "\n")

        -- Add a virtual instrument (e.g., ReaSynth)
        add_virtual_instrument(track, "ReaSynth")

        -- Add MIDI items based on chroma_mean
        local midi_start = 0
        local midi_end = 2 -- Duration of each MIDI note
        for j, pitch in ipairs(chroma_mean) do
            local midi_item = reaper.CreateNewMIDIItemInProj(track, midi_start, midi_start + midi_end, false)
            local take = reaper.GetActiveTake(midi_item)
            if take then
                local velocity = math.floor(energy) -- Use energy for velocity
                local pitch_note = math.floor(pitch * 12 + 60) -- Convert chroma_mean to MIDI pitch
                reaper.MIDI_InsertNote(take, false, false, 0, 480, 0, pitch_note, velocity, true)
                reaper.ShowConsoleMsg("Added MIDI note: pitch=" .. pitch_note .. ", velocity=" .. velocity .. "\n")
            end
            midi_start = midi_start + midi_end
        end
    end

    reaper.ShowConsoleMsg("All MIDI tracks created successfully with virtual instruments.\n")
end

-- Run the script
local json_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/analysis/cleaned_track_combinations.json"
create_midi_tracks_from_json(json_path)

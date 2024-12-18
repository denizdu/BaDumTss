-- Lua Script for Reaper: Import Tracks with Tempo, Energy, and Danceability

-- Add path to dkjson library
package.path = package.path .. ";C:/Users/denizdu/AppData/Roaming/REAPER/Scripts/?.lua"
local json = require("dkjson") -- JSON parsing library

-- Function to read JSON file
function read_json_file(file_path)
    local file = io.open(file_path, "r")
    if not file then
        error("Error: Could not open file " .. file_path)
    end
    local content = file:read("*all")
    file:close()
    local data, _, err = json.decode(content)
    if err then
        error("Error parsing JSON: " .. err)
    end
    return data
end

-- Insert a sample into a track
function insert_sample_to_track(track_name, tempo, energy, danceability)
    if not tempo or not energy or not danceability then
        reaper.ShowConsoleMsg("Error: Missing tempo, energy, or danceability values.\n")
        return
    end

    -- Create a new track
    reaper.InsertTrackAtIndex(reaper.CountTracks(0), true)
    local track = reaper.GetTrack(0, reaper.CountTracks(0) - 1)
    reaper.GetSetMediaTrackInfo_String(track, "P_NAME", track_name, true)

    -- Set tempo, energy, and danceability as track parameters
    local tempo_str = string.format("Tempo: %.2f", tempo)
    local energy_str = string.format("Energy: %.2f", energy)
    local danceability_str = string.format("Danceability: %.2f", danceability)

    -- Add track notes with the values
    local note = tempo_str .. "\n" .. energy_str .. "\n" .. danceability_str
    reaper.GetSetMediaTrackInfo_String(track, "P_NOTES", note, true)

    reaper.ShowConsoleMsg("Track created: " .. track_name .. "\n" .. note .. "\n")
end

-- Main function
function main()
    -- Path to the JSON file exported from Python
    local json_file_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/export/Ardışık_tracks.json"
    local tracks_data = read_json_file(json_file_path)

    -- Iterate through the tracks and create Reaper tracks
    for _, track in ipairs(tracks_data) do
        local track_name = track.name or "Untitled Track"
        local tempo = track.tempo
        local energy = track.energy
        local danceability = track.danceability

        -- Validate and insert sample
        if tempo and energy and danceability then
            insert_sample_to_track(track_name, tempo, energy, danceability)
        else
            reaper.ShowConsoleMsg("Skipping track: " .. track_name .. " (missing required values)\n")
        end
    end
end

-- Run the script
main()
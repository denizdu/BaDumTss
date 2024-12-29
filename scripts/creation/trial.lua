-- Reaper Lua Script: Add Full Analysis Data from JSON to Project
-- Author: Deniz
-- Description: Parses a JSON file to add BPM, beat grid, drum analysis, and spectral features into a Reaper project.

local json = require("dkjson")
local reaper = reaper

local json_file = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/analysis/input.json"
local kick_sample_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Kicks/Cymatics_9God_Kick_1_C.wav"
local snare_sample_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Snares/Cymatics_9God_Snare_1_C.wav"
local hihat_sample_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Cymbals/Rides/Cymatics_9God_Ride_1.wav"

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

-- Extract data for processing
local analysis_data = json_data[next(json_data)]  -- Assuming first key contains the analysis
if not analysis_data then
    reaper.ShowMessageBox("No valid data found in JSON file.", "Error", 0)
    return
end

-- Set project BPM
if analysis_data["Main Features"] and analysis_data["Main Features"]["Tempo (BPM)"] then
    local bpm = analysis_data["Main Features"]["Tempo (BPM)"]
    reaper.SetCurrentBPM(0, bpm, true)
end

-- Ensure there are tracks for kicks, snares, and hi-hats
local function ensure_track(index, name)
    local track = reaper.GetTrack(0, index)
    if not track then
        reaper.InsertTrackAtIndex(index, true)
        track = reaper.GetTrack(0, index)
        reaper.GetSetMediaTrackInfo_String(track, "P_NAME", name, true)
    end
    return track
end

local kick_track = ensure_track(0, "Kicks")
local snare_track = ensure_track(1, "Snares")
local hihat_track = ensure_track(2, "Hi-Hats")

-- Function to add media items
local function add_media_item(track, position, sample_path)
    local item = reaper.AddMediaItemToTrack(track)
    if item then
        reaper.SetMediaItemInfo_Value(item, "D_POSITION", position)
        reaper.SetMediaItemInfo_Value(item, "D_LENGTH", 0.1)  -- Default length for drum hits
        local take = reaper.AddTakeToMediaItem(item)
        if take then
            local source = reaper.PCM_Source_CreateFromFile(sample_path)
            if not source then
                reaper.ShowMessageBox("Failed to load sample file: " .. sample_path, "Error", 0)
                return false
            end
            reaper.SetMediaItemTake_Source(take, source)
        else
            reaper.ShowMessageBox("Failed to create take for track: " .. sample_path, "Error", 0)
            return false
        end
    else
        reaper.ShowMessageBox("Failed to create media item on track.", "Error", 0)
        return false
    end
    return true
end

-- Process drum analysis
if analysis_data["Drum Analysis"] then
    local drum_analysis = analysis_data["Drum Analysis"]

    -- Add kick positions
    if drum_analysis["Kick Positions"] then
        for _, position in ipairs(drum_analysis["Kick Positions"]) do
            if not add_media_item(kick_track, position, kick_sample_path) then return end
        end
    end

    -- Add snare positions
    if drum_analysis["Snare Positions"] then
        for _, position in ipairs(drum_analysis["Snare Positions"]) do
            if not add_media_item(snare_track, position, snare_sample_path) then return end
        end
    end

    -- Add hi-hat positions
    if drum_analysis["HiHat Positions"] then
        for _, position in ipairs(drum_analysis["HiHat Positions"]) do
            if not add_media_item(hihat_track, position, hihat_sample_path) then return end
        end
    end
end

-- Process spectral features as markers
if analysis_data["Spectral Features"] then
    local spectral_features = analysis_data["Spectral Features"]
    if spectral_features["Spectral Centroid"] then
        local marker_position = 0  -- Example position, adjust as needed
        reaper.AddProjectMarker(0, false, marker_position, 0, "Spectral Centroid: " .. spectral_features["Spectral Centroid"], -1)
    end
    if spectral_features["Spectral Roll-off"] then
        local marker_position = 2  -- Example position, adjust as needed
        reaper.AddProjectMarker(0, false, marker_position, 0, "Spectral Roll-off: " .. spectral_features["Spectral Roll-off"], -1)
    end
end

reaper.ShowMessageBox("Analysis data has been added to the Reaper project.", "Success", 0)

-- Lua script to parse and create tracks in REAPER using dkjson

-- Load dkjson library
local json = require "dkjson"

-- Load JSON file content
function load_json_file(file_path)
    local file = io.open(file_path, "r")
    if not file then
        reaper.ShowConsoleMsg("Could not open file: " .. file_path .. "\n")
        return nil
    end

    local content = file:read("*a")
    file:close()

    reaper.ShowConsoleMsg("JSON file content loaded successfully.\n")

    -- Attempt to parse JSON with dkjson
    local parsed_data, pos, err = json.decode(content)
    if err then
        reaper.ShowConsoleMsg("Failed to parse JSON content: " .. tostring(err) .. "\n")
        return nil
    end

    return parsed_data
end

-- Main function to create tracks from JSON data
function main()
    -- Specify the JSON file path
    local json_file_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/analysis/cleaned_track_combinations.json"
    reaper.ShowConsoleMsg("Loading JSON file: " .. json_file_path .. "\n")

    local data = load_json_file(json_file_path)

    if not data then
        reaper.ShowConsoleMsg("Failed to load or parse JSON file. Exiting script.\n")
        return
    end

    reaper.ShowConsoleMsg("JSON data loaded and parsed successfully.\n")

    -- Iterate through the JSON data to create tracks
    for i, combination in ipairs(data) do
        reaper.ShowConsoleMsg("Processing combination " .. tostring(i) .. "\n")

        local track_name = "Combination " .. tostring(i)
        reaper.InsertTrackAtIndex(reaper.CountTracks(0), true) -- Create a new track
        local track = reaper.GetTrack(0, reaper.CountTracks(0) - 1)

        if track then
            reaper.GetSetMediaTrackInfo_String(track, "P_NAME", track_name, true)
            reaper.ShowConsoleMsg("Created track: " .. track_name .. "\n")

            -- Log the track details
            if type(combination) ~= "table" then
                reaper.ShowConsoleMsg("Combination " .. tostring(i) .. " is not a table. Skipping.\n")
                goto continue
            end

            local tempo = combination.tempo or "Unknown Tempo"
            local energy = combination.energy or "Unknown Energy"
            local chroma_mean = table.concat(combination.chroma_mean or {}, ", ")

            reaper.ShowConsoleMsg(" - Tempo: " .. tostring(tempo) .. "\n")
            reaper.ShowConsoleMsg(" - Energy: " .. tostring(energy) .. "\n")
            reaper.ShowConsoleMsg(" - Chroma Mean: " .. tostring(chroma_mean) .. "\n")
        else
            reaper.ShowConsoleMsg("Failed to create track for combination: " .. tostring(i) .. "\n")
        end

        ::continue::
    end

    reaper.ShowConsoleMsg("All tracks created successfully.\n")
end

-- Run the script
main()

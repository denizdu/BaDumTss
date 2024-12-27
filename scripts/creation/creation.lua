-- Include dkjson library for JSON parsing
local json = require("dkjson")

-- Load environment variables from a .env file
function load_env(filepath)
    local env_vars = {}
    local file = io.open(filepath, "r")
    if not file then
        reaper.ShowConsoleMsg("Error: Could not open .env file at " .. filepath .. "\n")
        return env_vars
    end

    -- İlk geçiş: Tüm değişkenleri yükle
    for line in file:lines() do
        if line:match("^%s*$") == nil and not line:match("^#") then
            local key, value = line:match("^(%w+)=(.+)$")
            if key and value then
                env_vars[key] = value
            else
                reaper.ShowConsoleMsg("Warning: Skipping invalid line in .env file: " .. line .. "\n")
            end
        end
    end
    file:close()

    -- İkinci geçiş: Değişken interpolasyonlarını çöz
    for key, value in pairs(env_vars) do
        env_vars[key] = value:gsub("%${(.-)}", function(var_name)
            return env_vars[var_name] or ""
        end)
    end

    return env_vars
end

-- Check if file exists
function file_exists(filepath)
    local file = io.open(filepath, "r")
    if file then
        file:close()
        return true
    else
        return false
    end
end

-- Load model output from a JSON file
function load_model_output(filepath)
    if not file_exists(filepath) then
        reaper.ShowConsoleMsg("Error: File does not exist - " .. filepath .. "\n")
        return nil
    end
    local file = io.open(filepath, "r")
    local content = file:read("*all")
    file:close()
    local data, pos, err = json.decode(content, 1, nil)
    if err then
        reaper.ShowConsoleMsg("Error parsing JSON: " .. err .. "\n")
        return nil
    end
    return data
end

-- Initialize a new Reaper project
function initialize_reaper()
    reaper.Main_OnCommand(40025, 0) -- New Project
    reaper.ShowConsoleMsg("Initialized Reaper project\n")
end

-- Create a new track
function create_new_track(track_name)
    local track_index = reaper.CountTracks(0)
    reaper.InsertTrackAtIndex(track_index, true)
    local track = reaper.GetTrack(0, track_index)
    reaper.GetSetMediaTrackInfo_String(track, "P_NAME", track_name, true)
    reaper.ShowConsoleMsg("Created track: " .. track_name .. "\n")
    return track
end

-- Create a MIDI item on a given track
function create_midi_item(track, start_time, end_time)
    local item = reaper.CreateNewMIDIItemInProj(track, start_time, end_time, false)
    reaper.ShowConsoleMsg("Created MIDI item\n")
    return item
end

-- Process Main Features
function process_main_features(track, main_features)
    if main_features["Tempo (BPM)"] then
        reaper.CSurf_OnTempoChange(main_features["Tempo (BPM)"])
        reaper.ShowConsoleMsg("Set tempo to " .. main_features["Tempo (BPM)"] .. " BPM\n")
    end
    if main_features["Key (Tonalite)"] then
        reaper.ShowConsoleMsg("Set key to " .. main_features["Key (Tonalite)"] .. "\n")
    end
end

-- Process Frequency and Spectrum
function process_freq_and_spectrum(track, freq_data)
    if freq_data then
        reaper.ShowConsoleMsg("Processing frequency spectrum for track\n")
        -- Add frequency manipulation logic
    end
end

-- Process Rhythm
function process_rhythm(track, rhythm_data)
    if rhythm_data then
        reaper.ShowConsoleMsg("Processing rhythm for track\n")
        -- Add rhythm processing logic
    end
end

-- Process Spectral Features
function process_spectral_features(track, spectral_data)
    if spectral_data then
        reaper.ShowConsoleMsg("Processing spectral features for track\n")
        -- Add spectral feature processing logic
    end
end

-- Process Extra Features
function process_extra_features(track, extra_data)
    if extra_data then
        reaper.ShowConsoleMsg("Processing extra features for track\n")
        -- Add extra feature processing logic
    end
end

-- Process the pipeline for each track
function process_pipeline(model_data)
    for track_name, track_data in pairs(model_data) do
        reaper.ShowConsoleMsg("Processing track: " .. track_name .. "\n")
        local track = create_new_track(track_name)

        -- Create a placeholder MIDI item
        create_midi_item(track, 0, 10)

        -- Process each feature
        process_main_features(track, track_data["Main Features"])
        process_freq_and_spectrum(track, track_data["Frequency and Spectrum"])
        process_rhythm(track, track_data["Rhythm"])
        process_spectral_features(track, track_data["Spectral Features"])
        process_extra_features(track, track_data["Extra Features"])
    end
end

-- Save the project
function save_project(output_directory, filename)
    local project_path = output_directory .. "/" .. filename
    reaper.ShowConsoleMsg("Saving project to: " .. project_path .. "\n")

    -- Ensure the output directory exists
    local output_folder_check = os.execute('mkdir "' .. output_directory .. '"')
    if output_folder_check ~= 0 then
        reaper.ShowConsoleMsg("Warning: Output directory already exists or could not be created.\n")
    end

    -- Save the project
    local success = reaper.Main_SaveProject(0, false)
    if success then
        reaper.ShowConsoleMsg("Project successfully saved to: " .. project_path .. "\n")
    else
        reaper.ShowConsoleMsg("Error: Failed to save the project.\n")
    end
end


-- Main Function
function main()
    -- Get paths from environment variables
    local output_directory = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/creation"
    local model_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/model/model_output.json"

    -- Load model data
    local model_data = load_model_output(model_path)
    if not model_data then
        return
    end

    -- Initialize Reaper project
    initialize_reaper()

    -- Process the creation pipeline
    -- process_pipeline(model_data)

    -- Save the project
    --save_project(output_directory, "created_project.rpp")
end

main()

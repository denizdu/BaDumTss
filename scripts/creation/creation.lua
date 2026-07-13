-- creation.lua script

-- Load the JSON library.
local json = require("dkjson")

local kick_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Kicks/Cymatics_9God_Kick_1_C.wav"
local snare_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Snares/Cymatics_9God_Snare_1_C.wav"
local hihat_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Cymbals/Rides/Cymatics_9God_Ride_1.wav"

-- Read an input file.
function read_json_file(file_path)
    local file = io.open(file_path, "r")
    if not file then error("Could not open file: " .. file_path) end
    local content = file:read("*a")
    file:close()
    return json.decode(content)
end

-- Sanitize file names.
function sanitize_filename(name)
    local translation_table = {
        [" "] = "_",
        ["ı"] = "i",
        ["İ"] = "I",
        ["ş"] = "s",
        ["Ş"] = "S",
        ["ğ"] = "g",
        ["Ğ"] = "G",
        ["ö"] = "o",
        ["Ö"] = "O",
        ["ü"] = "u",
        ["Ü"] = "U",
        ["ç"] = "c",
        ["Ç"] = "C",
        ["|"] = "",
        [","] = "",
        ["."] = "",
        ["'"] = "",
        ["/"] = "", -- Remove path separator characters.
        ["\\"] = "",
        [":"] = "",
        ["*"] = "",
        ["?"] = "",
        ["\""] = "",
        ["<"] = "",
        [">"] = ""
    }
    name = name:gsub(".", translation_table)
    name = name:gsub("_+", "_") -- Collapse consecutive underscores.
    name = name:gsub("^_+", ""):gsub("_+$", "") -- Remove leading and trailing underscores.
    return name
end

-- Create a new REAPER project.
function create_new_project()
    reaper.Main_openProject("") -- Open an empty project.
end

-- Add a track.
function add_track()
    reaper.InsertTrackAtIndex(0, true) -- Insert a new first track.
end

-- Add an audio sample to a track.
function add_sample_to_track(track, sample_path, start_position)
    local retval = reaper.InsertMedia(sample_path, 0)
    if retval then
        local item = reaper.GetTrackMediaItem(track, reaper.CountTrackMediaItems(track) - 1)
        if item then
            reaper.SetMediaItemInfo_Value(item, "D_POSITION", start_position)
        end
    end
end

-- Add a MIDI note using project seconds for the item and PPQ positions for note events.
function add_midi_note_to_track(track, note, start_seconds, duration_beats, tempo)
    local duration_seconds = duration_beats * 60.0 / tempo
    local end_seconds = start_seconds + duration_seconds
    local item = reaper.CreateNewMIDIItemInProj(track, start_seconds, end_seconds, false)
    local take = reaper.GetMediaItemTake(item, 0)
    if take then
        local start_ppq = reaper.MIDI_GetPPQPosFromProjTime(take, start_seconds)
        local end_ppq = reaper.MIDI_GetPPQPosFromProjTime(take, end_seconds)
        reaper.MIDI_InsertNote(take, false, false, start_ppq, end_ppq, 0, math.floor(note), 100, false)
        reaper.MIDI_Sort(take)
    end
end

-- Process core features.
function process_main_features(features)
    local tempo = features["Tempo (BPM)"]
    reaper.SetCurrentBPM(0, tempo, true) -- Set the tempo.
end

-- Report interpretable spectral measurements without treating FFT magnitudes as EQ parameters.
function report_spectral_profile(spectral_features)
    if not spectral_features then
        reaper.ShowConsoleMsg("Spectral features are unavailable; skipping the profile report.\n")
        return
    end

    local centroid = tonumber(spectral_features["Spectral Centroid"])
    local rolloff = tonumber(spectral_features["Spectral Roll-off"])
    if not centroid or not rolloff then
        reaper.ShowConsoleMsg("Spectral centroid or roll-off is invalid; skipping the profile report.\n")
        return
    end

    local profile = "balanced"
    if centroid < 1500 then
        profile = "dark"
    elseif centroid > 3500 then
        profile = "bright"
    end

    reaper.ShowConsoleMsg(string.format(
        "Spectral profile: %s (centroid %.1f Hz, roll-off %.1f Hz). Automatic EQ is disabled until calibrated frequency-band data is available.\n",
        profile, centroid, rolloff
    ))
end

-- Create rhythm and melody parts.
function create_rhythm_and_melody(song_data, track)
    local rhythm = song_data["Rhythm"]
    local melody = song_data["Frequency and Spectrum"] and song_data["Frequency and Spectrum"]["Melody Contour"]
    local tempo = tonumber(song_data["Main Features"] and song_data["Main Features"]["Tempo (BPM)"]) or 120

    -- Validate rhythm and melody values.
    if not rhythm or not rhythm["Beat Grid"] then
        reaper.ShowConsoleMsg("Rhythm data is missing or invalid.\n")
        return
    end

    if not melody then
        reaper.ShowConsoleMsg("Melody Contour data is missing or invalid.\n")
        return
    end

    -- Add kick, snare, and hi-hat notes for the rhythm.
    for i, beat in ipairs(rhythm["Beat Grid"]) do
        if i % 4 == 1 then -- Add kick on the first beat of each four-beat group.
            add_sample_to_track(track, kick_path, beat)
        elseif i % 4 == 2 or i % 4 == 4 then -- Add snare on the second and fourth beats.
            add_sample_to_track(track, snare_path, beat)
        else -- Add hi-hat on all remaining beats.
            add_sample_to_track(track, hihat_path, beat)
        end
    end

    -- Add the melody.
    for i, freq in ipairs(melody) do
        local note = math.floor(69 + 12 * math.log(freq / 440) / math.log(2) + 0.5) -- Round to the nearest note.
        local start_seconds = (i - 1) * 60.0 / tempo
        add_midi_note_to_track(track, note, start_seconds, 0.5, tempo)
    end
end

-- Process a song and save the project.
function process_song(song_name, song_data)
    create_new_project()
    add_track()
    local track = reaper.GetTrack(0, 0)

    process_main_features(song_data["Main Features"])
    report_spectral_profile(song_data["Spectral Features"])
    create_rhythm_and_melody(song_data, track)

    local sanitized_name = sanitize_filename(song_name)
    local save_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/creation/" .. sanitized_name .. ".rpp"
    reaper.Main_SaveProjectEx(0, save_path, 0)
end

-- Main script flow.
function main()
    local input_file = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/model/model_output.json" -- Path to the JSON file.
    local song_data = read_json_file(input_file)

    for song_name, data in pairs(song_data) do
        process_song(song_name, data)
    end
end

main()

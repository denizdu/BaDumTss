-- creation.lua script

-- JSON kütüphanesini yükler
local json = require("dkjson")

local kick_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Kicks/Cymatics_9God_Kick_1_C.wav"
local snare_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Snares/Cymatics_9God_Snare_1_C.wav"
local hihat_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/sample/drums/Cymbals/Rides/Cymatics_9God_Ride_1.wav"

-- Input dosyasını okur
function read_json_file(file_path)
    local file = io.open(file_path, "r")
    if not file then error("Dosya açılamadı: " .. file_path) end
    local content = file:read("*a")
    file:close()
    return json.decode(content)
end

-- Dosya adlarını sanitize eden fonksiyon
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
        ["/"] = "", -- Yol karakterlerini temizle
        ["\\"] = "",
        [":"] = "",
        ["*"] = "",
        ["?"] = "",
        ["\""] = "",
        ["<"] = "",
        [">"] = ""
    }
    name = name:gsub(".", translation_table)
    name = name:gsub("_+", "_") -- Birden fazla alt çizgiyi tek bir alt çizgiye indir
    name = name:gsub("^_+", ""):gsub("_+$", "") -- Baştaki ve sondaki alt çizgileri kaldır
    return name
end

-- Reaper'da yeni proje oluşturur
function create_new_project()
    reaper.Main_openProject("") -- Boş bir proje açar
end

-- Track ekler
function add_track()
    reaper.InsertTrackAtIndex(0, true) -- İlk sırada yeni bir track ekler
end

-- Örnek ses dosyasını track'e ekler
function add_sample_to_track(track, sample_path, start_position)
    local retval = reaper.InsertMedia(sample_path, 0)
    if retval then
        local item = reaper.GetTrackMediaItem(track, reaper.CountTrackMediaItems(track) - 1)
        if item then
            reaper.SetMediaItemInfo_Value(item, "D_POSITION", start_position)
        end
    end
end

-- MIDI notası ekler
function add_midi_note_to_track(track, note, start_position)
    local item = reaper.CreateNewMIDIItemInProj(track, math.floor(start_position), math.floor(start_position + 960), false) -- MIDI PPQ: 960 = çeyrek nota
    local take = reaper.GetMediaItemTake(item, 0)
    if take then
        reaper.MIDI_InsertNote(take, false, false, math.floor(start_position), math.floor(start_position + 480), 0, math.floor(note), 100, false)
    end
end

-- Ana özellikleri işler
function process_main_features(features)
    local tempo = features["Tempo (BPM)"]
    reaper.SetCurrentBPM(0, tempo, true) -- Tempo ayarla
end

-- Frekans ve spektrum özelliklerini işler
function process_freq_and_spectrum(freq_spec, track)
    local spectrum = freq_spec["Frequency Spectrum"]
    reaper.TrackFX_AddByName(track, "ReaEQ", false, -1) -- EQ ekle
    for i, value in ipairs(spectrum) do
        reaper.TrackFX_SetParam(track, 0, i - 1, value / 50) -- EQ bandını ayarla
    end
end

-- Ritim ve melodi oluşturur
function create_rhythm_and_melody(song_data, track)
    local rhythm = song_data["Rhythm"]
    local melody = song_data["Frequency and Spectrum"] and song_data["Frequency and Spectrum"]["Melody Contour"]

    -- Ritim ve melodi değerlerini kontrol et
    if not rhythm or not rhythm["Beat Grid"] then
        reaper.ShowConsoleMsg("Ritim bilgileri eksik veya hatalı.\n")
        return
    end

    if not melody then
        reaper.ShowConsoleMsg("Melody Contour eksik veya hatalı.\n")
        return
    end

    -- Ritim için Kick, Snare ve HiHat ekle
    for i, beat in ipairs(rhythm["Beat Grid"]) do
        if i % 4 == 1 then -- Her 4 beat'in birincisine kick ekle
            add_sample_to_track(track, kick_path, beat)
        elseif i % 4 == 2 or i % 4 == 4 then -- İkinci ve dördüncü vuruşlara snare ekle
            add_sample_to_track(track, snare_path, beat)
        else -- Diğer tüm vuruşlara hihat ekle
            add_sample_to_track(track, hihat_path, beat)
        end
    end

    -- Melodi ekle
    for i, freq in ipairs(melody) do
        local note = math.floor(69 + 12 * math.log(freq / 440) / math.log(2) + 0.5) -- Yuvarlama eklendi
        local start_pos = math.floor(i * 960) -- Tam sayıya çevir
        add_midi_note_to_track(track, note, start_pos)
    end
end

-- Şarkıyı işler ve proje kaydeder
function process_song(song_name, song_data)
    create_new_project()
    add_track()
    local track = reaper.GetTrack(0, 0)

    process_main_features(song_data["Main Features"])
    process_freq_and_spectrum(song_data["Frequency and Spectrum"], track)
    create_rhythm_and_melody(song_data, track)

    local sanitized_name = sanitize_filename(song_name)
    local save_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/creation/" .. sanitized_name .. ".rpp"
    reaper.Main_SaveProjectEx(0, save_path, 0)
end

-- Ana script akışı
function main()
    local input_file = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/output/model/model_output.json" -- JSON dosyasının yolu
    local song_data = read_json_file(input_file)

    for song_name, data in pairs(song_data) do
        process_song(song_name, data)
    end
end

main()

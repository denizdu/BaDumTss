-- Lua Script for Reaper: Import Tracks with Tempo, Energy, and Danceability
-- JSON kütüphanesi (dkjson) dahil edilir
package.path = package.path .. ";C:/Users/denizdu/AppData/Roaming/REAPER/Scripts/?.lua"
local json = require("dkjson") -- JSON parsing library

-- JSON dosyasını okuma fonksiyonu
local function read_json_file(file_path)
    local file, err = io.open(file_path, "r")
    if not file then
        reaper.ShowMessageBox("JSON dosyası açılamadı: " .. err, "Hata", 0)
        return nil
    end
    local content = file:read("*a")
    file:close()
    return json.decode(content)
end

-- Track ve Media Item oluşturma
local function create_track_with_items(track_name, tracks_data)
    -- Yeni bir track oluştur
    local track_index = reaper.CountTracks(0)
    reaper.InsertTrackAtIndex(track_index, true)
    local track = reaper.GetTrack(0, track_index)
    reaper.GetSetMediaTrackInfo_String(track, "P_NAME", track_name, true)

    -- Her bir şarkı için media item ekle
    local position = 0 -- Başlangıç pozisyonu
    for _, track_data in ipairs(tracks_data) do
        local tempo = track_data.tempo or 120
        local energy = track_data.energy or 0.5
        local danceability = track_data.danceability or 0.5

        -- Şarkının uzunluğu ve enerjiye bağlı ses seviyesi
        local duration = (track_data.duration_ms or 200000) / 1000 -- Saniyeye çevir
        local volume = energy * 1.5 -- Ses seviyesi enerjiden etkilenir

        -- Media item oluştur ve track'e ekle
        local item = reaper.CreateNewMIDIItemInProj(track, position, position + duration, false)
        local take = reaper.GetMediaItemTake(item, 0)
        reaper.GetSetMediaItemInfo_String(item, "P_NAME", track_data.name, true)
        reaper.SetMediaItemInfo_Value(item, "D_VOL", volume)

        -- MIDI notalar ekle
        local start_pitch = math.floor(danceability * 60 + 36) -- Dans edilebilirlik ton aralığını belirler
        reaper.MIDI_InsertNote(take, false, false, 0, 240, 0, start_pitch, 100, false)

        -- Pozisyonu ilerlet
        position = position + duration + 1 -- Şarkılar arasında 1 saniye boşluk
    end
end

-- Kullanıcıdan JSON dosyasını seçmesini iste
local retval, file_path = reaper.GetUserFileNameForRead("", "Cleaned JSON Dosyasını Seçin", ".json")
if not retval then return end

-- JSON dosyasını oku
local playlist_data = read_json_file(file_path)
if not playlist_data then return end

-- Reaper üzerinde patternler oluştur
create_track_with_items("Spotify Playlist", playlist_data)

-- İşlem tamamlandı
reaper.ShowMessageBox("Playlist başarıyla işlendi ve patternler oluşturuldu.", "Tamamlandı", 0)

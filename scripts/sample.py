import sys
sys.path.append("C:/Program Files/REAPER (x64)/Plugins")
import reaper_python  # ReaScript Python API'yi yükle

# Sample dosyasını yükleme
def insert_sample_to_track(sample_path, track_name):
    num_tracks = RPR_CountTracks(0)  # Toplam track sayısı
    track_found = False

    # Mevcut track'lerde ismi kontrol et
    for i in range(num_tracks):
        track = RPR_GetTrack(0, i)
        retval, current_track_name = RPR_GetSetMediaTrackInfo_String(track, "P_NAME", "", False)
        if current_track_name == track_name:
            track_found = True
            break

    # Track yoksa yeni bir tane ekle
    if not track_found:
        RPR_InsertTrackAtIndex(num_tracks, True)
        track = RPR_GetTrack(0, num_tracks)
        RPR_GetSetMediaTrackInfo_String(track, "P_NAME", track_name, True)

    # Sample'ı yükle
    RPR_InsertMedia(sample_path, 0)

    print(f"Sample '{sample_path}' başarıyla {track_name} isimli track'e eklendi.")

# Sample dosyasını bir döngüde çalma
def create_loop(track_name, loop_length):
    num_tracks = RPR_CountTracks(0)

    for i in range(num_tracks):
        track = RPR_GetTrack(0, i)
        retval, current_track_name = RPR_GetSetMediaTrackInfo_String(track, "P_NAME", "", False)
        if current_track_name == track_name:
            num_items = RPR_GetTrackNumMediaItems(track)
            if num_items > 0:
                media_item = RPR_GetTrackMediaItem(track, 0)
                RPR_SetMediaItemInfo_Value(media_item, "D_LENGTH", loop_length)
                RPR_SetMediaItemInfo_Value(media_item, "B_LOOPSRC", 1)  # Loop özelliğini aç
                RPR_Main_OnCommand(40020, 0)  # Loop aktif et
                print(f"{track_name} track'inde {loop_length} saniyelik döngü oluşturuldu.")
                return

# Örnek Kullanım
sample_path = "C:/Users/Deniz/Music/sample.wav"
track_name = "Beat Track"
loop_length = 4.0  # 4 saniyelik döngü

insert_sample_to_track(sample_path, track_name)
create_loop(track_name, loop_length)
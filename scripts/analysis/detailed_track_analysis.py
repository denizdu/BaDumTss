import librosa
import librosa.display
import matplotlib.pyplot as plt

# 1. Ses dosyasını yükle
file_path = 'C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/samples/raw/JamieScottMade.mp3'  # Ses dosyasının yolunu buraya ekle
y, sr = librosa.load(file_path)

# 2. Temel bilgiler
print(f"\u00d6rnekleme oranı: {sr} Hz")
print(f"Ses dosyasının uzunluğu: {len(y) / sr:.2f} saniye")

# 3. Ses dalgasını çiz
plt.figure(figsize=(12, 4))
librosa.display.waveshow(y, sr=sr)
plt.title("Ses Dalgası")
plt.xlabel("Zaman (saniye)")
plt.ylabel("Genlik")
plt.show()

# Tempo ve beat bilgisi
try:
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    if isinstance(tempo, (float, int)):
        print(f"Tempo (BPM): {tempo:.2f}")
    elif isinstance(tempo, (list, tuple, librosa.core.time_constant.numpy.ndarray)):
        tempo_value = tempo[0] if len(tempo) > 0 else None
        print(f"Tempo (BPM): {tempo_value:.2f}")
    else:
        print("Tempo tipi tanımlanamıyor.")
    print(f"Ritmik Vuruşlar (Beat Frame Sayısı): {len(beats)}")

    # Beatlerin zamanını hesapla
    beat_times = librosa.frames_to_time(beats, sr=sr)
    print(f"Ritmik Vuruş Zamanları: {beat_times[:10]}")  # İlk 10 vuruşun zamanı
except Exception as e:
    print(f"Tempo veya ritim analizinde bir hata oluştu: {e}")

# Chroma özellikleri
try:
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)

    # Görselleştirme
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(chroma, x_axis='time', y_axis='chroma', sr=sr, cmap='coolwarm')
    plt.colorbar()
    plt.title("Chroma Özellikleri")
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("Notalar")
    plt.show()
except Exception as e:
    print(f"Chroma analizinde bir hata oluştu: {e}")

# Spektrogram
try:
    S = librosa.stft(y)
    S_db = librosa.amplitude_to_db(abs(S))

    # Görselleştirme
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title("Frekans Spektrumu (Spektrogram)")
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("Frekans (Hz)")
    plt.show()
except Exception as e:
    print(f"Spektrogram analizinde bir hata oluştu: {e}")

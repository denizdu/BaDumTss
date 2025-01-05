import os
import json
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# .env dosyasını yükle
load_dotenv()

# Dizinler
DIR_OUTPUT_ANALYSIS = os.getenv("DIR_OUTPUT_ANALYSIS")
DIR_OUTPUT_MODEL = os.getenv("DIR_OUTPUT_MODEL")

input_data_file = os.path.join(DIR_OUTPUT_ANALYSIS, "analysis_output.json")
output_file = os.path.join(DIR_OUTPUT_MODEL, "drum_kit_recommendation_model.pkl")

# Analiz dosyasının bulunduğu dizini oluştur
os.makedirs(DIR_OUTPUT_ANALYSIS, exist_ok=True)

# Veri Yükleme
with open(input_data_file, 'r') as file:
    data = json.load(file)

# Veriyi Hazırlama
def prepare_data(data):
    features = []
    labels = []

    for file_path, analysis in data.items():
        # Ana özelliklerden bazılarını seçiyoruz
        main_features = analysis["Main Features"]
        tempo = main_features.get("Tempo (BPM)", 0)
        loudness = main_features.get("Loudness (dB)", 0)
        dynamics = main_features.get("Dynamics", 0)

        # Frekans spektrumunun ortalamasını alıyoruz
        spectrum = analysis["Frequency and Spectrum"].get("Frequency Spectrum", [])
        spectrum_mean = sum(spectrum) / len(spectrum) if spectrum else 0

        # Drum kit önerisi için dummy bir label ekleniyor (örneğin "Rock", "Hip-Hop")
        # Gerçek verilerinizde bu etiketlerin doğru olmasını sağlamalısınız.
        label = "Rock" if tempo > 120 else "Jazz"  # Bu kısım örnek.

        features.append([tempo, loudness, dynamics, spectrum_mean])
        labels.append(label)

    return pd.DataFrame(features, columns=["Tempo", "Loudness", "Dynamics", "Spectrum Mean"]), labels

# Veriyi işleme
X, y = prepare_data(data)

# Veri Setini Eğitim ve Test Olarak Ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli Eğitme
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Modeli Test Etme
y_pred = model.predict(X_test)

# Sonuçları Yazdırma
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Modeli Kaydetme
import joblib
joblib.dump(model, output_file)

print("Model başarıyla eğitildi ve kaydedildi!")

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. Veri Yükleme
file_path = r"C:\\Users\\denizdu\\OneDrive\\Masaüstü\\BaDumTss\\output\\analysis\\analysis_output.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# 2. Veriyi İşleme
rows = []
for file, features in data.items():
    main_features = features.get("Main Features", {})
    freq_features = features.get("Frequency and Spectrum", {})
    spectral_features = features.get("Spectral Features", {})
    extra_features = features.get("Extra Features", {})

    rows.append({
        "file": file,
        "tempo_bpm": main_features.get("Tempo (BPM)", np.nan),
        "key": main_features.get("Key (Tonalite)", "Unknown"),
        "loudness_db": main_features.get("Loudness (dB)", np.nan),
        "dynamics": main_features.get("Dynamics", np.nan),
        "harmonic_content": freq_features.get("Harmonic Content", np.nan),
        "spectral_centroid": spectral_features.get("Spectral Centroid", np.nan),
        "spectral_rolloff": spectral_features.get("Spectral Roll-off", np.nan),
        "zero_crossing_rate": extra_features.get("Zero-Crossing Rate", np.nan)
    })

# Pandas DataFrame oluşturma
df = pd.DataFrame(rows)

# Eksik verileri doldurma (sadece sayısal sütunlar için)
numeric_columns = df.select_dtypes(include=[np.number])
df[numeric_columns.columns] = numeric_columns.fillna(numeric_columns.mean())

# Sayısal olmayan sütunlar için varsayılan değerler atama
non_numeric_columns = df.select_dtypes(exclude=[np.number])
for col in non_numeric_columns.columns:
    df[col] = df[col].fillna("Unknown")

# 3. Veri Görselleştirme
def plot_feature_distribution(df, feature):
    plt.figure(figsize=(8, 6))
    plt.hist(df[feature], bins=20, alpha=0.7, color='blue')
    plt.title(f"Distribution of {feature}")
    plt.xlabel(feature)
    plt.ylabel("Frequency")
    plt.show()

# Örnek görselleştirme
plot_feature_distribution(df, "tempo_bpm")
plot_feature_distribution(df, "spectral_centroid")

# 4. Veri Ölçekleme ve Modelleme
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.drop(columns=["file", "key"]))

# K-Means Modeli
n_clusters = min(len(df), 3)  # Veri boyutuna uygun küme sayısı belirleme
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(scaled_features)
df['cluster'] = kmeans.labels_

# PCA ile boyut indirgeme
pca = PCA(n_components=2)
pca_features = pca.fit_transform(scaled_features)

def plot_clusters(pca_features, labels):
    plt.figure(figsize=(8, 6))
    plt.scatter(pca_features[:, 0], pca_features[:, 1], c=labels, cmap='viridis', alpha=0.6)
    plt.title("Cluster Visualization")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.colorbar(label="Cluster")
    plt.show()

plot_clusters(pca_features, kmeans.labels_)

# 5. Öneri Motoru
def recommend_similar_songs(df, cluster_id, top_n=3):
    cluster_songs = df[df['cluster'] == cluster_id]
    return cluster_songs.sort_values(by="tempo_bpm").head(top_n)["file"].tolist()

# Örnek öneriler
cluster_id = 0
recommendations = recommend_similar_songs(df, cluster_id)
print(f"Recommended songs for cluster {cluster_id}: {recommendations}")

# 6. Analiz Raporu - `ace_tools` olmadan
output_path = r"C:\\Users\\denizdu\\OneDrive\\Masaüstü\\BaDumTss\\output\\model\\clustered_music_data.csv"
df.to_csv(output_path, index=False)
print(f"Clustered music data saved to {output_path}")

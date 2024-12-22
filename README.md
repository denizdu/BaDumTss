# BaDumTss 🎵

Bu proje, belirli bir şarkı listesi üzerinden müzik analizi yapmayı ve ilgili sonuçları derlemeyi amaçlayan bir Python uygulamasıdır. `BaDumTss`, şarkıları YouTube'dan indirip analiz eder ve elde edilen sonuçları JSON formatında saklar. Proje, müzik analizi için birden fazla modül kullanır ve veri işleme süreçlerini otomatize eder.

## 📁 Proje Dizini

### Ana Dizin
- **scripts/**: Uygulamanın temel fonksiyonlarını içeren Python betikleri.
  - **fetch/**: Şarkıların indirilmesiyle ilgili fonksiyonlar.
  - **analysis/**: Müzik analizi süreçleri.
- **.gitignore**: Gereksiz dosyaların Git takibinden çıkarılması için yapılandırma dosyası.
- **README.md**: Projenin kullanımına yönelik açıklamalar.
- **requirements.txt**: Proje bağımlılıklarını listeleyen dosya.

## 🚀 Kurulum ve Kullanım

### 1. Gerekli Bağımlılıkların Kurulumu
Proje, bağımlılıkların sanal bir Python ortamında kurulmasını önerir. 

```bash
# Sanal ortam oluşturun
python -m venv venv

# Ortamı aktif hale getirin
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Gerekli bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 2. Çevresel Değişkenlerin Ayarlanması
Proje, bir `.env` dosyasına ihtiyaç duyar. Örnek bir `.env` dosyası aşağıdaki gibidir:

```env
DIR_DOWNLOAD=downloads
DIR_OUTPUT_FETCH=fetch_output
PLAYLIST_TOBE_ANALYZED=Ardisik
DIR_OUTPUT_ANALYSIS=analysis_output
```

### 3. Playlist'in Hazırlanması
`fetch_output` dizininde analiz edilecek şarkı listesi için bir JSON dosyası bulunmalıdır. Örnek:

`fetch_output/Ardisik_tracks.json`:
```json
[
  {"name": "Yol (feat. Sorgu)", "artist": "Farazi"},
  {"name": "Bazen (feat. Sansar Salvo)", "artist": "Çağrı Sinci"}
]
```

### 4. Projenin Çalıştırılması

Analiz sürecini başlatmak için aşağıdaki komutu çalıştırın:

```bash
python scripts/analysis/analysis.py
```

### 5. Analiz Sonuçları
Analiz sonuçları, `analysis_output` dizininde `analysis_output.json` dosyasında saklanır.

## 🛠 Kullanılan Teknolojiler
- **Python**: Temel programlama dili.
- **python-dotenv**: Çevresel değişkenlerin yönetimi.
- **yt-dlp**: YouTube'dan şarkı indirimi.
- **NumPy, SciPy**: Müzik analizi ve sinyal işleme.

## 🐞 Olası Sorunlar
- **`ModuleNotFoundError: No module named 'dotenv'`**:
  Bağımlılıklar doğru kurulmamış olabilir. `pip install -r requirements.txt` komutunu tekrar çalıştırın.
- **`Error in download_song_as_wav`**:
  İndirme işlemi sırasında bir hata oluştu. YouTube bağlantılarını ve `yt-dlp` kütüphanesinin düzgün çalıştığını kontrol edin.

## 🤝 Katkıda Bulunma
Projeye katkıda bulunmak isterseniz, şu adımları takip edebilirsiniz:

1. Bu depoyu forkladıktan sonra bir branch oluşturun:
   ```bash
   git checkout -b feature/your-feature
   ```
2. Değişikliklerinizi yapıp commit edin:
   ```bash
   git commit -m "Yeni özellik ekle"
   ```
3. Branch'i geri gönderin:
   ```bash
   git push origin feature/your-feature
   ```
4. Bir **Pull Request** açarak katkıda bulunun.

## 📄 Lisans
Bu proje MIT lisansı altında sunulmaktadır. Daha fazla bilgi için `LICENSE` dosyasını inceleyebilirsiniz.

## 📬 İletişim
Sorularınız veya önerileriniz için [denizdu](https://github.com/denizdu) ile iletişime geçebilirsiniz. Şaka yaptım, arayıp sormayın, ağlayarak günlüğünüze yazarsınız.

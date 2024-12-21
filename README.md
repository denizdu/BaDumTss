# BaDumTss Projesi

Bu proje, Spotify çalma listelerini indirip analiz etmek için hazırlanmış bir Python uygulamasıdır. Çalma listelerindeki şarkıları YouTube üzerinden indirir ve analiz işlemleri için düzenler.

## Özellikler
- Spotify çalma listelerini JSON formatında dışa aktarır.
- Belirli bir çalma listesindeki şarkıları YouTube üzerinden indirir.
- Tüm dizin ve path yapılandırmaları `.env` dosyasından yönetilir.

## Gereksinimler
- Python 3.8 veya üstü
- Spotify API için kayıtlı bir uygulama ve API anahtarları

### Kullanılan Kütüphaneler
- `spotipy`: Spotify API ile etkileşim
- `pytube`: YouTube üzerinden şarkı indirme
- `python-dotenv`: `.env` dosyasını yükleme ve yönetme

## Kurulum
1. Bu projeyi klonlayın veya indirin.
2. Sanal bir ortam oluşturun ve aktifleştirin:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows için: venv\Scripts\activate
   ```
3. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. Proje kök dizininde bir `.env` dosyası oluşturun ve şu bilgileri girin:
   ```env
   PROJECT_ROOT=/path/to/BaDumTss

   DIR_DOWNLOAD=${PROJECT_ROOT}/downloads
   DIR_OUTPUT_ANALYSIS=${PROJECT_ROOT}/output/analysis
   DIR_OUTPUT_FETCH=${PROJECT_ROOT}/output/fetch
   DIR_OUTPUT_MODEL=${PROJECT_ROOT}/output/model
   DIR_OUTPUT_SAMPLING=${PROJECT_ROOT}/output/sampling

   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   REDIRECT_URI=http://localhost:8080
   ```

## Kullanım
### 1. Spotify Fetch
Spotify çalma listelerini JSON formatında dışa aktarmak için:
```bash
python scripts/fetch/spotify_fetch.py
```

### 2. YouTube Fetch
Belirli bir çalma listesindeki şarkıları indirmek için:
```bash
python scripts/fetch/youtube_fetch.py
```
Komut çalıştırıldığında çalma listesi adını girmeniz istenir.

## Dizin Yapısı
```
BaDumTss/
├── scripts/
│   ├── fetch/
│   │   ├── spotify_fetch.py
│   │   ├── youtube_fetch.py
├── output/
│   ├── fetch/
│   ├── analysis/
├── downloads/
├── .env
├── requirements.txt
```

## Hata Ayıklama
- `.env` dosyasının doğru şekilde yapılandırıldığından emin olun.
- Python kütüphanelerinin kurulu olduğundan emin olun:
  ```bash
  pip list
  ```

## Lisans
Bu proje MIT lisansı altında sunulmaktadır.

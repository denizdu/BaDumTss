# ENV Kurulumu

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip freeze > requirements.txt


---

### 1. **Python Virtual Environment Kurulumu**
1. **Python Versiyonunu Kontrol Et**:
   Python'un yüklü olduğundan ve sürümünün 3.6 veya daha yeni olduğundan emin ol:
   ```bash
   python --version
   ```
   veya
   ```bash
   python3 --version
   ```

2. **Virtual Environment Oluştur**:
   Proje dizinine git ve bir virtual environment oluştur:
   ```bash
   python -m venv venv
   ```
   Bu komut, aynı dizin içinde `venv` adında bir klasör oluşturur.

3. **Virtual Environment Aktifleştirme**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Aktif Olduğunu Kontrol Et**:
   Terminalde, sanal ortamın aktif olduğunu anlamak için prompt'ta `(venv)` ibaresini görmelisin.

---

### 2. **Gerekli Kütüphaneleri Yükleme**
1. **Projenin Gereksinimlerini Belirt**:
   Eğer bir `requirements.txt` dosyan varsa, şu komutla tüm bağımlılıkları yükle:
   ```bash
   pip install -r requirements.txt
   ```
   Eğer yoksa, bu projede temel olarak şu kütüphaneleri yüklemen gerekecek:
   ```bash
   pip install spotipy pytube
   ```

2. **Yüklenen Paketleri Kontrol Et**:
   Kurulumları doğrulamak için:
   ```bash
   pip list
   ```

---

### 3. **Proje Yapılandırması**
1. **Proje Dosyalarını Düzenle**:
   - Scriptlerini proje klasörüne yerleştir.
   - Çalışma dizinini netleştir.

2. **Gerekli API Bilgilerini Ayarla**:
   - Spotify API için bir `client_id` ve `client_secret` belirle.
   - Bu bilgileri `analysis.py` içinde veya `.env` dosyasına kaydet.

---

### 4. **Çalıştırma ve Test**
1. **Sanal Ortamda Çalıştır**:
   Sanal ortamı aktif hale getir ve scripti çalıştır:
   ```bash
   python analysis.py
   ```

2. **Sorun Çıkarsa Logları İncele**:
   Hatalarla karşılaşırsan, Python’un hata mesajlarını dikkatlice oku ve çözüm için yönlendirme iste.

---

### 5. **Kapanış ve Temizlik**
1. **Sanal Ortamı Deaktive Et**:
   Çalışman bittiğinde, sanal ortamı kapatabilirsin:
   ```bash
   deactivate
   ```

2. **Yedekleme**:
   Proje dosyalarını ve bağımlılık listesini (`pip freeze > requirements.txt`) yedekle.

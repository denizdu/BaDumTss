import os
import subprocess
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv(dotenv_path="C://Users//denizdu//OneDrive//Masaüstü//BaDumTss//.env")

# Dizinler
DIR_DOWNLOAD = os.getenv("DIR_DOWNLOAD")
COOKIES_FILE = "C://Users//denizdu//OneDrive//Masaüstü//BaDumTss//cookies.txt"  # Çerez dosyası yolu

def download_song_as_wav(search_query, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    try:
        print(f"Downloading {search_query}...")

        # İndirme komutu
        command = [
            "yt-dlp",
            "-x", "--audio-format", "wav",
            "--output", f"{output_dir}/%(title)s.%(ext)s",
            f"ytsearch1:{search_query}"
        ]

        # Sadece `cookies.txt` kullan
        if os.path.exists(COOKIES_FILE):
            print(f"Using cookies from: {COOKIES_FILE}")
            command.extend(["--cookies", COOKIES_FILE])
        else:
            print("Error: No cookies.txt file found. Please create it first.")
            return None

        # Komutu çalıştır
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Başarılı indirme
        if result.returncode == 0:
            print(f"Successfully downloaded: {search_query}")

            # İndirilen dosyanın tam yolunu bul
            for file_name in os.listdir(output_dir):
                if search_query.split(" ")[0] in file_name:
                    file_path = os.path.join(output_dir, file_name)
                    print(f"Filepath: {file_path}")
                    return file_path

            print("Downloaded file not found.")
            return None
        else:
            print(f"Error downloading {search_query}: {result.stderr.decode('utf-8')}")
            return None
    except Exception as e:
        print(f"Error in download_song_as_wav: {e}")
        return None

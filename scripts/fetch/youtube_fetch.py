import os
import subprocess
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv(dotenv_path="C://Users//denizdu//OneDrive//Masaüstü//BaDumTss//.env")

# Dizinler
DIR_DOWNLOAD = os.getenv("DIR_DOWNLOAD")

def download_song_as_wav(search_query, output_dir, cookies=None, browser="edge", profile="Default"):
    os.makedirs(output_dir, exist_ok=True)
    try:
        print(f"Downloading {search_query}...")
        command = [
            "yt-dlp",
            "-x", "--audio-format", "wav",
            "--output", f"{output_dir}/%(title)s.%(ext)s",
            f"ytsearch1:{search_query}"
        ]

        if cookies:
            command.extend(["--cookies", cookies])  # Manuel çerez dosyasını belirt
        else:
            command.extend(["--cookies-from-browser", f"{browser}:{profile}"])  # Tarayıcı ve profil kullan

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

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

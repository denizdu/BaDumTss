import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

cookie_setting = os.getenv("YOUTUBE_COOKIES_FILE", "cookies.txt")
cookie_path = Path(cookie_setting).expanduser()
COOKIES_FILE = cookie_path if cookie_path.is_absolute() else PROJECT_ROOT / cookie_path

def download_song_as_wav(search_query, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Downloading {search_query}...")

        # İndirme komutu
        command = [
            "yt-dlp",
            "-x", "--audio-format", "wav",
            "--output", str(output_dir / "%(title)s.%(ext)s"),
            "--print", "after_move:filepath",
            f"ytsearch1:{search_query}"
        ]

        # Cookie isteğe bağlıdır; yalnızca kullanıcının yetkili içeriğinde gerekirse kullanılır.
        if COOKIES_FILE.exists():
            print(f"Using cookies from: {COOKIES_FILE}")
            command.extend(["--cookies", str(COOKIES_FILE)])
        else:
            print("No cookies file configured; continuing without cookies.")

        # Komutu çalıştır
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Başarılı indirme
        if result.returncode == 0:
            print(f"Successfully downloaded: {search_query}")

            reported_paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            if reported_paths:
                file_path = Path(reported_paths[-1])
                if file_path.exists():
                    print(f"Filepath: {file_path}")
                    return str(file_path)

            print("Downloaded file not found.")
            return None
        else:
            print(f"Error downloading {search_query}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error in download_song_as_wav: {e}")
        return None

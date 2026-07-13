import os
import subprocess
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
COOKIES_FILE = None


def configured_cookie_file(environment=None):
    if COOKIES_FILE is not None:
        return Path(COOKIES_FILE)
    environment = os.environ if environment is None else environment
    cookie_setting = environment.get("YOUTUBE_COOKIES_FILE", "cookies.txt")
    cookie_path = Path(cookie_setting).expanduser()
    return cookie_path if cookie_path.is_absolute() else PROJECT_ROOT / cookie_path

def download_song_as_wav(search_query, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Downloading {search_query}...")

        # Download command.
        command = [
            "yt-dlp",
            "-x", "--audio-format", "wav",
            "--output", str(output_dir / "%(title)s.%(ext)s"),
            "--print", "after_move:filepath",
            f"ytsearch1:{search_query}"
        ]

        # Cookies are optional and only used for content the user is authorized to access.
        cookie_file = configured_cookie_file()
        if cookie_file.exists():
            print(f"Using cookies from: {cookie_file}")
            command.extend(["--cookies", str(cookie_file)])
        else:
            print("No cookies file configured; continuing without cookies.")

        # Run the command.
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Successful download.
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

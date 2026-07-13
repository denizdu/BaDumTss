from types import SimpleNamespace

from scripts.fetch import youtube_fetch


def test_download_continues_without_cookie_file(tmp_path, monkeypatch):
    downloaded_file = tmp_path / "downloaded.wav"

    def fake_run(command, **kwargs):
        downloaded_file.write_bytes(b"wav")
        assert "--cookies" not in command
        return SimpleNamespace(returncode=0, stdout=str(downloaded_file), stderr="")

    monkeypatch.setattr(youtube_fetch, "COOKIES_FILE", tmp_path / "missing-cookies.txt")
    monkeypatch.setattr(youtube_fetch.subprocess, "run", fake_run)

    result = youtube_fetch.download_song_as_wav("authorized test audio", tmp_path)

    assert result == str(downloaded_file)


def test_download_uses_reported_output_path(tmp_path, monkeypatch):
    downloaded_file = tmp_path / "title unrelated to query.wav"
    cookie_file = tmp_path / "cookies.txt"
    cookie_file.write_text("# Netscape HTTP Cookie File", encoding="utf-8")

    def fake_run(command, **kwargs):
        downloaded_file.write_bytes(b"wav")
        assert command[command.index("--cookies") + 1] == str(cookie_file)
        return SimpleNamespace(returncode=0, stdout=str(downloaded_file), stderr="")

    monkeypatch.setattr(youtube_fetch, "COOKIES_FILE", cookie_file)
    monkeypatch.setattr(youtube_fetch.subprocess, "run", fake_run)

    result = youtube_fetch.download_song_as_wav("different query", tmp_path)

    assert result == str(downloaded_file)

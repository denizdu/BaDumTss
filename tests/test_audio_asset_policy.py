import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AUDIO_EXTENSIONS = {".aac", ".flac", ".m4a", ".mp3", ".ogg", ".wav"}


def test_repository_does_not_track_audio_assets():
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
    )
    tracked_files = result.stdout.decode("utf-8").split("\0")
    audio_files = [
        path for path in tracked_files if Path(path).suffix.lower() in AUDIO_EXTENSIONS
    ]
    assert not audio_files, f"Audio assets must remain external: {audio_files}"


def test_asset_manifest_example_has_required_metadata():
    manifest_path = PROJECT_ROOT / "sample" / "assets.example.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == 1
    assert manifest["assets"]
    required_fields = {
        "id",
        "role",
        "environment_variable",
        "source",
        "license",
        "sha256",
    }
    for asset in manifest["assets"]:
        assert required_fields <= asset.keys()


def test_reaper_script_uses_configured_sample_paths():
    script = (PROJECT_ROOT / "scripts" / "creation" / "creation.lua").read_text(
        encoding="utf-8"
    )

    assert "BADUMTSS_KICK_SAMPLE" in script
    assert "BADUMTSS_SNARE_SAMPLE" in script
    assert "BADUMTSS_HIHAT_SAMPLE" in script
    assert "Cymatics" not in script

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _package_names(requirements_file):
    names = set()
    for raw_line in requirements_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#", "-r")):
            continue
        names.add(line.split("==", 1)[0].lower())
    return names


def test_runtime_manifest_contains_only_direct_dependencies():
    runtime_packages = _package_names(PROJECT_ROOT / "requirements.txt")

    assert runtime_packages == {
        "joblib",
        "librosa",
        "numpy",
        "pandas",
        "python-dotenv",
        "scikit-learn",
        "scipy",
        "spotipy",
        "yt-dlp",
    }


def test_test_tools_are_kept_out_of_runtime_manifest():
    runtime_packages = _package_names(PROJECT_ROOT / "requirements.txt")
    development_packages = _package_names(PROJECT_ROOT / "requirements-dev.txt")

    assert "pytest" not in runtime_packages
    assert "pytest-cov" not in runtime_packages
    assert {"pytest", "pytest-cov"} <= development_packages


def test_removed_heavy_frameworks_do_not_return():
    runtime_packages = _package_names(PROJECT_ROOT / "requirements.txt")

    assert runtime_packages.isdisjoint({"tensorflow", "tensorflow-intel", "torch"})

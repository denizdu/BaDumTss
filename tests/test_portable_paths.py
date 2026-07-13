from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
FORBIDDEN_PATH_FRAGMENTS = (
    "C:/Users/",
    "C://Users//",
    "C:\\Users\\",
    "OneDrive",
    "Masaüstü",
)


def test_scripts_do_not_contain_user_specific_absolute_paths():
    source_files = [
        path
        for path in SCRIPTS_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".py", ".lua", ".bat"}
    ]

    violations = {}
    for path in source_files:
        content = path.read_text(encoding="utf-8")
        matches = [fragment for fragment in FORBIDDEN_PATH_FRAGMENTS if fragment in content]
        if matches:
            violations[str(path.relative_to(PROJECT_ROOT))] = matches

    assert not violations, violations

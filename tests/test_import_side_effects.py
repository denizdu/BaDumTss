import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import analysis
from scripts.fetch.cookie_converter import convert_cookies


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_core_modules_import_without_configuration_or_filesystem_writes(tmp_path):
    environment = os.environ.copy()
    for variable in (
        "DIR_DOWNLOAD",
        "DIR_OUTPUT_FETCH",
        "DIR_OUTPUT_ANALYSIS",
        "DIR_OUTPUT_MODEL",
        "PLAYLIST_TOBE_ANALYZED",
        "SPOTIFY_CLIENT_ID",
        "SPOTIFY_CLIENT_SECRET",
        "REDIRECT_URI",
    ):
        environment.pop(variable, None)
    environment["PYTHONPATH"] = os.pathsep.join(
        [
            str(PROJECT_ROOT),
            str(PROJECT_ROOT / "scripts" / "analysis"),
            str(PROJECT_ROOT / "scripts" / "model"),
        ]
    )
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import analysis; import model; "
                "import scripts.fetch.spotify_fetch; "
                "import scripts.fetch.youtube_fetch; "
                "import scripts.fetch.cookie_converter"
            ),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert list(tmp_path.iterdir()) == []


def test_analysis_configuration_is_validated_only_when_requested():
    with pytest.raises(RuntimeError, match="PLAYLIST_TOBE_ANALYZED"):
        analysis.load_analysis_config({})


def test_cookie_conversion_runs_only_after_an_explicit_call(tmp_path):
    source = tmp_path / "cookies.json"
    destination = tmp_path / "cookies.txt"
    source.write_text(
        json.dumps(
            [
                {
                    "domain": ".example.com",
                    "path": "/",
                    "secure": True,
                    "expirationDate": 1234.9,
                    "name": "session",
                    "value": "authorized-test-value",
                }
            ]
        ),
        encoding="utf-8",
    )

    result = convert_cookies(source, destination)

    assert result == destination
    assert destination.read_text(encoding="utf-8").splitlines() == [
        "# Netscape HTTP Cookie File",
        ".example.com\tTRUE\t/\tTRUE\t1234\tsession\tauthorized-test-value",
    ]

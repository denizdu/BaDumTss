import os
import sys
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "analysis"))
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "creation"))

TEST_OUTPUT = Path(tempfile.gettempdir()) / "badumtss-tests"
os.environ.setdefault("DIR_DOWNLOAD", str(TEST_OUTPUT / "downloads"))
os.environ.setdefault("DIR_OUTPUT_FETCH", str(TEST_OUTPUT / "fetch"))
os.environ.setdefault("DIR_OUTPUT_ANALYSIS", str(TEST_OUTPUT / "analysis"))
os.environ.setdefault("PLAYLIST_TOBE_ANALYZED", "test-playlist")

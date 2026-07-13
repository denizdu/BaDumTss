@echo off
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Run: python -m venv .venv
    exit /b 1
)

call ".venv\Scripts\activate.bat"
python -m pip install -r requirements.txt
set PYTHONPATH=.
python scripts\fetch\spotify_fetch.py
python scripts\fetch\cookie_converter.py
python scripts\analysis\analysis.py
python scripts\model\model.py

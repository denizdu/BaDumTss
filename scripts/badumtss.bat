C:\Users\denizdu\OneDrive\Masaüstü\BaDumTss\venv\Scripts\activate.bat
pip install -r requirements.txt
set PYTHONPATH=.
python scripts\fetch\spotify_fetch.py
python scripts\fetch\cookie_converter.py
python scripts\analysis\analysis.py
python scripts\model\model.py

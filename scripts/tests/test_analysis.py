# tests/test_analysis.py
import pytest
from analysis import analyze_data

def test_analyze_data_success():
    data = [1, 2, 3, 4, 5]
    result = analyze_data(data)
    assert result == 3.0

def test_analyze_data_empty():
    with pytest.raises(ValueError, match="Data list is empty"):
        analyze_data([])

# tests/test_fetch.py
import pytest
from unittest.mock import patch
from fetch import fetch_data

def test_fetch_data_success():
    mock_response = {"key": "value"}

    with patch('fetch.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = fetch_data('http://example.com')
        assert result == mock_response

def test_fetch_data_http_error():
    with patch('fetch.requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        with pytest.raises(requests.exceptions.HTTPError):
            fetch_data('http://example.com')

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from so_challenge.data_fetcher import fetch_data
from requests.exceptions import RequestException

@patch("so_challenge.data_fetcher.requests.get")
@patch("so_challenge.data_fetcher.pd.DataFrame.to_csv")
def test_fetch_data_returns_correct_dataframe(mock_to_csv, mock_get):
    """Test successful data fetch returns correct DataFrame shape and columns."""
    # Mock API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "items": [
            {"year_month": "2024-01", "question_count": 100},
            {"year_month": "2024-02", "question_count": 150}
        ]
    }
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    df = fetch_data(cache_path="dummy_cache.csv")

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["year_month", "question_count"]
    assert len(df) == 2
    assert mock_get.called
    assert mock_to_csv.called

@patch("so_challenge.data_fetcher.os.path.exists")
@patch("so_challenge.data_fetcher.pd.read_csv")
@patch("so_challenge.data_fetcher.requests.get")
def test_fetch_data_uses_cache(mock_get, mock_read_csv, mock_exists):
    """Test that cached data is returned without network call."""
    mock_exists.return_value = True
    mock_read_csv.return_value = pd.DataFrame({
        "year_month": ["2024-01"],
        "question_count": [100]
    })

    df = fetch_data(cache_path="existing_cache.csv")

    assert not mock_get.called
    assert len(df) == 1
    assert df.iloc[0]["year_month"] == "2024-01"

@patch("so_challenge.data_fetcher.requests.get")
@patch("so_challenge.data_fetcher.time.sleep") # Mock sleep to speed up tests
def test_fetch_data_retries_on_error(mock_sleep, mock_get):
    """Test that network error triggers retry logic."""
    # First call fails, second call succeeds
    mock_fail = MagicMock()
    mock_fail.side_effect = RequestException("Network error")
    
    mock_success = MagicMock()
    mock_success.json.return_value = {"items": [{"year_month": "2024-01", "question_count": 100}]}
    mock_success.status_code = 200
    
    mock_get.side_effect = [RequestException("Network error"), mock_success]

    df = fetch_data(cache_path="dummy_cache.csv")

    assert mock_get.call_count == 2
    assert len(df) == 1
    assert mock_sleep.called

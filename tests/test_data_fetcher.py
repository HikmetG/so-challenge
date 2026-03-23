"""Tests for data_fetcher module."""
import pytest
from so_challenge import data_fetcher

def test_fetcher_exists():
    assert data_fetcher is not None

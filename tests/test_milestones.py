import pytest
from datetime import datetime
from so_challenge.milestones import get_milestones

def test_get_milestones_returns_list():
    """Test that get_milestones returns a list."""
    milestones = get_milestones()
    assert isinstance(milestones, list)
    assert len(milestones) > 0

def test_get_milestones_structure():
    """Test that each milestone has the required keys."""
    milestones = get_milestones()
    for m in milestones:
        assert "date" in m
        assert "label" in m
        assert isinstance(m["date"], str)
        assert isinstance(m["label"], str)

def test_get_milestones_valid_dates():
    """Test that milestone dates are in YYYY-MM-DD format."""
    milestones = get_milestones()
    for m in milestones:
        # This will raise ValueError if date string is invalid
        datetime.strptime(m["date"], "%Y-%m-%d")

def test_get_milestones_contains_key_events():
    """Test that key AI milestones are present."""
    milestones = get_milestones()
    labels = [m["label"] for m in milestones]
    
    # Check for ChatGPT
    assert any("ChatGPT" in label for label in labels)
    # Check for GPT-4
    assert any("GPT-4" in label for label in labels)

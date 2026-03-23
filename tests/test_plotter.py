import pytest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
from so_challenge.plotter import plot_questions

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "year_month": ["2024-01", "2024-02", "2024-03"],
        "question_count": [100, 150, 120]
    })

@pytest.fixture
def sample_milestones():
    return [
        {"date": "2024-02-15", "label": "Milestone A"}
    ]

@patch("so_challenge.plotter.plt.subplots")
def test_plot_questions_creates_figure(mock_subplots, sample_df, sample_milestones):
    """Test that plot_questions creates a figure and axes."""
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)

    fig, ax = plot_questions(sample_df, sample_milestones)

    assert mock_subplots.called
    assert fig == mock_fig
    assert ax == mock_ax

def test_plot_questions_has_labels(sample_df, sample_milestones):
    """Test that the plot has correct labels and title."""
    with patch("so_challenge.plotter.plt.subplots") as mock_subplots:
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)

        plot_questions(sample_df, sample_milestones)

        mock_ax.set_xlabel.assert_called_with("Date")
        mock_ax.set_ylabel.assert_called_with("Question Count")
        mock_ax.set_title.assert_called()
        mock_ax.legend.assert_called()

def test_plot_questions_plots_milestones(sample_df, sample_milestones):
    """Test that milestones are plotted as vertical lines."""
    with patch("so_challenge.plotter.plt.subplots") as mock_subplots:
        _, mock_ax = mock_subplots.return_value = (MagicMock(), MagicMock())

        plot_questions(sample_df, sample_milestones)

        # Check if axvline was called for the milestone
        assert mock_ax.axvline.called
        args, kwargs = mock_ax.axvline.call_args
        # The first argument should be the date (or transformed date)
        assert "label" in kwargs
        assert kwargs["label"] == "Milestone A"

def test_plot_questions_empty_df():
    """Test handling of empty DataFrame."""
    empty_df = pd.DataFrame(columns=["year_month", "question_count"])
    with pytest.raises(ValueError, match="DataFrame is empty"):
        plot_questions(empty_df, [])

# so-challenge

Project for collecting, analyzing, and visualizing StackOverflow data, specifically focusing on the impact of AI milestones on question volume between 2010 and 2025.

## Project Structure

- `src/so_challenge/data_fetcher.py`: Data collection from Stack Exchange API or SEDE.
- `src/so_challenge/plotter.py`: Visualization and plotting logic.
- `src/so_challenge/milestones.py`: Definition of AI-related event milestones.
- `tests/`: Project test suite.
- `diary/`: Record of AI interactions.

## Setup

This project uses `uv` for dependency management.

```bash
uv sync
```

## Running Tests

```bash
uv run pytest
```

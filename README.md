# so-challenge

Project for collecting, analyzing, and visualizing StackOverflow data, specifically focusing on the impact of AI milestones on question volume between 2010 and 2025.

## Project Structure

- `src/so_challenge/data_fetcher.py`: Data collection from Stack Exchange API or SEDE.
- `src/so_challenge/plotter.py`: Visualization and plotting logic.
- `src/so_challenge/milestones.py`: Definition of AI-related event milestones.
- `tests/`: Project test suite.
- `diary/`: Record of AI interactions.

## Usage

This project uses `uv` for dependency management.

### Setup

```bash
uv sync
```

### Running the Application

To fetch data (or load from cache) and generate the visualization:

```bash
uv run python -m so_challenge.main
```

The resulting plot will be saved as `so_questions_plot.png`.

### Running Tests

```bash
uv run pytest
```

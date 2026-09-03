# AI Search Maze

A polished implementation of the Colab maze-search assignment. It exposes breadth-first search, depth-first search, and A* behind one deterministic API and keeps algorithm metrics separate from rendering.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
python -m maze_search.cli --algorithm astar
```

Cells use `(row, column)` coordinates. Walls are excluded from expansion; A* uses Manhattan distance and returns an optimal path for unit-cost movement.


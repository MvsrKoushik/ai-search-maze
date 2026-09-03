import argparse
from .search import astar, bfs, dfs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", choices=("bfs", "dfs", "astar"), default="astar")
    args = parser.parse_args()
    walls = {(1, 1), (1, 2), (2, 2)}
    result = {"bfs": bfs, "dfs": dfs, "astar": astar}[args.algorithm](4, 5, (0, 0), (3, 4), walls)
    print({"path": result.path, "cost": result.cost, "expanded": result.expanded})


if __name__ == "__main__":
    main()


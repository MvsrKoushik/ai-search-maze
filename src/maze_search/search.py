from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from collections import deque
from typing import Callable, Iterable

Point = tuple[int, int]


@dataclass(frozen=True)
class SearchResult:
    path: tuple[Point, ...]
    expanded: int

    @property
    def cost(self) -> int:
        return max(0, len(self.path) - 1)


def _neighbors(point: Point, rows: int, cols: int, walls: set[Point]) -> Iterable[Point]:
    r, c = point
    for nxt in ((r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)):
        if 0 <= nxt[0] < rows and 0 <= nxt[1] < cols and nxt not in walls:
            yield nxt


def _path(parent: dict[Point, Point | None], goal: Point) -> tuple[Point, ...]:
    if goal not in parent:
        return ()
    out: list[Point] = []
    cur: Point | None = goal
    while cur is not None:
        out.append(cur)
        cur = parent[cur]
    return tuple(reversed(out))


def _uninformed(rows: int, cols: int, start: Point, goal: Point, walls: set[Point], *, depth_first: bool) -> SearchResult:
    frontier = [start] if depth_first else deque([start])
    parent: dict[Point, Point | None] = {start: None}
    expanded = 0
    while frontier:
        current = frontier.pop() if depth_first else frontier.popleft()
        expanded += 1
        if current == goal:
            break
        candidates = list(_neighbors(current, rows, cols, walls))
        if depth_first:
            candidates.reverse()
        for nxt in candidates:
            if nxt not in parent:
                parent[nxt] = current
                frontier.append(nxt)
    return SearchResult(_path(parent, goal), expanded)


def bfs(rows: int, cols: int, start: Point, goal: Point, walls: set[Point] | None = None) -> SearchResult:
    return _uninformed(rows, cols, start, goal, walls or set(), depth_first=False)


def dfs(rows: int, cols: int, start: Point, goal: Point, walls: set[Point] | None = None) -> SearchResult:
    return _uninformed(rows, cols, start, goal, walls or set(), depth_first=True)


def astar(rows: int, cols: int, start: Point, goal: Point, walls: set[Point] | None = None,
          heuristic: Callable[[Point, Point], float] | None = None) -> SearchResult:
    blocked = walls or set()
    h = heuristic or (lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]))
    serial = count()
    queue: list[tuple[float, int, Point]] = [(h(start, goal), next(serial), start)]
    parent: dict[Point, Point | None] = {start: None}
    best = {start: 0}
    expanded = 0
    while queue:
        _, _, current = heappop(queue)
        expanded += 1
        if current == goal:
            break
        for nxt in _neighbors(current, rows, cols, blocked):
            score = best[current] + 1
            if score < best.get(nxt, 10**18):
                best[nxt], parent[nxt] = score, current
                heappush(queue, (score + h(nxt, goal), next(serial), nxt))
    return SearchResult(_path(parent, goal), expanded)


from maze_search import astar, bfs


def test_astar_matches_bfs_shortest_path():
    walls = {(1, 1), (1, 2), (2, 2)}
    assert astar(4, 5, (0, 0), (3, 4), walls).cost == bfs(4, 5, (0, 0), (3, 4), walls).cost


def test_unreachable_goal():
    assert not bfs(2, 2, (0, 0), (1, 1), {(0, 1), (1, 0)}).path


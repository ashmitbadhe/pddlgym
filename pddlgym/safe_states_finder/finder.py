from typing import List, Tuple, Set, Mapping, Dict

from eoDTG import eoDTG, eoDTG_edge, eoDTG_path

"""
    BFS algorithm for detecting a path in a graph.
"""


def bfs_any_path_existance_search(graph: eoDTG, start_value: int, end_value: int) -> bool:
    visited = [False] * len(graph.nodes)

    frontier = set()
    frontier.add(start_value)
    visited[start_value] = True

    while not visited[end_value] and len(frontier) > 0:
        new_frontier = set()
        for index in frontier:
            for edge in graph.nodes[index].edges:
                visited[edge.node.value] = True
                if visited[end_value]:
                    return True
                new_frontier.add(edge.node.value)
        frontier = new_frontier

    return visited[end_value]


"""
    BFS algorithm for any sortest path in a graph.
"""


def bfs_shortest_path_search(graph: eoDTG, start_value: int, end_value: int) -> eoDTG_path:
    visited = [False] * len(graph.nodes)

    frontier: Set[Tuple[eoDTG_path, int]] = set()
    frontier.add((eoDTG_path(), start_value))
    visited[start_value] = True

    if visited[end_value]:
        return eoDTG_path()

    while len(frontier) > 0:
        new_frontier: Set[Tuple[eoDTG_path, int]] = set()
        for (path, index) in frontier:
            for edge in graph.nodes[index].edges:
                visited[edge.node.value] = True
                if edge.node.value == end_value:
                    return eoDTG_path(path, edge)
                new_frontier.add((eoDTG_path(path, edge), edge.node.value))
        frontier = new_frontier

    return None


"""
    DFS algorithm for finding all paths.
"""


def dfs_all_paths_search(graph: eoDTG, start_value: int, end_value: int, previous: eoDTG_path = eoDTG_path(),
                         init: int = -1) -> List[eoDTG_path]:
    initial_node = init if init != -1 else start_value
    paths: List[eoDTG_path] = []

    if start_value == end_value:
        paths.append(previous)
    else:
        for edge in graph.nodes[start_value].edges:
            if edge not in previous.path and edge.node.value != init:
                paths += dfs_all_paths_search(graph, edge.node.value, end_value, eoDTG_path(previous, edge),
                                              initial_node)

    return paths
from __future__ import annotations

# Week 9 Solutions -- Adjacency Matrices and a Faster Reachability Check
#
# See ../../comp-271-su26/week09/graphs.py for the stub version and
# ../../comp-271-su26/week09/week09-assignment.md for the full writeup.
# This file is the private counterpart of graphs.py: everything through
# naive_reachability is unchanged from the stub (it was already
# complete there), and better_reachability is filled in below.

AdjacencyList = list[list[int]]
AdjacencyMatrix = list[list[int]]

graph: AdjacencyList = [
        [1, 2, 3],      # neighbors for vertex 0
        [0, 6],         # neighbors for vertex 1
        [0, 3, 4],      # neighbors for vertex 2
        [2, 0],         # neighbors for vertex 3
        [2, 6],         # neighbors for vertex 4
        [7],            # neighbors for vertex 5
        [1, 4],         # neighbors for vertex 6
        [5]             # neighbors for vertex 7
        ]


def produce_adjacency_matrix(adjacency_list: AdjacencyList) -> AdjacencyMatrix:
    vertex_count = len(adjacency_list)

    # n x n, all zero to start: adjacency_matrix[i][j] == 1 will mean
    # an edge between vertex i and vertex j.
    adjacency_matrix: AdjacencyMatrix = [[0] * vertex_count for _ in range(vertex_count)]

    for vertex in range(vertex_count):
        for neighbor in adjacency_list[vertex]:
            # The graph is undirected, so an edge has to be recorded in
            # both directions -- otherwise the matrix would only be
            # symmetric by accident, depending on which vertex's
            # neighbor list happened to mention the edge first.
            adjacency_matrix[vertex][neighbor] = 1
            adjacency_matrix[neighbor][vertex] = 1

    return adjacency_matrix


def display_adjacency_matrix(adjacency_matrix: AdjacencyMatrix) -> None:
    vertex_count = len(adjacency_matrix)
    for row in range(vertex_count):
        for col in range(vertex_count):
            print(f"{adjacency_matrix[row][col]:5d}", end="")
        print()


def naive_reachability(graph: AdjacencyList, start: int, target: int) -> bool:
    """Return True if there is a path from start to target in the graph,
    False otherwise. This is a naive implementation: it always visits
    every vertex reachable from start before checking whether target
    was among them, even if target was the very first neighbor
    examined.
    """
    visited: list[int] = []

    # explore_next is used like a queue -- pop(0) always removes the
    # oldest entry -- so vertices are visited in breadth-first order,
    # nearest to start first. A vertex can be appended more than once
    # (two different visited vertices can share the same neighbor); the
    # not-in-visited check below is what makes a repeat harmless instead
    # of an infinite loop on a cyclic graph.
    explore_next: list[int] = [start]

    while len(explore_next) > 0:
        # pop(0) is O(n) -- the same front-of-list shifting cost as
        # week08's array-backed queue, since explore_next is a plain
        # list rather than the circular buffer from earlier this week.
        vertex_to_explore = explore_next.pop(0)

        if vertex_to_explore not in visited:
            # First time seeing this vertex: mark it visited before
            # queuing its neighbors, so a cycle back to it later is
            # skipped instead of requeued.
            visited.append(vertex_to_explore)

            for neighbor in graph[vertex_to_explore]:
                explore_next.append(neighbor)

    # Every vertex reachable from start is in visited by this point --
    # there was no early exit above, which is exactly what makes this
    # version naive.
    return target in visited


def better_reachability(graph: AdjacencyList, start: int, target: int) -> bool:
    """Return the same answer naive_reachability would return, for any
    graph, start, and target -- but without visiting every reachable
    vertex first when that is not necessary.
    """
    visited: list[int] = []
    explore_next: list[int] = [start]

    # The "second question" the assignment's docstring pointed at:
    # path_exists starts False and is the only new state this version
    # needs. Once it flips to True, the while condition below stops the
    # loop on its very next check, instead of draining explore_next the
    # way naive_reachability always does.
    path_exists: bool = False

    while len(explore_next) > 0 and not path_exists:
        vertex_to_explore = explore_next.pop(0)

        if vertex_to_explore not in visited:
            visited.append(vertex_to_explore)

            if vertex_to_explore == target:
                # Found it. Setting the flag here -- rather than a
                # `break` -- is what lets the while condition itself
                # end the loop, so control still leaves through the one
                # place the loop is allowed to end: its own condition.
                path_exists = True
            else:
                # Only queue neighbors when this vertex was not the
                # target -- once path_exists is True there is no reason
                # to keep growing explore_next with vertices that will
                # now never be looked at.
                for neighbor in graph[vertex_to_explore]:
                    explore_next.append(neighbor)

    # path_exists already holds the answer: True the moment target was
    # popped and marked visited, False if explore_next ran out first.
    return path_exists


def main() -> None:
    adjacency_matrix = produce_adjacency_matrix(graph)
    display_adjacency_matrix(adjacency_matrix)

    print(naive_reachability(graph, 0, 6))  # expected: True
    print(naive_reachability(graph, 0, 5))  # expected: False
    print(naive_reachability(graph, 0, 7))  # expected: False

    print(better_reachability(graph, 0, 6))  # expected: True
    print(better_reachability(graph, 0, 5))  # expected: False
    print(better_reachability(graph, 0, 7))  # expected: False

    # Edge cases from the assignment's Verification section.
    print(better_reachability(graph, 0, 0))  # expected: True -- start == target
    print(better_reachability(graph, 5, 7))  # expected: True -- isolated component
    print(better_reachability(graph, 7, 0) == naive_reachability(graph, 7, 0))  # expected: True


if __name__ == "__main__":
    main()

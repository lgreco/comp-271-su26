from __future__ import annotations

# A list of lists representing the
# adjacency of a graph

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

    Contract:
    - Same signature, same meaning, same return value as
      naive_reachability for every input.
    - Must be able to stop as soon as the answer is already known,
      rather than only stopping once explore_next runs empty on its
      own.

    naive_reachability's while loop asks exactly one question every
    time around: is there still something left in explore_next? That
    question alone can never produce an early stop -- it has no way to
    know that the answer to the whole function was already decided
    three iterations ago. What second question could the loop condition
    ask alongside it, so that becoming true partway through is enough
    to end the loop right there? What is the smallest new piece of
    state -- initialized before the loop starts, changed in exactly one
    place inside it -- that second question would need to check?

    One return statement, at the very end.
    """
    pass


def main() -> None:
    adjacency_matrix = produce_adjacency_matrix(graph)
    display_adjacency_matrix(adjacency_matrix)

    print(naive_reachability(graph, 0, 6))  # expected: True
    print(naive_reachability(graph, 0, 5))  # expected: False
    print(naive_reachability(graph, 0, 7))  # expected: False

    print(better_reachability(graph, 0, 6))  # expected: True
    print(better_reachability(graph, 0, 5))  # expected: False
    print(better_reachability(graph, 0, 7))  # expected: False


if __name__ == "__main__":
    main()

# A list of lists representing the
# adjacency of a graph

graph = [
        [1, 2, 3],      # neighbors for vertex 0
        [0, 6],         # neighbors for vertex 1
        [0, 3, 4],      # neighbors for vertex 2
        [2, 0],         # neighbors for vertex 3
        [2 ,6],         # neighbors for vertex 4
        [7],            # neighbors for vertex 5
        [1, 4],         # neighbors for vertex 6
        [5]             # neighbors for vertex 7
        ]

def produce_adj_matrix(from_adj_list):
    n = len(from_adj_list)  # number of vertices
    # initialize the matrix as a sq. array of size n
    adj_matrix = [[ 0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        # process the i-th vertex:
        for j in from_adj_list[i]:
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
    return adj_matrix

am = produce_adj_matrix(graph)
m = len(am)
for row in range(m):
    for col in range(m):
        print(f"{am[row][col]:5d}", end = "")
    print()

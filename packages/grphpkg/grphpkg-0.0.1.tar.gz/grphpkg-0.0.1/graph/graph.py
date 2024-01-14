from __future__ import absolute_import
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, representation, adj_list=False):
        self.graph = defaultdict(set)
        self.__construct_graph(representation, adj_list)
    
    def __construct_graph(self, representation, adj_list):
        if isinstance(representation, list):
            if not adj_list:
                # Adjacency Matrix
                self.__construct_graph_from_matrix(representation)
            else:
                # Adjacency List
                self.__construct_graph_from_list(representation)
        else:
            raise ValueError("Invalid representation type. Please provide a 2D list (matrix) or a list (adjacency list).")
        
    def __construct_graph_from_matrix(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])

        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 1:
                    self.add_edge(i, j)

    def __construct_graph_from_list(self, adj_list):
        for u, neighbors in enumerate(adj_list):
            for v in neighbors:
                self.add_edge(u, v)

    def add_edge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)  # Make the graph bidirectional

    def print_graph(self):
        for k, v in self.graph.items():
            print(f"{k} -> {list(v)}")

    def bfs(self, start, callback):
        """Perform BFS and callback operation on each node

        * start: Starting node
        * callback: Your custom function to perform your operation
        on each node
        """
        visited = set()
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                callback(vertex)
                visited.add(vertex)
                queue.extend(neighbour for neighbour in self.graph[vertex] if neighbour not in visited)

    def dfs(self, start, callback):
        """Perform DFS and callback operation on each node
        
        * start: Starting node
        * callback: Your custom function to perform your operation 
        on each node
        """
        visited = set()
        def dfs_recursive(vertex):
            visited.add(vertex)
            callback(vertex)
            for neighbour in self.graph[vertex]:
                if neighbour not in visited:
                    dfs_recursive(neighbour)

        dfs_recursive(start)

    def draw_graph(self):
        """Draw the graph for visualization
        """
        G = nx.Graph(self.graph)
        # Set positions for the nodes
        pos = nx.spring_layout(G)
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)
        # Draw edges
        nx.draw_networkx_edges(G, pos)
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
        # Display the graph
        plt.show()
import numpy as np
import matplotlib.pyplot as plt

class SGIA:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.grid = {}  # Dictionary to store vectors in grid cells

    def insert(self, vector, data):
        # Recursively insert vector into the grid
        self._insert_recursive(self.grid, vector, data, 0)

    def _insert_recursive(self, current_node, vector, data, depth):
        if depth == self.dimensions:
            if "data" in current_node:
                current_node["data"].append((vector, data))
            else:
                current_node["data"] = [(vector, data)]
        else:
            dimension = depth % self.dimensions
            if vector[dimension] < current_node.get("split", 0):
                if "left" not in current_node:
                    current_node["left"] = {}
                self._insert_recursive(current_node["left"], vector, data, depth + 1)
            else:
                if "right" not in current_node:
                    current_node["right"] = {}
                self._insert_recursive(current_node["right"], vector, data, depth + 1)

    def search(self, query_vector, k=1):
        # Find the k nearest neighbors to the query vector
        neighbors = []

        def _search_recursive(current_node, depth):
            if "data" in current_node:
                for vector, data in current_node["data"]:
                    distance = np.linalg.norm(np.array(vector) - np.array(query_vector))
                    neighbors.append((distance, data))
                    neighbors.sort()
                    if len(neighbors) > k:
                        neighbors.pop()
            dimension = depth % self.dimensions
            if query_vector[dimension] < current_node.get("split", 0):
                if "left" in current_node:
                    _search_recursive(current_node["left"], depth + 1)
            else:
                if "right" in current_node:
                    _search_recursive(current_node["right"], depth + 1)

        _search_recursive(self.grid, 0)
        return neighbors[:k]

    def display(self):
        # Create a scatter plot to visualize vectors
        vectors = []
        for node in self.grid:
            vectors.extend(self._get_vectors_in_node(self.grid[node]))

        vectors = np.array(vectors)
        x, y = vectors[:, 0], vectors[:, 1]

        plt.figure()
        plt.scatter(x, y, s=50, c='b', marker='o')

        # Create rectangles to visualize grid cells
        self._plot_grid(self.grid, self.dimensions, depth=0, x_min=0, x_max=10, y_min=0, y_max=10)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.title('Vector Index Visualization')
        plt.show()

    def _get_vectors_in_node(self, node):
        vectors = []
        if "data" in node:
            vectors.extend([vector for vector, _ in node["data"]])
        if "left" in node:
            vectors.extend(self._get_vectors_in_node(node["left"]))
        if "right" in node:
            vectors.extend(self._get_vectors_in_node(node["right"]))
        return vectors

    def _plot_grid(self, current_node, dimensions, depth, x_min, x_max, y_min, y_max):
        if depth == dimensions:
            plt.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min], 'k-', lw=0.5)
        else:
            split = current_node.get("split", 0)
            if depth % 2 == 0:
                self._plot_grid(current_node.get("left", {}), dimensions, depth + 1, x_min, split, y_min, y_max)
                self._plot_grid(current_node.get("right", {}), dimensions, depth + 1, split, x_max, y_min, y_max)
            else:
                self._plot_grid(current_node.get("left", {}), dimensions, depth + 1, x_min, x_max, y_min, split)
                self._plot_grid(current_node.get("right", {}), dimensions, depth + 1, x_min, x_max, split, y_max)
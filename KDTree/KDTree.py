import numpy as np
from sklearn.datasets import load_iris

class KDTree:
    def __init__(self, points, depth=0):
        self.depth = depth
        self.k = points.shape[1]  # Number of dimensions
        self.node = None
        self.left = None
        self.right = None

        if len(points) > 0:
            axis = depth % self.k
            points = points[points[:, axis].argsort()]
            median_index = len(points) // 2
            self.node = points[median_index]
            self.left = KDTree(points[:median_index], depth + 1)
            self.right = KDTree(points[median_index + 1:], depth + 1)

    def nearest_neighbor(self, point, best=None, best_dist=float("inf")):
        if self.node is None:
            return best, best_dist

        axis = self.depth % self.k
        dist = np.linalg.norm(self.node - point)

        if dist < best_dist:
            best = self.node
            best_dist = dist

        next_branch = self.left if point[axis] < self.node[axis] else self.right
        other_branch = self.right if point[axis] < self.node[axis] else self.left

        best, best_dist = next_branch.nearest_neighbor(point, best, best_dist)
        if abs(point[axis] - self.node[axis]) < best_dist:
            best, best_dist = other_branch.nearest_neighbor(point, best, best_dist)

        return best, best_dist

if __name__ == "__main__":
    # Load Iris dataset
    iris = load_iris()
    data = iris.data  # Only use features, not target labels

    # Build KD-Tree
    kd_tree = KDTree(data)

    # Test nearest neighbor search
    test_point = np.array([5.0, 3.0, 1.4, 0.2])  # Example point
    nearest, distance = kd_tree.nearest_neighbor(test_point)
    print("Test Point:", test_point)
    print("Nearest Point:", nearest)
    print("Distance:", distance)

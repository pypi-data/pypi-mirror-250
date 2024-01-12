import numpy as np

from src.base import Model


class KNN(Model):
    """
    K-nearest neighbors model.
    """
    def __init__(self, k: int = 3):
        """
        :param k: Number of neighbours.
        """

        self.k = k
        self._x = None
        self._y = None

    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Remember training data.
        :param x: Training data.
        :param y: Target feature.
        :return:
        """

        self._x = x
        self._y = y

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict k-nearest neighbors in vectorized form using Euclidian distance.
        :param x: Test data.
        :return: Test scores.
        """
        euclidian_distance = np.linalg.norm(self._x[:, np.newaxis] - x, axis=2)

        k_nearest = np.argsort(euclidian_distance, axis=0)[:self.k].transpose()  # Shape is (n_examples, k)
        counts = np.apply_along_axis(np.bincount, 1, self._y[k_nearest])
        scores = np.argmax(counts, axis=1)

        return scores





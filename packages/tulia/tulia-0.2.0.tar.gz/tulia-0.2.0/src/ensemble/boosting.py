from abc import abstractmethod

import numpy as np

from src.base import Model
from src.tree import DecisionTreeRegressor


class GradientBoostingRegressor(Model):
    """
    Gradient Boosting for regression
    """
    def __init__(
            self,
            learning_rate: float = 1e-3,
            n_steps: int = 100,
            max_depth: int = 3,
            min_samples_split: int = 2,
            max_features: float = 1.0
    ):
        """
        :param learning_rate: Learning rate for gradient descent.
        :param n_steps: Number of gradient descent steps.
        :param max_depth: Maximum depth of a decision tree.
        :param min_samples_split: Minimum number of samples to split data into right and left nodes.
        :param max_features: Percentage of features to use for training.
        """

        self.learning_rate = learning_rate
        self.n_steps = n_steps
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features

        self.trees = None
        self.constant_prediction = None

    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Train gradient boosting.
        :param x: Training data.
        :param y: Target feature.
        :return:
        """

        # Initial prediction
        self.constant_prediction = y.mean()

        prediction = self.constant_prediction
        self.trees = []
        for _ in range(self.n_steps):
            tree = DecisionTreeRegressor(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=self.max_features
            )

            residuals = prediction - y
            tree.fit(x, residuals)
            prediction = prediction + self.learning_rate * tree.predict(x)

            self.trees.append(tree)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict target feature using pretrained boosting trees.
        :param x: Test data.
        :return: Test predictions.
        """
        n_samples, _ = x.shape

        predictions = np.ones(shape=(n_samples,)) * self.constant_prediction

        for tree in self.trees:
            predictions = predictions + self.learning_rate * tree.predict(x)

        return predictions


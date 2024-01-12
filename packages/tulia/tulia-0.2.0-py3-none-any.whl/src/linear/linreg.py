import numpy as np

from .linear import _Linear


class LinearRegression(_Linear):
    """
    Vanilla Linear Regression.
    """

    def _calculate_error(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate mean-squared error.
        :param x: Training data.
        :param y: Targets.
        :return: Mean-squared error.
        """
        n_examples, _ = x.shape

        error = 1 / (n_examples * 2) * np.sum((x @ self.theta - y) ** 2)
        return error

    def _calculate_gradient(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Find gradient of a loss function with respect to theta.
        :param x: Training data.
        :param y: Targets.
        :return: Gradient with respect to theta.
        """
        n_examples, _ = x.shape

        dtheta = 1 / n_examples * np.sum((x @ self.theta - y)[:, np.newaxis] * x, axis=0)
        return dtheta

    def _calculate_predictions(self, x: np.ndarray) -> np.ndarray:
        """
        Make predictions for a regression linear model.
        :param x: Input data.
        :return: Predictions.
        """
        return x @ self.theta

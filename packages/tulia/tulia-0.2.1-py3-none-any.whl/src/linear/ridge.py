import numpy as np

from .linreg import LinearRegression


class RidgeRegression(LinearRegression):
    """
    Ridge Regression (L2)
    """

    def __init__(self, learning_rate: float = 1e-3, alpha: float = 1.0, n_steps: int = 1000, tol: float = 1e-5):
        """
        :param learning_rate: Learning rate for gradient descent.
        :param n_steps: Number of gradient descent steps.
        :param alpha: Regularization strength for L2.
        :param tol: Tolerance value to terminate a training process if function converges.
        """
        super().__init__(learning_rate=learning_rate, n_steps=n_steps, tol=tol)

        self.alpha = alpha

    def _calculate_error(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Find mean-squared error with L2 regularization.
        :param x: Training data.
        :param y: Targets.
        :return: Mean-squared error with L2 regularization.
        """
        n_examples, _ = x.shape

        mean_squared = 1 / (2 * n_examples) * np.sum((x @ self.theta - y) ** 2)
        regularization = self.alpha * np.sum(self.theta ** 2)

        error = mean_squared + regularization
        return error

    def _calculate_gradient(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Find gradient of a loss function with respect to theta.
        :param x: Training data.
        :param y: Targets.
        :return: Gradient with respect to theta.
        """
        n_examples, _ = x.shape

        dtheta_mean_squared = 1 / n_examples * np.sum((x @ self.theta - y)[:, np.newaxis] * x, axis=0)
        dtheta_regularization = self.alpha * 2 * np.sum(self.theta)

        dtheta = dtheta_mean_squared + dtheta_regularization
        return dtheta

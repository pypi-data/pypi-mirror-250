from abc import abstractmethod

import numpy as np

from src.base import Model


class _Linear(Model):
    def __init__(self, learning_rate: float = 1e-3, n_steps: int = 1000, tol: float = 1e-5):
        """
        :param learning_rate: Learning rate for gradient descent.
        :param n_steps: Number of gradient descent steps.
        :param tol: Tolerance value to terminate a training process if function converges.
        """
        self.learning_rate = learning_rate
        self.n_steps = n_steps
        self.tol = tol

        self.error = 0.0
        self.theta = None

    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Train linear model.
        :param x: Training data.
        :param y: Target feature.
        :return:
        """
        n_examples, n_features = x.shape

        # Consider bias by adding one extra parameter.
        self.theta = np.random.randn(n_features + 1)

        bias_term = np.ones((n_examples, 1))
        x_copy = np.concatenate((x, bias_term), axis=1)

        prev_error = None  # Stopping criteria of error is the same.
        for _ in range(self.n_steps):
            self.error = self._calculate_error(x_copy, y)

            # Terminate a training process if the function converges.
            if prev_error and np.isclose(self.error, prev_error, rtol=self.tol, atol=self.tol):
                return
            prev_error = self.error

            # Backpropagation over the loss function.
            dtheta = self._calculate_gradient(x_copy, y)

            # Update theta value by making gradient descent step.
            self.theta = self.theta - dtheta * self.learning_rate

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict target feature using theta parameters.
        :param x: Test data.
        :return: Test predictions.
        """
        n_examples, n_features = x.shape

        # Add bias term for test data.
        bias_term = np.ones((n_examples, 1))
        x_copy = np.concatenate((x, bias_term), axis=1)

        predictions = self._calculate_predictions(x_copy)

        return predictions

    @abstractmethod
    def _calculate_predictions(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate predictions for input data.
        :param x: Input data.
        :return: Predictions.
        """
        pass

    @abstractmethod
    def _calculate_error(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate loss function.
        :param x: Training data.
        :param y: Targets.
        :return: Error.
        """
        pass

    @abstractmethod
    def _calculate_gradient(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Find gradient of a loss function with respect to theta.
        :param x: Training data.
        :param y: Targets.
        :return: Gradient with respect to theta.
        """
        pass

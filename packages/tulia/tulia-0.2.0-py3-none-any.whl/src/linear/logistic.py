import numpy as np

from .linear import _Linear


class LogisticRegression(_Linear):
    """
    Logistic Regression (Classification)
    Currently implemented only binary classification.
    """

    def __init__(self, learning_rate: float = 1e-3, eps: float = 1e-5, n_steps: int = 1000, tol: float = 1e-5):
        """
        :param learning_rate: Learning rate for gradient descent.
        :param n_steps: Number of gradient descent steps.
        :param eps: Small number to prevent log of 0.
        :param tol: Tolerance value to terminate a training process if function converges.
        """
        super().__init__(learning_rate=learning_rate, n_steps=n_steps, tol=tol)

        self.eps = eps
        self._logits = None

    def _calculate_predictions(self, x: np.ndarray) -> np.ndarray:
        """
        Predict class label using sigmoid function.
        :param x: Input data.
        :return: Predictions.
        """
        logits = 1 / (1 + np.exp(-x @ self.theta))
        predictions = (logits >= 0.5).astype(int)  # Convert from float numbers to discrete classes.

        return predictions

    def _calculate_error(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate probability for each example (via sigmoid function) and then use in a binary cross-entropy (logloss).
        :param x:
        :param y:
        :return:
        """
        n_examples, _ = x.shape

        self._logits = 1 / (1 + np.exp(-x @ self.theta))
        error = -np.sum(
            y * np.log(self._logits + self.eps) + (1 - y) * np.log(1 - self._logits + self.eps)) / n_examples

        return error

    def _calculate_gradient(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Find gradient of a loss function with respect to theta.
        :param x: Training data.
        :param y: Targets.
        :return: Gradient with respect to theta.
        """
        n_examples, _ = x.shape

        # Calculate derivatives step-by-step using backpropagation.
        dlogits = (self._logits - y) / n_examples
        dtheta = np.dot(x.T, dlogits)

        return dtheta

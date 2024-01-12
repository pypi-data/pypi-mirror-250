import numpy as np

from src.base import Model


class GaussianNB(Model):
    """
    Gaussian Naive Bayes model for classification tasks.
    """

    def __init__(self, eps=1e-5):
        """
        :param eps: float - Value to prevent division by zero in the denominator.
        """
        self.means = {}
        self.variances = {}
        self.class_prob = {}
        self.classes = None

        self.eps = eps

    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Calculate mean and variances for each feature and class.
        :param x: Array of training data (batch_size, n_features)
        :param y: Ground truth labels for training data (batch_size, )
        :return: None
        """
        self.classes = sorted(list(np.unique(y)))

        # Iterate over each class and calculate statistics for each feature of that class.
        for cls in self.classes:
            self.means[str(cls)] = np.mean(x[cls == y], axis=0)
            self.variances[str(cls)] = np.var(x[cls == y], axis=0)
            self.class_prob[str(cls)] = (y == cls).sum() / y.shape[0]

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Goes through each data example and gives prediction for a class using calculated
        probability in the helper function.
        :param x: Array of test data (batch_size, n_features)
        :return: Numpy array with class predictions (batch_size, )
        """
        out = []

        for x_row in x:
            probabilities = self._calculate_class_probabilities(x_row)
            out.append(int(max(probabilities, key=probabilities.get)))

        return np.array(out)

    def _calculate_class_probabilities(self, x: np.ndarray) -> dict:
        """
        Helper function to calculate probability for each class using Gaussian formula.
        :param x: Single example of training data
        :return: Dictionary of class probabilities for a single data example.
        """
        probabilities = {}
        for cls in self.classes:
            means = self.means[str(cls)]
            vars = self.variances[str(cls)]
            class_prob = self.class_prob[str(cls)]

            # Gaussian formula to calculate probability of data example.
            coef = 1 / (np.sqrt(2 * np.pi * vars + self.eps))
            exp = np.exp(-((x - means) ** 2) / (2 * vars + self.eps))
            probabilities[cls] = np.prod(coef * exp) * class_prob

        return probabilities

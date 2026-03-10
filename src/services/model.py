"""Model wrapper that maintains a scikit-learn regressor for predictions."""

from typing import Dict

from sklearn.dummy import DummyRegressor


class ModelWrapper:
    def __init__(self) -> None:
        self.model = DummyRegressor(strategy="mean")
        self.model.fit([[0.0]], [0.0])
        self.is_trained = True

    def fit(self, X, y):
        """Fit the underlying regressor if training data is available."""
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, feature_vector: Dict[str, float]) -> float:
        """Return a prediction using the feature vector."""
        if not self.is_trained:
            return 0.0
        flat = feature_vector.values()
        return float(self.model.predict([list(flat)])[0])

    def explain(self, feature_vector: Dict[str, float]) -> str:
        """Generate a brief reasoning string based on the most important features."""
        sorted_features = sorted(feature_vector.items(), key=lambda item: abs(item[1]), reverse=True)
        top_two = sorted_features[:2]
        explanations = [f"{name}={value:.2f}" for name, value in top_two]
        return " + ".join(explanations)

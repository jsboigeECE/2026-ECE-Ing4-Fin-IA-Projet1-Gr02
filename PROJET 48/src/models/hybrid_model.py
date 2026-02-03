"""Hybrid model combining ML and rule-based approaches."""

import logging
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

from .ml_model import MLModel
from .rule_based import RuleBasedModel
from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class HybridModel:
    """Hybrid model combining ML and rule-based predictions."""

    def __init__(
        self,
        ml_model: Optional[MLModel] = None,
        rule_model: Optional[RuleBasedModel] = None,
        ml_weight: float = 0.6,
        rule_weight: float = 0.4,
        confidence_threshold: float = 0.7,
    ):
        """Initialize the HybridModel.

        Args:
            ml_model: ML model instance. If None, creates a new one.
            rule_model: Rule-based model instance. If None, creates a new one.
            ml_weight: Weight for ML predictions (0-1).
            rule_weight: Weight for rule-based predictions (0-1).
            confidence_threshold: Threshold for using ML over rules.
        """
        self.ml_model = ml_model if ml_model else MLModel()
        self.rule_model = rule_model if rule_model else RuleBasedModel()

        # Normalize weights
        total_weight = ml_weight + rule_weight
        self.ml_weight = ml_weight / total_weight
        self.rule_weight = rule_weight / total_weight

        self.confidence_threshold = confidence_threshold
        self.decision_classes = Config.DECISION_CLASSES

        self.is_fitted = False

    def train(
        self,
        X_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.Series],
        feature_names: Optional[List[str]] = None,
    ) -> None:
        """Train the ML component of the hybrid model.

        Args:
            X_train: Training features.
            y_train: Training labels.
            feature_names: Names of the features.
        """
        logger.info("Training ML component of hybrid model...")
        self.ml_model.train(X_train, y_train, feature_names)
        self.is_fitted = True
        logger.info("Hybrid model training completed")

    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Make predictions using the hybrid approach.

        Args:
            X: Features to predict.

        Returns:
            Predicted class labels (0=SELL, 1=HOLD, 2=BUY).
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        # Get ML predictions
        ml_predictions = self.ml_model.predict(X)
        ml_proba = self.ml_model.predict_proba(X)

        # Get rule-based predictions
        rule_predictions = self.rule_model.predict(X)
        rule_predictions_conf, rule_confidences = self.rule_model.predict_with_confidence(X)

        # Combine predictions
        predictions = []

        for i in range(len(X)):
            ml_pred = ml_predictions[i]
            rule_pred = rule_predictions[i]
            ml_conf = ml_proba[i].max()
            rule_conf = rule_confidences[i]

            # Use ML if confidence is high
            if ml_conf >= self.confidence_threshold:
                predictions.append(ml_pred)
            # Use rules if ML confidence is low but rule confidence is high
            elif rule_conf >= self.confidence_threshold:
                predictions.append(rule_pred)
            # Otherwise, use weighted voting
            else:
                # Weighted voting
                ml_vote = ml_pred * self.ml_weight
                rule_vote = rule_pred * self.rule_weight

                # Round to nearest integer
                combined = round(ml_vote + rule_vote)
                combined = np.clip(combined, 0, 2)
                predictions.append(combined)

        return np.array(predictions)

    def predict_with_details(
        self, X: Union[np.ndarray, pd.DataFrame]
    ) -> Dict[str, np.ndarray]:
        """Make predictions with detailed information.

        Args:
            X: Features to predict.

        Returns:
            Dictionary with predictions and details.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        # Get ML predictions
        ml_predictions = self.ml_model.predict(X)
        ml_proba = self.ml_model.predict_proba(X)

        # Get rule-based predictions
        rule_predictions, rule_confidences = self.rule_model.predict_with_confidence(X)
        rule_explanations = self.rule_model.get_explanation(X)

        # Get hybrid predictions
        hybrid_predictions = self.predict(X)

        # Calculate hybrid confidence
        hybrid_confidences = []
        decision_sources = []

        for i in range(len(X)):
            ml_pred = ml_predictions[i]
            rule_pred = rule_predictions[i]
            ml_conf = ml_proba[i].max()
            rule_conf = rule_confidences[i]
            hybrid_pred = hybrid_predictions[i]

            # Determine source and confidence
            if ml_conf >= self.confidence_threshold:
                source = "ML"
                confidence = ml_conf
            elif rule_conf >= self.confidence_threshold:
                source = "Rules"
                confidence = rule_conf
            else:
                source = "Hybrid"
                confidence = (ml_conf * self.ml_weight) + (rule_conf * self.rule_weight)

            hybrid_confidences.append(confidence)
            decision_sources.append(source)

        return {
            "predictions": hybrid_predictions,
            "ml_predictions": ml_predictions,
            "rule_predictions": rule_predictions,
            "ml_confidence": ml_proba.max(axis=1),
            "rule_confidence": rule_confidences,
            "hybrid_confidence": np.array(hybrid_confidences),
            "decision_source": np.array(decision_sources),
            "rule_explanations": rule_explanations,
        }

    def evaluate(
        self,
        X_test: Union[np.ndarray, pd.DataFrame],
        y_test: Union[np.ndarray, pd.Series],
    ) -> Dict[str, float]:
        """Evaluate the hybrid model.

        Args:
            X_test: Test features.
            y_test: Test labels.

        Returns:
            Dictionary of evaluation metrics.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before evaluation")

        from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

        predictions = self.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, average="weighted", zero_division=0),
            "recall": recall_score(y_test, predictions, average="weighted", zero_division=0),
            "f1": f1_score(y_test, predictions, average="weighted", zero_division=0),
        }

        # Also evaluate individual components
        ml_metrics = self.ml_model.evaluate(X_test, y_test)
        rule_predictions = self.rule_model.predict(X_test)
        rule_metrics = {
            "accuracy": accuracy_score(y_test, rule_predictions),
            "precision": precision_score(y_test, rule_predictions, average="weighted", zero_division=0),
            "recall": recall_score(y_test, rule_predictions, average="weighted", zero_division=0),
            "f1": f1_score(y_test, rule_predictions, average="weighted", zero_division=0),
        }

        metrics["ml_accuracy"] = ml_metrics["accuracy"]
        metrics["rule_accuracy"] = rule_metrics["accuracy"]

        logger.info(f"Hybrid model evaluation: {metrics}")
        return metrics

    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from the ML component.

        Returns:
            DataFrame with feature names and importance scores.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")

        return self.ml_model.get_feature_importance()

    def save_model(self, filename: str = "hybrid_model.joblib") -> None:
        """Save the hybrid model to disk.

        Args:
            filename: Name of the file to save.
        """
        import joblib
        from pathlib import Path

        model_data = {
            "ml_model": self.ml_model,
            "rule_model": self.rule_model,
            "ml_weight": self.ml_weight,
            "rule_weight": self.rule_weight,
            "confidence_threshold": self.confidence_threshold,
            "is_fitted": self.is_fitted,
        }

        filepath = Config.MODELS_DIR / filename
        joblib.dump(model_data, filepath)

        logger.info(f"Hybrid model saved to {filepath}")

    def load_model(self, filepath: str) -> None:
        """Load a hybrid model from disk.

        Args:
            filepath: Path to the saved model.
        """
        import joblib
        from pathlib import Path

        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")

        model_data = joblib.load(filepath)

        self.ml_model = model_data["ml_model"]
        self.rule_model = model_data["rule_model"]
        self.ml_weight = model_data["ml_weight"]
        self.rule_weight = model_data["rule_weight"]
        self.confidence_threshold = model_data["confidence_threshold"]
        self.is_fitted = model_data["is_fitted"]

        logger.info(f"Hybrid model loaded from {filepath}")

    def get_model_summary(self) -> Dict:
        """Get a summary of the hybrid model.

        Returns:
            Dictionary with model information.
        """
        return {
            "ml_model_type": self.ml_model.model_type,
            "ml_weight": self.ml_weight,
            "rule_weight": self.rule_weight,
            "confidence_threshold": self.confidence_threshold,
            "is_fitted": self.is_fitted,
            "decision_classes": self.decision_classes,
            "rule_summary": self.rule_model.get_rule_summary(),
        }

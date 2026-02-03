"""Counterfactual explainer for generating alternative scenarios."""

import logging
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd

from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class CounterfactualExplainer:
    """Counterfactual explainer for generating alternative scenarios."""

    def __init__(
        self,
        model,
        feature_names: Optional[List[str]] = None,
        num_samples: int = Config.COUNTERFACTUAL_NUM_SAMPLES,
        feature_ranges: Optional[Dict[str, tuple]] = None,
    ):
        """Initialize the CounterfactualExplainer.

        Args:
            model: The trained model to explain.
            feature_names: Names of the features.
            num_samples: Number of counterfactual samples to generate.
            feature_ranges: Dictionary mapping feature names to (min, max) ranges.
        """
        self.model = model
        self.num_samples = num_samples
        self.feature_names = feature_names
        self.feature_ranges = feature_ranges or {}

        self.decision_classes = Config.DECISION_CLASSES

    def generate_counterfactual(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
        target_class: Optional[int] = None,
        max_iterations: int = 100,
        learning_rate: float = 0.1,
    ) -> Dict:
        """Generate a counterfactual explanation for a single instance.

        Args:
            X: Feature values.
            index: Index of the instance.
            target_class: Target class for counterfactual. If None, finds the closest different class.
            max_iterations: Maximum number of iterations for optimization.
            learning_rate: Learning rate for gradient-based search.

        Returns:
            Dictionary with counterfactual explanation.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
            feature_names = X.columns.tolist()
        else:
            X_array = X
            feature_names = self.feature_names or [f"feature_{i}" for i in range(X.shape[1])]

        original_instance = X_array[index : index + 1][0].copy()
        original_prediction = self.model.predict([original_instance])[0]

        # Determine target class if not specified
        if target_class is None:
            # Find the closest different class
            target_class = self._find_closest_class(original_instance, original_prediction)

        # Generate counterfactual
        counterfactual = self._optimize_counterfactual(
            original_instance,
            original_prediction,
            target_class,
            max_iterations,
            learning_rate,
        )

        # Calculate changes
        changes = self._calculate_changes(original_instance, counterfactual, feature_names)

        # Verify counterfactual
        cf_prediction = self.model.predict([counterfactual])[0]
        success = cf_prediction == target_class

        explanation = {
            "index": index,
            "original_instance": original_instance.tolist(),
            "original_prediction": int(original_prediction),
            "original_prediction_label": self.decision_classes[int(original_prediction)],
            "counterfactual": counterfactual.tolist(),
            "counterfactual_prediction": int(cf_prediction),
            "counterfactual_prediction_label": self.decision_classes[int(cf_prediction)],
            "target_class": target_class,
            "target_class_label": self.decision_classes[target_class],
            "success": success,
            "changes": changes,
            "distance": float(np.linalg.norm(counterfactual - original_instance)),
        }

        return explanation

    def _find_closest_class(
        self, instance: np.ndarray, original_class: int
    ) -> int:
        """Find the closest different class to the original prediction.

        Args:
            instance: Original instance.
            original_class: Original predicted class.

        Returns:
            Closest different class.
        """
        # Try each class and find the one with minimal distance
        best_class = None
        best_distance = float("inf")

        for target_class in range(len(self.decision_classes)):
            if target_class == original_class:
                continue

            # Simple heuristic: try to find a counterfactual
            cf = self._optimize_counterfactual(
                instance, original_class, target_class, max_iterations=50, learning_rate=0.1
            )
            distance = np.linalg.norm(cf - instance)

            if distance < best_distance:
                best_distance = distance
                best_class = target_class

        return best_class if best_class is not None else (original_class + 1) % len(self.decision_classes)

    def _optimize_counterfactual(
        self,
        original_instance: np.ndarray,
        original_class: int,
        target_class: int,
        max_iterations: int,
        learning_rate: float,
    ) -> np.ndarray:
        """Optimize a counterfactual instance.

        Args:
            original_instance: Original instance.
            original_class: Original predicted class.
            target_class: Target class for counterfactual.
            max_iterations: Maximum iterations.
            learning_rate: Learning rate.

        Returns:
            Optimized counterfactual instance.
        """
        counterfactual = original_instance.copy()
        best_cf = counterfactual.copy()
        best_distance = float("inf")
        
        # Get probability predictions to guide search
        try:
            original_proba = self.model.predict_proba([original_instance])[0]
            target_proba = original_proba[target_class]
        except:
            original_proba = None
            target_proba = 0

        for iteration in range(max_iterations):
            # Check if we've reached the target class
            prediction = self.model.predict([counterfactual])[0]

            if prediction == target_class:
                # Found a valid counterfactual
                distance = np.linalg.norm(counterfactual - original_instance)
                if distance < best_distance:
                    best_cf = counterfactual.copy()
                    best_distance = distance
                break

            # Try systematic perturbations on each feature
            for i in range(len(counterfactual)):
                # Try positive perturbation
                new_cf = counterfactual.copy()
                new_cf[i] += learning_rate * (1 + np.random.randn() * 0.1)
                new_prediction = self.model.predict([new_cf])[0]
                
                if new_prediction == target_class:
                    distance = np.linalg.norm(new_cf - original_instance)
                    if distance < best_distance:
                        best_cf = new_cf.copy()
                        best_distance = distance
                        counterfactual = new_cf.copy()
                        break
                
                # Try negative perturbation
                new_cf = counterfactual.copy()
                new_cf[i] -= learning_rate * (1 + np.random.randn() * 0.1)
                new_prediction = self.model.predict([new_cf])[0]
                
                if new_prediction == target_class:
                    distance = np.linalg.norm(new_cf - original_instance)
                    if distance < best_distance:
                        best_cf = new_cf.copy()
                        best_distance = distance
                        counterfactual = new_cf.copy()
                        break
            
            # If we found a valid counterfactual, return it
            if best_distance < float("inf"):
                return best_cf
            
            # Otherwise, try random perturbations as fallback
            perturbation = np.random.randn(len(counterfactual)) * learning_rate
            new_cf = counterfactual + perturbation
            new_prediction = self.model.predict([new_cf])[0]
            
            if new_prediction == target_class:
                distance = np.linalg.norm(new_cf - original_instance)
                if distance < best_distance:
                    best_cf = new_cf.copy()
                    best_distance = distance
                    counterfactual = new_cf.copy()
            elif new_prediction != original_class:
                # Accept if it changes the prediction
                distance = np.linalg.norm(new_cf - original_instance)
                if distance < best_distance:
                    best_cf = new_cf.copy()
                    best_distance = distance
                    counterfactual = new_cf.copy()

            # Reduce learning rate
            learning_rate *= 0.95

        return best_cf

    def _calculate_changes(
        self,
        original: np.ndarray,
        counterfactual: np.ndarray,
        feature_names: List[str],
    ) -> List[Dict]:
        """Calculate changes between original and counterfactual.

        Args:
            original: Original instance.
            counterfactual: Counterfactual instance.
            feature_names: Names of features.

        Returns:
            List of change dictionaries.
        """
        changes = []
        diff = counterfactual - original

        for i, (name, change) in enumerate(zip(feature_names, diff)):
            if abs(change) > 0.01:  # Only include significant changes
                original_val = original[i]
                cf_val = counterfactual[i]
                pct_change = (change / abs(original_val)) * 100 if original_val != 0 else 0

                changes.append(
                    {
                        "feature": name,
                        "original_value": float(original_val),
                        "counterfactual_value": float(cf_val),
                        "change": float(change),
                        "percent_change": float(pct_change),
                        "direction": "increase" if change > 0 else "decrease",
                    }
                )

        # Sort by absolute change
        changes.sort(key=lambda x: abs(x["change"]), reverse=True)

        return changes

    def generate_multiple_counterfactuals(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
        num_counterfactuals: int = 3,
        target_class: Optional[int] = None,
    ) -> List[Dict]:
        """Generate multiple counterfactual explanations.

        Args:
            X: Feature values.
            index: Index of the instance.
            num_counterfactuals: Number of counterfactuals to generate.
            target_class: Target class for counterfactuals.

        Returns:
            List of counterfactual explanations.
        """
        counterfactuals = []

        for i in range(num_counterfactuals):
            # Use different random seeds for variety
            np.random.seed(i * 42)
            cf = self.generate_counterfactual(X, index, target_class)
            counterfactuals.append(cf)

        return counterfactuals

    def get_counterfactual_summary(
        self,
        counterfactuals: List[Dict],
    ) -> Dict:
        """Summarize multiple counterfactuals.

        Args:
            counterfactuals: List of counterfactual explanations.

        Returns:
            Summary dictionary.
        """
        successful = [cf for cf in counterfactuals if cf["success"]]

        if not successful:
            return {
                "total": len(counterfactuals),
                "successful": 0,
                "failed": len(counterfactuals),
                "average_distance": None,
                "common_changes": [],
            }

        # Calculate average distance
        avg_distance = np.mean([cf["distance"] for cf in successful])

        # Find common changes
        all_changes = []
        for cf in successful:
            all_changes.extend(cf["changes"])

        # Aggregate changes by feature
        feature_changes = {}
        for change in all_changes:
            feature = change["feature"]
            if feature not in feature_changes:
                feature_changes[feature] = {"count": 0, "total_change": 0}

            feature_changes[feature]["count"] += 1
            feature_changes[feature]["total_change"] += change["change"]

        # Calculate average change per feature
        common_changes = []
        for feature, data in feature_changes.items():
            avg_change = data["total_change"] / data["count"]
            common_changes.append(
                {
                    "feature": feature,
                    "count": data["count"],
                    "average_change": float(avg_change),
                    "frequency": data["count"] / len(successful),
                }
            )

        # Sort by frequency
        common_changes.sort(key=lambda x: x["frequency"], reverse=True)

        return {
            "total": len(counterfactuals),
            "successful": len(successful),
            "failed": len(counterfactuals) - len(successful),
            "average_distance": float(avg_distance),
            "common_changes": common_changes[:10],  # Top 10
        }

    def get_counterfactual_text(
        self,
        counterfactual: Dict,
        max_changes: int = 5,
    ) -> str:
        """Generate a text explanation for a counterfactual.

        Args:
            counterfactual: Counterfactual explanation dictionary.
            max_changes: Maximum number of changes to include.

        Returns:
            Text explanation.
        """
        if not counterfactual["success"]:
            return "Could not generate a valid counterfactual explanation."

        original_label = counterfactual["original_prediction_label"]
        target_label = counterfactual["target_class_label"]
        changes = counterfactual["changes"][:max_changes]

        text_parts = [
            f"To change the recommendation from {original_label} to {target_label},",
            "the following changes would be needed:",
        ]

        for change in changes:
            direction = "increase" if change["direction"] == "increase" else "decrease"
            text_parts.append(
                f"- {direction} {change['feature']} from {change['original_value']:.2f} "
                f"to {change['counterfactual_value']:.2f}"
            )

        return " ".join(text_parts)

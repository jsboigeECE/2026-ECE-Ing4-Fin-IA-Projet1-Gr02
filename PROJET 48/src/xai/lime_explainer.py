"""LIME explainer for local model interpretation."""

import logging
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
from lime import lime_tabular

from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class LIMEExplainer:
    """LIME explainer for local model interpretation."""

    def __init__(
        self,
        model,
        training_data: Union[np.ndarray, pd.DataFrame],
        feature_names: Optional[List[str]] = None,
        class_names: Optional[List[str]] = None,
        num_samples: int = Config.LIME_NUM_SAMPLES,
        mode: str = "classification",
    ):
        """Initialize the LIMEExplainer.

        Args:
            model: The trained model to explain.
            training_data: Training data for LIME explainer.
            feature_names: Names of the features.
            class_names: Names of the classes.
            num_samples: Number of samples for LIME explanation.
            mode: Mode of the model ('classification' or 'regression').
        """
        self.model = model
        self.num_samples = num_samples
        self.mode = mode
        self.class_names = class_names or Config.DECISION_CLASSES

        # Prepare training data
        if isinstance(training_data, pd.DataFrame):
            self.training_data = training_data.values
            self.feature_names = training_data.columns.tolist()
        else:
            self.training_data = training_data
            self.feature_names = feature_names or [f"feature_{i}" for i in range(training_data.shape[1])]

        self.explainer = None
        self._initialize_explainer()

    def _initialize_explainer(self) -> None:
        """Initialize the LIME explainer."""
        logger.info("Initializing LIME explainer...")

        self.explainer = lime_tabular.LimeTabularExplainer(
            training_data=self.training_data,
            feature_names=self.feature_names,
            class_names=self.class_names,
            mode=self.mode,
            discretize_continuous=True,
        )

        logger.info("LIME explainer initialized")

    def explain_instance(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
        num_features: int = 10,
    ) -> Dict:
        """Explain a single instance using LIME.

        Args:
            X: Feature values.
            index: Index of the instance to explain.
            num_features: Number of top features to include in explanation.

        Returns:
            Dictionary with LIME explanation.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
        else:
            X_array = X

        instance = X_array[index : index + 1][0]

        # Get model prediction function
        if hasattr(self.model, "predict_proba"):
            predict_fn = self.model.predict_proba
        else:
            predict_fn = self.model.predict

        # Generate LIME explanation
        exp = self.explainer.explain_instance(
            instance,
            predict_fn,
            num_features=num_features,
            num_samples=self.num_samples,
        )

        # Extract explanation data
        explanation = {
            "index": index,
            "prediction": self.class_names[int(self.model.predict([instance])[0])],
            "prediction_proba": self.model.predict_proba([instance])[0].tolist(),
            "intercept": exp.intercept,
            "intercept_pred": exp.intercept_pred,
            "local_pred": exp.local_pred,
            "score": exp.score,
            "features": self._extract_feature_importance(exp),
        }

        return explanation

    def _extract_feature_importance(self, exp) -> List[Dict]:
        """Extract feature importance from LIME explanation.

        Args:
            exp: LIME explanation object.

        Returns:
            List of feature importance dictionaries.
        """
        features = []
        for feature, value in exp.as_list():
            features.append(
                {
                    "feature": feature,
                    "weight": float(value),
                    "abs_weight": float(abs(value)),
                    "direction": "positive" if value > 0 else "negative",
                }
            )

        # Sort by absolute weight
        features.sort(key=lambda x: x["abs_weight"], reverse=True)

        return features

    def explain_batch(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        num_features: int = 10,
    ) -> List[Dict]:
        """Explain multiple instances.

        Args:
            X: Feature values.
            num_features: Number of top features to include.

        Returns:
            List of LIME explanations.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
        else:
            X_array = X

        explanations = []
        for i in range(len(X_array)):
            explanation = self.explain_instance(X_array, i, num_features)
            explanations.append(explanation)

        return explanations

    def get_top_features(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
        top_n: int = 5,
    ) -> List[Dict]:
        """Get top features for an instance.

        Args:
            X: Feature values.
            index: Index of the instance.
            top_n: Number of top features to return.

        Returns:
            List of top feature dictionaries.
        """
        explanation = self.explain_instance(X, index)
        return explanation["features"][:top_n]

    def compare_instances(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        indices: List[int],
    ) -> Dict:
        """Compare explanations for multiple instances.

        Args:
            X: Feature values.
            indices: List of indices to compare.

        Returns:
            Dictionary with comparison data.
        """
        explanations = [self.explain_instance(X, idx) for idx in indices]

        # Aggregate feature importance across instances
        feature_aggregation = {}

        for exp in explanations:
            for feature in exp["features"]:
                name = feature["feature"]
                weight = feature["weight"]

                if name not in feature_aggregation:
                    feature_aggregation[name] = {"weights": [], "count": 0}

                feature_aggregation[name]["weights"].append(weight)
                feature_aggregation[name]["count"] += 1

        # Calculate average importance
        comparison = {
            "explanations": explanations,
            "feature_aggregation": [],
        }

        for name, data in feature_aggregation.items():
            avg_weight = np.mean(data["weights"])
            comparison["feature_aggregation"].append(
                {
                    "feature": name,
                    "avg_weight": float(avg_weight),
                    "abs_avg_weight": float(abs(avg_weight)),
                    "count": data["count"],
                    "direction": "positive" if avg_weight > 0 else "negative",
                }
            )

        # Sort by average absolute weight
        comparison["feature_aggregation"].sort(
            key=lambda x: x["abs_avg_weight"], reverse=True
        )

        return comparison

    def plot_explanation(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
        save_path: Optional[str] = None,
    ) -> None:
        """Create a LIME explanation plot.

        Args:
            X: Feature values.
            index: Index of the instance.
            save_path: Path to save the plot.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
        else:
            X_array = X

        instance = X_array[index : index + 1][0]

        # Get model prediction function
        if hasattr(self.model, "predict_proba"):
            predict_fn = self.model.predict_proba
        else:
            predict_fn = self.model.predict

        # Generate LIME explanation
        exp = self.explainer.explain_instance(
            instance,
            predict_fn,
            num_samples=self.num_samples,
        )

        # Create plot
        fig = exp.as_pyplot_figure()

        if save_path:
            fig.savefig(save_path, bbox_inches="tight", dpi=300)
            import matplotlib.pyplot as plt

            plt.close(fig)
            logger.info(f"LIME explanation plot saved to {save_path}")

    def get_explanation_text(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
        num_features: int = 5,
    ) -> str:
        """Get a text explanation for an instance.

        Args:
            X: Feature values.
            index: Index of the instance.
            num_features: Number of features to include.

        Returns:
            Text explanation.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
        else:
            X_array = X

        instance = X_array[index : index + 1][0]

        # Get model prediction function
        if hasattr(self.model, "predict_proba"):
            predict_fn = self.model.predict_proba
        else:
            predict_fn = self.model.predict

        # Generate LIME explanation
        exp = self.explainer.explain_instance(
            instance,
            predict_fn,
            num_features=num_features,
            num_samples=self.num_samples,
        )

        # Get text explanation
        explanation_text = exp.as_list()

        # Format as readable text
        text_parts = []
        for feature, weight in explanation_text:
            direction = "increases" if weight > 0 else "decreases"
            text_parts.append(f"{feature} {direction} the prediction probability")

        return " and ".join(text_parts)

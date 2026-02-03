"""SHAP explainer for model interpretation."""

import logging
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
import shap

from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SHAPExplainer:
    """SHAP explainer for model interpretation."""

    def __init__(
        self,
        model,
        background_data: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        background_size: int = Config.SHAP_BACKGROUND_SIZE,
        feature_names: Optional[List[str]] = None,
    ):
        """Initialize the SHAPExplainer.

        Args:
            model: The trained model to explain.
            background_data: Background data for SHAP values calculation.
            background_size: Number of background samples to use.
            feature_names: Names of the features.
        """
        self.model = model
        self.background_size = background_size
        self.feature_names = feature_names
        self.explainer = None
        self.background_data = background_data

        self._initialize_explainer()

    def _initialize_explainer(self) -> None:
        """Initialize the SHAP explainer based on model type."""
        logger.info("Initializing SHAP explainer...")

        # Determine explainer type based on model
        if hasattr(self.model, "predict_proba"):
            # For tree-based models, use TreeExplainer
            if hasattr(self.model, "estimators_") or hasattr(self.model, "get_booster"):
                logger.info("Using TreeExplainer for tree-based model")
                self.explainer = shap.TreeExplainer(self.model)
            else:
                logger.info("Using KernelExplainer for general model")
                self.explainer = shap.KernelExplainer(
                    self.model.predict_proba,
                    self._get_background_data(),
                )
        else:
            logger.info("Using Explainer for general model")
            self.explainer = shap.Explainer(self.model, self._get_background_data())

        logger.info("SHAP explainer initialized")

    def _get_background_data(self) -> np.ndarray:
        """Get background data for SHAP explainer.

        Returns:
            Background data array.
        """
        if self.background_data is not None:
            if isinstance(self.background_data, pd.DataFrame):
                return self.background_data.values
            return self.background_data[: self.background_size]
        return np.zeros((self.background_size, 10))  # Default placeholder

    def explain_instance(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
    ) -> Dict:
        """Explain a single instance.

        Args:
            X: Feature values.
            index: Index of the instance to explain.

        Returns:
            Dictionary with SHAP explanation.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
            feature_names = X.columns.tolist()
        else:
            X_array = X
            feature_names = self.feature_names or [f"feature_{i}" for i in range(X.shape[1])]

        instance = X_array[index : index + 1]

        # Calculate SHAP values
        shap_values = self.explainer.shap_values(instance)

        # Handle different SHAP value formats
        if isinstance(shap_values, list):
            # Multi-class case
            shap_values = shap_values[0]  # Use first class for now

        # Create explanation dictionary
        explanation = {
            "index": index,
            "shap_values": shap_values[0].tolist(),
            "base_value": float(self.explainer.expected_value[0])
            if isinstance(self.explainer.expected_value, list)
            else float(self.explainer.expected_value),
            "feature_values": instance[0].tolist(),
            "feature_names": feature_names,
            "feature_importance": self._get_feature_importance(shap_values[0], feature_names),
        }

        return explanation

    def explain_batch(
        self,
        X: Union[np.ndarray, pd.DataFrame],
    ) -> List[Dict]:
        """Explain multiple instances.

        Args:
            X: Feature values.

        Returns:
            List of SHAP explanations.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
            feature_names = X.columns.tolist()
        else:
            X_array = X
            feature_names = self.feature_names or [f"feature_{i}" for i in range(X.shape[1])]

        # Calculate SHAP values for all instances
        shap_values = self.explainer.shap_values(X_array)

        # Handle different SHAP value formats
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        explanations = []
        for i in range(len(X_array)):
            explanation = {
                "index": i,
                "shap_values": shap_values[i].tolist(),
                "base_value": float(self.explainer.expected_value[0])
                if isinstance(self.explainer.expected_value, list)
                else float(self.explainer.expected_value),
                "feature_values": X_array[i].tolist(),
                "feature_names": feature_names,
                "feature_importance": self._get_feature_importance(shap_values[i], feature_names),
            }
            explanations.append(explanation)

        return explanations

    def _get_feature_importance(
        self, shap_values: np.ndarray, feature_names: List[str]
    ) -> List[Dict]:
        """Get feature importance from SHAP values.

        Args:
            shap_values: SHAP values for an instance.
            feature_names: Names of the features.

        Returns:
            List of feature importance dictionaries.
        """
        importance = []
        for i, (name, value) in enumerate(zip(feature_names, shap_values)):
            importance.append(
                {
                    "feature": name,
                    "shap_value": float(value),
                    "abs_shap_value": float(abs(value)),
                    "direction": "positive" if value > 0 else "negative",
                }
            )

        # Sort by absolute SHAP value
        importance.sort(key=lambda x: x["abs_shap_value"], reverse=True)

        return importance

    def get_global_feature_importance(
        self,
        X: Union[np.ndarray, pd.DataFrame],
    ) -> pd.DataFrame:
        """Get global feature importance.

        Args:
            X: Feature values.

        Returns:
            DataFrame with global feature importance.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
            feature_names = X.columns.tolist()
        else:
            X_array = X
            feature_names = self.feature_names or [f"feature_{i}" for i in range(X.shape[1])]

        # Calculate SHAP values
        shap_values = self.explainer.shap_values(X_array)

        # Handle different SHAP value formats
        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        # Calculate mean absolute SHAP values
        mean_abs_shap = np.mean(np.abs(shap_values), axis=0)

        importance_df = pd.DataFrame(
            {"feature": feature_names, "importance": mean_abs_shap}
        ).sort_values("importance", ascending=False)

        return importance_df

    def plot_summary(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        save_path: Optional[str] = None,
    ) -> None:
        """Create a SHAP summary plot.

        Args:
            X: Feature values.
            save_path: Path to save the plot.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
        else:
            X_array = X

        shap_values = self.explainer.shap_values(X_array)

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        shap.summary_plot(
            shap_values,
            X_array,
            feature_names=self.feature_names,
            show=False,
        )

        if save_path:
            import matplotlib.pyplot as plt

            plt.savefig(save_path, bbox_inches="tight", dpi=300)
            plt.close()
            logger.info(f"SHAP summary plot saved to {save_path}")

    def plot_waterfall(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
        save_path: Optional[str] = None,
    ) -> None:
        """Create a SHAP waterfall plot for a single instance.

        Args:
            X: Feature values.
            index: Index of the instance.
            save_path: Path to save the plot.
        """
        if isinstance(X, pd.DataFrame):
            X_array = X.values
        else:
            X_array = X

        instance = X_array[index : index + 1]
        shap_values = self.explainer.shap_values(instance)

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        expected_value = (
            self.explainer.expected_value[0]
            if isinstance(self.explainer.expected_value, list)
            else self.explainer.expected_value
        )

        shap.waterfall_plot(
            shap.Explanation(
                values=shap_values[0],
                base_values=expected_value,
                data=instance[0],
                feature_names=self.feature_names,
            ),
            show=False,
        )

        if save_path:
            import matplotlib.pyplot as plt

            plt.savefig(save_path, bbox_inches="tight", dpi=300)
            plt.close()
            logger.info(f"SHAP waterfall plot saved to {save_path}")

    def get_force_plot_data(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        index: int = 0,
    ) -> Dict:
        """Get data for a force plot.

        Args:
            X: Feature values.
            index: Index of the instance.

        Returns:
            Dictionary with force plot data.
        """
        explanation = self.explain_instance(X, index)
        return explanation

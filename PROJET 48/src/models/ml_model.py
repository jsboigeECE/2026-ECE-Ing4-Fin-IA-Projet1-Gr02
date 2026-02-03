"""Machine Learning model for investment recommendations."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score, GridSearchCV
from xgboost import XGBClassifier

from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class MLModel:
    """Machine Learning model for investment recommendations."""

    def __init__(
        self,
        model_type: str = Config.MODEL_TYPE,
        random_seed: int = Config.RANDOM_SEED,
        model_path: Optional[Path] = None,
    ):
        """Initialize the MLModel.

        Args:
            model_type: Type of model ('xgboost', 'lightgbm', 'random_forest').
            random_seed: Random seed for reproducibility.
            model_path: Path to save/load the model.
        """
        self.model_type = model_type.lower()
        self.random_seed = random_seed
        self.model_path = Path(model_path) if model_path else Config.MODELS_DIR
        self.model_path.mkdir(parents=True, exist_ok=True)

        self.model = None
        self.feature_names: List[str] = []
        self.is_fitted = False

        self._initialize_model()

    def _initialize_model(self) -> None:
        """Initialize the model based on model_type."""
        if self.model_type == "xgboost":
            self.model = XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_seed,
                eval_metric="logloss",
            )
        elif self.model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=self.random_seed,
                n_jobs=-1,
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

        logger.info(f"Initialized {self.model_type} model")

    def train(
        self,
        X_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.Series],
        feature_names: Optional[List[str]] = None,
    ) -> None:
        """Train the model.

        Args:
            X_train: Training features.
            y_train: Training labels.
            feature_names: Names of the features.
        """
        logger.info(f"Training {self.model_type} model...")

        # Store feature names
        if isinstance(X_train, pd.DataFrame):
            self.feature_names = X_train.columns.tolist()
        elif feature_names:
            self.feature_names = feature_names

        # Train the model
        self.model.fit(X_train, y_train)
        self.is_fitted = True

        logger.info("Model training completed")

    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Make predictions.

        Args:
            X: Features to predict.

        Returns:
            Predicted class labels.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        return self.model.predict(X)

    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Predict class probabilities.

        Args:
            X: Features to predict.

        Returns:
            Predicted probabilities for each class.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        return self.model.predict_proba(X)

    def evaluate(
        self,
        X_test: Union[np.ndarray, pd.DataFrame],
        y_test: Union[np.ndarray, pd.Series],
    ) -> Dict[str, float]:
        """Evaluate the model.

        Args:
            X_test: Test features.
            y_test: Test labels.

        Returns:
            Dictionary of evaluation metrics.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before evaluation")

        y_pred = self.predict(X_test)
        y_proba = self.predict_proba(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
            "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
            "f1": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        }

        logger.info(f"Model evaluation: {metrics}")
        return metrics

    def cross_validate(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
        cv: int = 5,
    ) -> Dict[str, float]:
        """Perform cross-validation.

        Args:
            X: Features.
            y: Labels.
            cv: Number of cross-validation folds.

        Returns:
            Dictionary of cross-validation scores.
        """
        logger.info(f"Performing {cv}-fold cross-validation...")

        scores = cross_val_score(self.model, X, y, cv=cv, scoring="accuracy")

        results = {
            "mean_accuracy": scores.mean(),
            "std_accuracy": scores.std(),
            "scores": scores.tolist(),
        }

        logger.info(f"Cross-validation results: {results}")
        return results

    def hyperparameter_tune(
        self,
        X_train: Union[np.ndarray, pd.DataFrame],
        y_train: Union[np.ndarray, pd.Series],
        param_grid: Optional[Dict] = None,
        cv: int = 5,
    ) -> Dict:
        """Tune hyperparameters using GridSearchCV.

        Args:
            X_train: Training features.
            y_train: Training labels.
            param_grid: Parameter grid for GridSearchCV.
            cv: Number of cross-validation folds.

        Returns:
            Best parameters and best score.
        """
        if param_grid is None:
            if self.model_type == "xgboost":
                param_grid = {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [3, 6, 9],
                    "learning_rate": [0.01, 0.1, 0.2],
                }
            elif self.model_type == "random_forest":
                param_grid = {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [5, 10, 15],
                    "min_samples_split": [2, 5, 10],
                }

        logger.info("Starting hyperparameter tuning...")

        grid_search = GridSearchCV(
            self.model, param_grid, cv=cv, scoring="accuracy", n_jobs=-1, verbose=1
        )
        grid_search.fit(X_train, y_train)

        self.model = grid_search.best_estimator_
        self.is_fitted = True

        results = {
            "best_params": grid_search.best_params_,
            "best_score": grid_search.best_score_,
        }

        logger.info(f"Best parameters: {results['best_params']}")
        logger.info(f"Best score: {results['best_score']}")

        return results

    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from the model.

        Returns:
            DataFrame with feature names and importance scores.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")

        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
        else:
            raise AttributeError("Model does not have feature_importances_ attribute")

        feature_importance = pd.DataFrame(
            {"feature": self.feature_names, "importance": importances}
        ).sort_values("importance", ascending=False)

        return feature_importance

    def save_model(self, filename: str = "model.joblib") -> Path:
        """Save the model to disk.

        Args:
            filename: Name of the file to save.

        Returns:
            Path to the saved model.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")

        model_data = {
            "model": self.model,
            "model_type": self.model_type,
            "feature_names": self.feature_names,
            "random_seed": self.random_seed,
        }

        filepath = self.model_path / filename
        joblib.dump(model_data, filepath)

        logger.info(f"Model saved to {filepath}")
        return filepath

    def load_model(self, filepath: Path) -> None:
        """Load a model from disk.

        Args:
            filepath: Path to the saved model.
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")

        model_data = joblib.load(filepath)

        self.model = model_data["model"]
        self.model_type = model_data["model_type"]
        self.feature_names = model_data["feature_names"]
        self.random_seed = model_data["random_seed"]
        self.is_fitted = True

        logger.info(f"Model loaded from {filepath}")

    def get_decision_function(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Get decision function values (for SHAP explanations).

        Args:
            X: Features.

        Returns:
            Decision function values.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting decision function")

        if hasattr(self.model, "predict_proba"):
            return self.predict_proba(X)
        elif hasattr(self.model, "decision_function"):
            return self.model.decision_function(X)
        else:
            return self.predict(X)

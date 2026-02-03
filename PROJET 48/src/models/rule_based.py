"""Rule-based model for investment recommendations."""

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


class RuleBasedModel:
    """Rule-based model for investment recommendations."""

    def __init__(self, thresholds: Optional[Dict] = None):
        """Initialize the RuleBasedModel.

        Args:
            thresholds: Dictionary of rule thresholds. If None, uses Config.RULE_THRESHOLDS.
        """
        self.thresholds = thresholds if thresholds else Config.RULE_THRESHOLDS
        self.decision_classes = Config.DECISION_CLASSES
        self.rules_applied: List[str] = []

    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Make predictions based on rules.

        Args:
            X: Features to predict.

        Returns:
            Predicted class labels (0=SELL, 1=HOLD, 2=BUY).
        """
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        predictions = []
        self.rules_applied = []

        for _, row in X.iterrows():
            decision, rules = self._apply_rules(row)
            predictions.append(decision)
            self.rules_applied.append(rules)

        return np.array(predictions)

    def predict_with_confidence(
        self, X: Union[np.ndarray, pd.DataFrame]
    ) -> tuple[np.ndarray, np.ndarray]:
        """Make predictions with confidence scores.

        Args:
            X: Features to predict.

        Returns:
            Tuple of (predictions, confidence_scores).
        """
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        predictions = []
        confidences = []

        for _, row in X.iterrows():
            decision, rules = self._apply_rules(row)
            confidence = self._calculate_confidence(row, rules)
            predictions.append(decision)
            confidences.append(confidence)

        return np.array(predictions), np.array(confidences)

    def _apply_rules(self, row: pd.Series) -> tuple[int, List[str]]:
        """Apply investment rules to a single observation.

        Args:
            row: Feature values for a single observation.

        Returns:
            Tuple of (decision, applied_rules).
        """
        buy_signals = 0
        sell_signals = 0
        hold_signals = 0
        applied_rules = []

        # RSI rules
        if "rsi" in row.index and not pd.isna(row["rsi"]):
            if row["rsi"] < self.thresholds["rsi"]["oversold"]:
                buy_signals += 1
                applied_rules.append("RSI oversold (<30)")
            elif row["rsi"] > self.thresholds["rsi"]["overbought"]:
                sell_signals += 1
                applied_rules.append("RSI overbought (>70)")
            else:
                hold_signals += 1

        # Moving average rules
        if "sma_20" in row.index and "sma_50" in row.index:
            if not pd.isna(row["sma_20"]) and not pd.isna(row["sma_50"]):
                if row["sma_20"] > row["sma_50"]:
                    buy_signals += 1
                    applied_rules.append("SMA20 > SMA50 (uptrend)")
                else:
                    sell_signals += 1
                    applied_rules.append("SMA20 < SMA50 (downtrend)")

        # MACD rules
        if "macd" in row.index and "macd_signal" in row.index:
            if not pd.isna(row["macd"]) and not pd.isna(row["macd_signal"]):
                if row["macd"] > row["macd_signal"]:
                    buy_signals += 1
                    applied_rules.append("MACD > Signal (bullish)")
                else:
                    sell_signals += 1
                    applied_rules.append("MACD < Signal (bearish)")

        # Bollinger Bands rules
        if "bb_upper" in row.index and "bb_lower" in row.index:
            if not pd.isna(row["bb_upper"]) and not pd.isna(row["bb_lower"]):
                # Assuming Close is in the row or we need to check against price
                # For now, we'll use the position relative to bands
                if "Close" in row.index and not pd.isna(row["Close"]):
                    if row["Close"] < row["bb_lower"]:
                        buy_signals += 1
                        applied_rules.append("Price below lower Bollinger Band")
                    elif row["Close"] > row["bb_upper"]:
                        sell_signals += 1
                        applied_rules.append("Price above upper Bollinger Band")

        # Momentum rules
        if "momentum_5" in row.index and not pd.isna(row["momentum_5"]):
            if row["momentum_5"] > 0.02:  # 2% positive momentum
                buy_signals += 1
                applied_rules.append("Positive 5-day momentum (>2%)")
            elif row["momentum_5"] < -0.02:  # 2% negative momentum
                sell_signals += 1
                applied_rules.append("Negative 5-day momentum (<-2%)")

        # Volatility rules
        if "volatility_20" in row.index and not pd.isna(row["volatility_20"]):
            if row["volatility_20"] > 0.03:  # High volatility
                hold_signals += 1
                applied_rules.append("High volatility (>3%) - hold")

        # Determine decision
        if buy_signals > sell_signals and buy_signals > hold_signals:
            decision = 2  # BUY
        elif sell_signals > buy_signals and sell_signals > hold_signals:
            decision = 0  # SELL
        else:
            decision = 1  # HOLD

        return decision, applied_rules

    def _calculate_confidence(self, row: pd.Series, rules: List[str]) -> float:
        """Calculate confidence score for a prediction.

        Args:
            row: Feature values.
            rules: List of applied rules.

        Returns:
            Confidence score between 0 and 1.
        """
        if not rules:
            return 0.5

        # More rules = higher confidence
        base_confidence = min(0.5 + (len(rules) * 0.1), 1.0)

        # Adjust based on signal strength
        if "rsi" in row.index and not pd.isna(row["rsi"]):
            rsi = row["rsi"]
            if rsi < 20 or rsi > 80:  # Extreme values
                base_confidence += 0.1

        return min(base_confidence, 1.0)

    def get_explanation(self, X: Union[np.ndarray, pd.DataFrame]) -> List[Dict]:
        """Get explanations for predictions.

        Args:
            X: Features to explain.

        Returns:
            List of explanation dictionaries.
        """
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        explanations = []

        for idx, row in X.iterrows():
            decision, rules = self._apply_rules(row)
            confidence = self._calculate_confidence(row, rules)

            explanation = {
                "index": idx,
                "decision": self.decision_classes[decision],
                "decision_code": decision,
                "confidence": confidence,
                "rules_applied": rules,
                "buy_signals": sum(1 for r in rules if "buy" in r.lower() or "bullish" in r.lower()),
                "sell_signals": sum(1 for r in rules if "sell" in r.lower() or "bearish" in r.lower()),
                "hold_signals": sum(1 for r in rules if "hold" in r.lower()),
            }
            explanations.append(explanation)

        return explanations

    def add_custom_rule(
        self,
        rule_name: str,
        condition: callable,
        signal: str = "buy",
    ) -> None:
        """Add a custom rule to the model.

        Args:
            rule_name: Name of the rule.
            condition: Function that takes a row and returns True if rule applies.
            signal: Signal type ('buy', 'sell', or 'hold').
        """
        # This would require modifying the _apply_rules method
        # For now, we'll just log it
        logger.info(f"Custom rule '{rule_name}' would be added with {signal} signal")
        logger.warning("Custom rules not yet implemented - requires refactoring")

    def get_rule_summary(self) -> Dict:
        """Get a summary of the rules being used.

        Returns:
            Dictionary with rule information.
        """
        return {
            "thresholds": self.thresholds,
            "decision_classes": self.decision_classes,
            "rule_categories": [
                "RSI (oversold/overbought)",
                "Moving Average crossover",
                "MACD signal",
                "Bollinger Bands",
                "Momentum",
                "Volatility",
            ],
        }

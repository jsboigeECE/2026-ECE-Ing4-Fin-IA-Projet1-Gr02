"""Argument builder for structuring explanations into coherent arguments."""

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


class Argument:
    """Represents a single argument in the argumentation system."""

    def __init__(
        self,
        premise: str,
        conclusion: str,
        strength: float,
        argument_type: str = "support",
        evidence: Optional[Dict] = None,
    ):
        """Initialize an Argument.

        Args:
            premise: The premise of the argument.
            conclusion: The conclusion derived from the premise.
            strength: Strength of the argument (0-1).
            argument_type: Type of argument ('support', 'oppose', 'neutral').
            evidence: Evidence supporting the argument.
        """
        self.premise = premise
        self.conclusion = conclusion
        self.strength = strength
        self.argument_type = argument_type
        self.evidence = evidence or {}

    def to_dict(self) -> Dict:
        """Convert argument to dictionary.

        Returns:
            Dictionary representation of the argument.
        """
        return {
            "premise": self.premise,
            "conclusion": self.conclusion,
            "strength": self.strength,
            "argument_type": self.argument_type,
            "evidence": self.evidence,
        }


class ArgumentBuilder:
    """Build structured arguments from XAI explanations."""

    def __init__(self, decision_classes: Optional[List[str]] = None):
        """Initialize the ArgumentBuilder.

        Args:
            decision_classes: List of decision class names.
        """
        self.decision_classes = decision_classes or Config.DECISION_CLASSES

    def build_arguments_from_shap(
        self,
        shap_explanation: Dict,
        prediction: int,
        confidence: float,
    ) -> List[Argument]:
        """Build arguments from SHAP explanation.

        Args:
            shap_explanation: SHAP explanation dictionary.
            prediction: Predicted class.
            confidence: Prediction confidence.

        Returns:
            List of arguments.
        """
        arguments = []
        decision_label = self.decision_classes[prediction]

        # Build main conclusion argument
        main_arg = Argument(
            premise=f"Based on the analysis of {len(shap_explanation['feature_names'])} features",
            conclusion=f"The recommendation is {decision_label}",
            strength=confidence,
            argument_type="support",
            evidence={"method": "SHAP", "confidence": confidence},
        )
        arguments.append(main_arg)

        # Build feature-based arguments
        for feature_info in shap_explanation["feature_importance"][:5]:
            feature = feature_info["feature"]
            shap_value = feature_info["shap_value"]
            direction = feature_info["direction"]

            if direction == "positive":
                premise = f"{feature} has a positive impact on the {decision_label} recommendation"
            else:
                premise = f"{feature} has a negative impact on the {decision_label} recommendation"

            arg = Argument(
                premise=premise,
                conclusion=f"Supports {decision_label} recommendation",
                strength=min(abs(shap_value), 1.0),
                argument_type="support",
                evidence={
                    "feature": feature,
                    "shap_value": shap_value,
                    "method": "SHAP",
                },
            )
            arguments.append(arg)

        return arguments

    def build_arguments_from_lime(
        self,
        lime_explanation: Dict,
        prediction: int,
    ) -> List[Argument]:
        """Build arguments from LIME explanation.

        Args:
            lime_explanation: LIME explanation dictionary.
            prediction: Predicted class.

        Returns:
            List of arguments.
        """
        arguments = []
        decision_label = self.decision_classes[prediction]

        # Build main conclusion argument
        main_arg = Argument(
            premise=f"Local analysis of the instance",
            conclusion=f"The recommendation is {decision_label}",
            strength=lime_explanation["score"],
            argument_type="support",
            evidence={"method": "LIME", "score": lime_explanation["score"]},
        )
        arguments.append(main_arg)

        # Build feature-based arguments
        for feature_info in lime_explanation["features"][:5]:
            feature = feature_info["feature"]
            weight = feature_info["weight"]
            direction = feature_info["direction"]

            if direction == "positive":
                premise = f"{feature} increases the probability of {decision_label}"
            else:
                premise = f"{feature} decreases the probability of {decision_label}"

            arg = Argument(
                premise=premise,
                conclusion=f"Supports {decision_label} recommendation",
                strength=min(abs(weight), 1.0),
                argument_type="support",
                evidence={
                    "feature": feature,
                    "weight": weight,
                    "method": "LIME",
                },
            )
            arguments.append(arg)

        return arguments

    def build_arguments_from_rules(
        self,
        rule_explanation: Dict,
        prediction: int,
    ) -> List[Argument]:
        """Build arguments from rule-based explanation.

        Args:
            rule_explanation: Rule-based explanation dictionary.
            prediction: Predicted class.

        Returns:
            List of arguments.
        """
        arguments = []
        decision_label = self.decision_classes[prediction]

        # Build main conclusion argument
        main_arg = Argument(
            premise=f"Based on {len(rule_explanation['rules_applied'])} technical analysis rules",
            conclusion=f"The recommendation is {decision_label}",
            strength=rule_explanation["confidence"],
            argument_type="support",
            evidence={"method": "Rules", "confidence": rule_explanation["confidence"]},
        )
        arguments.append(main_arg)

        # Build rule-based arguments
        for rule in rule_explanation["rules_applied"]:
            arg = Argument(
                premise=f"Technical indicator: {rule}",
                conclusion=f"Supports {decision_label} recommendation",
                strength=0.8,  # Fixed strength for rule-based arguments
                argument_type="support",
                evidence={"rule": rule, "method": "Rules"},
            )
            arguments.append(arg)

        return arguments

    def build_arguments_from_counterfactual(
        self,
        counterfactual: Dict,
    ) -> List[Argument]:
        """Build arguments from counterfactual explanation.

        Args:
            counterfactual: Counterfactual explanation dictionary.

        Returns:
            List of arguments.
        """
        arguments = []

        if not counterfactual["success"]:
            return arguments

        original_label = counterfactual["original_prediction_label"]
        target_label = counterfactual["target_class_label"]

        # Build main counterfactual argument
        main_arg = Argument(
            premise=f"To change the recommendation from {original_label} to {target_label}",
            conclusion=f"Specific changes in market conditions would be required",
            strength=1.0 - min(counterfactual["distance"], 1.0),
            argument_type="neutral",
            evidence={"method": "Counterfactual", "distance": counterfactual["distance"]},
        )
        arguments.append(main_arg)

        # Build change-based arguments
        for change in counterfactual["changes"][:5]:
            feature = change["feature"]
            direction = change["direction"]
            original_val = change["original_value"]
            cf_val = change["counterfactual_value"]

            premise = (
                f"{feature} would need to {direction} from {original_val:.2f} to {cf_val:.2f}"
            )
            conclusion = f"Would change recommendation to {target_label}"

            arg = Argument(
                premise=premise,
                conclusion=conclusion,
                strength=1.0 - min(abs(change["percent_change"]) / 100, 1.0),
                argument_type="neutral",
                evidence={
                    "feature": feature,
                    "change": change["change"],
                    "method": "Counterfactual",
                },
            )
            arguments.append(arg)

        return arguments

    def combine_arguments(
        self,
        shap_args: Optional[List[Argument]] = None,
        lime_args: Optional[List[Argument]] = None,
        rule_args: Optional[List[Argument]] = None,
        counterfactual_args: Optional[List[Argument]] = None,
    ) -> Dict:
        """Combine arguments from multiple sources.

        Args:
            shap_args: Arguments from SHAP.
            lime_args: Arguments from LIME.
            rule_args: Arguments from rules.
            counterfactual_args: Arguments from counterfactual.

        Returns:
            Combined argument structure.
        """
        all_arguments = []

        if shap_args:
            all_arguments.extend(shap_args)
        if lime_args:
            all_arguments.extend(lime_args)
        if rule_args:
            all_arguments.extend(rule_args)
        if counterfactual_args:
            all_arguments.extend(counterfactual_args)

        # Group arguments by type
        support_args = [arg for arg in all_arguments if arg.argument_type == "support"]
        oppose_args = [arg for arg in all_arguments if arg.argument_type == "oppose"]
        neutral_args = [arg for arg in all_arguments if arg.argument_type == "neutral"]

        # Calculate overall strength
        if support_args:
            avg_support_strength = np.mean([arg.strength for arg in support_args])
        else:
            avg_support_strength = 0.0

        return {
            "all_arguments": [arg.to_dict() for arg in all_arguments],
            "support_arguments": [arg.to_dict() for arg in support_args],
            "oppose_arguments": [arg.to_dict() for arg in oppose_args],
            "neutral_arguments": [arg.to_dict() for arg in neutral_args],
            "overall_strength": avg_support_strength,
            "argument_count": len(all_arguments),
        }

    def rank_arguments(
        self,
        arguments: List[Argument],
        top_n: int = 5,
    ) -> List[Argument]:
        """Rank arguments by strength.

        Args:
            arguments: List of arguments to rank.
            top_n: Number of top arguments to return.

        Returns:
            Ranked list of arguments.
        """
        ranked = sorted(arguments, key=lambda x: x.strength, reverse=True)
        return ranked[:top_n]

    def resolve_conflicts(
        self,
        arguments: List[Argument],
    ) -> List[Argument]:
        """Resolve conflicts between arguments.

        Args:
            arguments: List of arguments.

        Returns:
            List of arguments with conflicts resolved.
        """
        # Group arguments by conclusion
        conclusion_groups = {}
        for arg in arguments:
            if arg.conclusion not in conclusion_groups:
                conclusion_groups[arg.conclusion] = []
            conclusion_groups[arg.conclusion].append(arg)

        # For each conclusion, keep only the strongest argument
        resolved = []
        for conclusion, args in conclusion_groups.items():
            strongest = max(args, key=lambda x: x.strength)
            resolved.append(strongest)

        return resolved

"""Explanation generator for creating natural language explanations."""

import logging
from typing import Dict, List, Optional

from .argument_builder import Argument, ArgumentBuilder
from ..utils.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ExplanationGenerator:
    """Generate natural language explanations from structured arguments."""

    def __init__(
        self,
        argument_builder: Optional[ArgumentBuilder] = None,
        language: str = "fr",
    ):
        """Initialize the ExplanationGenerator.

        Args:
            argument_builder: ArgumentBuilder instance.
            language: Language for explanations ('fr' or 'en').
        """
        self.argument_builder = argument_builder or ArgumentBuilder()
        self.language = language
        self.decision_classes = Config.DECISION_CLASSES

        # Translation templates
        self.templates = self._get_templates()

    def _get_templates(self) -> Dict:
        """Get language templates for explanations.

        Returns:
            Dictionary of templates.
        """
        if self.language == "fr":
            return {
                "summary": "Recommandation : {decision}",
                "confidence": "Niveau de confiance : {confidence:.1%}",
                "main_reason": "Raison principale : {reason}",
                "supporting_factors": "Facteurs de soutien :",
                "opposing_factors": "Facteurs défavorables :",
                "counterfactual_intro": "Pour changer la recommandation de {original} à {target},",
                "counterfactual_changes": "les changements suivants seraient nécessaires :",
                "feature_impact": "{feature} a un impact {direction} sur la recommandation.",
                "rule_based": "Basé sur l'analyse technique : {rule}",
                "ml_based": "Le modèle ML indique : {reason}",
                "hybrid_source": "Source de la décision : {source}",
            }
        else:
            return {
                "summary": "Recommendation: {decision}",
                "confidence": "Confidence level: {confidence:.1%}",
                "main_reason": "Main reason: {reason}",
                "supporting_factors": "Supporting factors:",
                "opposing_factors": "Opposing factors:",
                "counterfactual_intro": "To change recommendation from {original} to {target},",
                "counterfactual_changes": "the following changes would be needed:",
                "feature_impact": "{feature} has a {direction} impact on the recommendation.",
                "rule_based": "Based on technical analysis: {rule}",
                "ml_based": "The ML model indicates: {reason}",
                "hybrid_source": "Decision source: {source}",
            }

    def generate_summary(
        self,
        prediction: int,
        confidence: float,
        decision_source: str = "Hybrid",
    ) -> str:
        """Generate a summary explanation.

        Args:
            prediction: Predicted class.
            confidence: Prediction confidence.
            decision_source: Source of the decision.

        Returns:
            Summary explanation text.
        """
        decision_label = self.decision_classes[prediction]

        summary = self.templates["summary"].format(decision=decision_label)
        confidence_text = self.templates["confidence"].format(confidence=confidence)
        source_text = self.templates["hybrid_source"].format(source=decision_source)

        return f"{summary}\n{confidence_text}\n{source_text}"

    def generate_detailed_explanation(
        self,
        arguments: Dict,
        prediction: int,
        confidence: float,
    ) -> str:
        """Generate a detailed explanation.

        Args:
            arguments: Combined arguments dictionary.
            prediction: Predicted class.
            confidence: Prediction confidence.

        Returns:
            Detailed explanation text.
        """
        lines = []

        # Summary
        lines.append(self.generate_summary(prediction, confidence))

        # Main reason
        if arguments["support_arguments"]:
            main_arg = arguments["support_arguments"][0]
            lines.append(self.templates["main_reason"].format(reason=main_arg["premise"]))

        # Supporting factors
        if len(arguments["support_arguments"]) > 1:
            lines.append(self.templates["supporting_factors"])
            for arg in arguments["support_arguments"][1:4]:
                lines.append(f"  - {arg['premise']}")

        # Opposing factors
        if arguments["oppose_arguments"]:
            lines.append(self.templates["opposing_factors"])
            for arg in arguments["oppose_arguments"][:3]:
                lines.append(f"  - {arg['premise']}")

        # Counterfactual (if available)
        if arguments["neutral_arguments"]:
            for arg in arguments["neutral_arguments"]:
                if "counterfactual" in arg.get("evidence", {}).get("method", ""):
                    lines.append(self.templates["counterfactual_intro"].format(
                        original=arg["evidence"].get("original", ""),
                        target=arg["evidence"].get("target", ""),
                    ))
                    lines.append(self.templates["counterfactual_changes"])

        return "\n".join(lines)

    def generate_feature_explanation(
        self,
        feature_name: str,
        feature_value: float,
        shap_value: float,
        direction: str,
    ) -> str:
        """Generate an explanation for a single feature.

        Args:
            feature_name: Name of the feature.
            feature_value: Value of the feature.
            shap_value: SHAP value for the feature.
            direction: Direction of impact ('positive' or 'negative').

        Returns:
            Feature explanation text.
        """
        direction_text = "positif" if direction == "positive" else "négatif"
        if self.language == "en":
            direction_text = "positive" if direction == "positive" else "negative"

        return self.templates["feature_impact"].format(
            feature=feature_name,
            direction=direction_text,
        )

    def generate_counterfactual_explanation(
        self,
        counterfactual: Dict,
    ) -> str:
        """Generate an explanation for a counterfactual scenario.

        Args:
            counterfactual: Counterfactual explanation dictionary.

        Returns:
            Counterfactual explanation text.
        """
        if not counterfactual["success"]:
            return "Impossible de générer un scénario contrefactuel valide."

        original = counterfactual["original_prediction_label"]
        target = counterfactual["target_class_label"]

        lines = [
            self.templates["counterfactual_intro"].format(original=original, target=target),
            self.templates["counterfactual_changes"],
        ]

        for change in counterfactual["changes"][:5]:
            direction = "augmenter" if change["direction"] == "increase" else "diminuer"
            if self.language == "en":
                direction = "increase" if change["direction"] == "increase" else "decrease"

            lines.append(
                f"  - {direction} {change['feature']} de {change['original_value']:.2f} "
                f"à {change['counterfactual_value']:.2f}"
            )

        return "\n".join(lines)

    def generate_multi_level_explanation(
        self,
        arguments: Dict,
        prediction: int,
        confidence: float,
        level: str = "medium",
    ) -> str:
        """Generate explanation at different detail levels.

        Args:
            arguments: Combined arguments dictionary.
            prediction: Predicted class.
            confidence: Prediction confidence.
            level: Detail level ('simple', 'medium', 'detailed').

        Returns:
            Explanation text at specified level.
        """
        if level == "simple":
            return self.generate_summary(prediction, confidence)
        elif level == "medium":
            return self.generate_detailed_explanation(arguments, prediction, confidence)
        elif level == "detailed":
            return self.generate_technical_explanation(arguments, prediction, confidence)
        else:
            return self.generate_detailed_explanation(arguments, prediction, confidence)

    def generate_technical_explanation(
        self,
        arguments: Dict,
        prediction: int,
        confidence: float,
    ) -> str:
        """Generate a technical explanation with all details.

        Args:
            arguments: Combined arguments dictionary.
            prediction: Predicted class.
            confidence: Prediction confidence.

        Returns:
            Technical explanation text.
        """
        lines = []

        # Summary
        lines.append(self.generate_summary(prediction, confidence))
        lines.append("")

        # All arguments
        lines.append("=== Arguments détaillés ===")
        lines.append(f"Force globale : {arguments['overall_strength']:.2%}")
        lines.append(f"Nombre d'arguments : {arguments['argument_count']}")
        lines.append("")

        # Support arguments
        if arguments["support_arguments"]:
            lines.append("Arguments de soutien :")
            for i, arg in enumerate(arguments["support_arguments"], 1):
                lines.append(f"{i}. {arg['premise']}")
                lines.append(f"   Force : {arg['strength']:.2%}")
                if arg.get("evidence"):
                    lines.append(f"   Preuve : {arg['evidence']}")
            lines.append("")

        # Oppose arguments
        if arguments["oppose_arguments"]:
            lines.append("Arguments opposants :")
            for i, arg in enumerate(arguments["oppose_arguments"], 1):
                lines.append(f"{i}. {arg['premise']}")
                lines.append(f"   Force : {arg['strength']:.2%}")
            lines.append("")

        # Neutral arguments
        if arguments["neutral_arguments"]:
            lines.append("Arguments neutres :")
            for i, arg in enumerate(arguments["neutral_arguments"], 1):
                lines.append(f"{i}. {arg['premise']}")
                lines.append(f"   Force : {arg['strength']:.2%}")

        return "\n".join(lines)

    def generate_comparison_explanation(
        self,
        explanations: List[Dict],
        tickers: List[str],
    ) -> str:
        """Generate a comparison explanation for multiple assets.

        Args:
            explanations: List of explanation dictionaries.
            tickers: List of ticker symbols.

        Returns:
            Comparison explanation text.
        """
        lines = ["=== Comparaison des recommandations ===\n"]

        for ticker, exp in zip(tickers, explanations):
            prediction = exp.get("prediction", 1)
            confidence = exp.get("confidence", 0.5)
            decision_label = self.decision_classes[prediction]

            lines.append(f"{ticker}: {decision_label} (confiance: {confidence:.1%})")

            if exp.get("main_reason"):
                lines.append(f"  Raison principale : {exp['main_reason']}")

            lines.append("")

        return "\n".join(lines)

    def format_for_display(
        self,
        explanation: str,
        format_type: str = "text",
    ) -> str:
        """Format explanation for display.

        Args:
            explanation: Explanation text.
            format_type: Format type ('text', 'html', 'markdown').

        Returns:
            Formatted explanation.
        """
        if format_type == "text":
            return explanation
        elif format_type == "markdown":
            return self._to_markdown(explanation)
        elif format_type == "html":
            return self._to_html(explanation)
        else:
            return explanation

    def _to_markdown(self, text: str) -> str:
        """Convert text to markdown format.

        Args:
            text: Plain text.

        Returns:
            Markdown formatted text.
        """
        lines = text.split("\n")
        markdown_lines = []

        for line in lines:
            if line.startswith("==="):
                # Convert === to markdown header
                header = line.replace("=", "").strip()
                markdown_lines.append(f"## {header}")
            elif line.startswith("- "):
                # Keep bullet points
                markdown_lines.append(line)
            else:
                markdown_lines.append(line)

        return "\n".join(markdown_lines)

    def _to_html(self, text: str) -> str:
        """Convert text to HTML format.

        Args:
            text: Plain text.

        Returns:
            HTML formatted text.
        """
        html = text.replace("\n", "<br>")
        html = html.replace("===", "<h3>")
        html = html.replace("===", "</h3>")
        return html

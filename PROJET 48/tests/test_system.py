"""Test script for the XAI Investment system."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd

from data import DataLoader, DataPreprocessor
from models import HybridModel
from xai import SHAPExplainer, LIMEExplainer, CounterfactualExplainer
from argumentation import ArgumentBuilder, ExplanationGenerator
from utils.config import Config


def test_data_loading():
    """Test data loading."""
    print("=" * 50)
    print("TEST 1: Chargement des données")
    print("=" * 50)

    loader = DataLoader()
    data = loader.load_yahoo_data("AAPL", period="2y")

    if data.empty:
        print("❌ Échec : Impossible de charger les données")
        return False

    print(f"✅ Succès : Données chargées ({len(data)} lignes)")
    print(f"Colonnes : {list(data.columns)}")
    return data


def test_preprocessing(data):
    """Test data preprocessing."""
    print("\n" + "=" * 50)
    print("TEST 2: Prétraitement des données")
    print("=" * 50)

    preprocessor = DataPreprocessor()

    # Clean data
    data = preprocessor.clean_data(data)
    print(f"✅ Nettoyage : {len(data)} lignes")

    # Compute indicators
    data = preprocessor.compute_technical_indicators(data)
    print(f"✅ Indicateurs calculés : {len(data.columns)} colonnes")

    # Create target
    data = preprocessor.create_target_variable(data)
    print(f"✅ Variable cible créée")
    print(f"   Distribution : {data['target'].value_counts().to_dict()}")

    # Prepare features
    features_df = preprocessor.prepare_features(data)
    print(f"✅ Features préparées : {len(features_df.columns)} colonnes")

    return data, features_df, preprocessor


def test_model_training(features_df, preprocessor):
    """Test model training."""
    print("\n" + "=" * 50)
    print("TEST 3: Entraînement du modèle")
    print("=" * 50)

    # Split data
    train, val, test = preprocessor.split_data(features_df, time_series_split=True)
    print(f"✅ Split : Train={len(train)}, Val={len(val)}, Test={len(test)}")

    # Train model
    X_train, y_train = preprocessor.get_feature_importance_data(train)
    model = HybridModel()
    model.train(X_train, y_train)
    print(f"✅ Modèle entraîné")

    # Evaluate
    X_test, y_test = preprocessor.get_feature_importance_data(test)
    metrics = model.evaluate(X_test, y_test)
    print(f"✅ Évaluation : Accuracy={metrics['accuracy']:.2%}")

    return model, X_test, y_test


def test_xai_explanations(model, X_test, X_train):
    """Test XAI explanations."""
    print("\n" + "=" * 50)
    print("TEST 4: Explications XAI")
    print("=" * 50)

    # SHAP
    try:
        shap_explainer = SHAPExplainer(model.ml_model.model, X_train)
        shap_exp = shap_explainer.explain_instance(X_test, index=0)
        print(f"✅ SHAP : {len(shap_exp['feature_importance'])} features expliquées")
    except Exception as e:
        print(f"⚠️  SHAP : {e}")

    # LIME
    try:
        lime_explainer = LIMEExplainer(model.ml_model.model, X_train)
        lime_exp = lime_explainer.explain_instance(X_test, index=0)
        print(f"✅ LIME : {len(lime_exp['features'])} features expliquées")
    except Exception as e:
        print(f"⚠️  LIME : {e}")

    # Counterfactual
    try:
        cf_explainer = CounterfactualExplainer(model.ml_model.model)
        cf_exp = cf_explainer.generate_counterfactual(X_test, index=0)
        print(f"✅ Counterfactual : Succès={cf_exp['success']}")
    except Exception as e:
        print(f"⚠️  Counterfactual : {e}")


def test_argumentation(model, X_test):
    """Test argumentation system."""
    print("\n" + "=" * 50)
    print("TEST 5: Système d'argumentation")
    print("=" * 50)

    argument_builder = ArgumentBuilder()
    explanation_generator = ExplanationGenerator(language="fr")

    # Get prediction
    prediction = model.predict(X_test[:1])[0]
    confidence = model.predict_with_details(X_test[:1])["hybrid_confidence"][0]

    # Generate summary
    summary = explanation_generator.generate_summary(prediction, confidence)
    print(f"✅ Résumé généré :\n{summary}")

    # Get rule explanations
    rule_explanations = model.rule_model.get_explanation(X_test[:1])
    if rule_explanations:
        print(f"✅ Règles : {len(rule_explanations[0]['rules_applied'])} appliquées")


def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("TESTS DU SYSTÈME XAI INVESTMENT")
    print("=" * 50)

    try:
        # Test 1: Data loading
        data = test_data_loading()
        if data is False:
            return

        # Test 2: Preprocessing
        data, features_df, preprocessor = test_preprocessing(data)

        # Test 3: Model training
        model, X_test, y_test = test_model_training(features_df, preprocessor)

        # Test 4: XAI explanations
        X_train, _ = preprocessor.get_feature_importance_data(
            preprocessor.prepare_features(data)
        )
        test_xai_explanations(model, X_test, X_train)

        # Test 5: Argumentation
        test_argumentation(model, X_test)

        print("\n" + "=" * 50)
        print("✅ TOUS LES TESTS TERMINÉS AVEC SUCCÈS")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

"""Main Streamlit application for XAI Investment recommendations."""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="XAI Investment",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recommendation-buy {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .recommendation-sell {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .recommendation-hold {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    st.markdown('<h1 class="main-header">📈 IA Explicable pour Décisions d\'Investissement</h1>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Ticker selection
        ticker = st.text_input("Symbole boursier", value="AAPL", help="Ex: AAPL, MSFT, GOOGL")

        # Period selection
        period = st.selectbox("Période", ["1y", "2y", "5y", "max"], index=2)

        # Model settings
        st.subheader("Paramètres du modèle")
        ml_weight = st.slider("Poids ML", 0.0, 1.0, 0.6, 0.1)
        rule_weight = 1.0 - ml_weight
        confidence_threshold = st.slider("Seuil de confiance", 0.0, 1.0, 0.7, 0.05)

        # Explanation settings
        st.subheader("Paramètres d'explication")
        explanation_level = st.selectbox("Niveau de détail", ["simple", "medium", "detailed"])
        num_features = st.slider("Nombre de features", 3, 10, 5)

        st.divider()
        st.write("Équipe : Lans Léo, Esnault Wandrille, Jezequel Martin")

    # Step 1: Load data
    st.header("Étape 1 : Chargement des données")
    with st.spinner("Chargement des données..."):
        try:
            from src.data import DataLoader
            loader = DataLoader()
            data = loader.load_yahoo_data(ticker, period=period)
            st.success(f"✅ Données chargées : {len(data)} lignes")
        except Exception as e:
            st.error(f"❌ Erreur de chargement : {e}")
            logger.error(f"Data loading error: {e}")
            return

    if data.empty:
        st.error(f"Impossible de charger les données pour {ticker}")
        return

    # Step 2: Preprocess data
    st.header("Étape 2 : Prétraitement des données")
    with st.spinner("Prétraitement des données..."):
        try:
            from src.data import DataPreprocessor
            preprocessor = DataPreprocessor()
            data = preprocessor.clean_data(data)
            st.success("✅ Nettoyage terminé")
            
            data = preprocessor.compute_technical_indicators(data)
            st.success("✅ Indicateurs calculés")
            
            data = preprocessor.create_target_variable(data)
            st.success("✅ Variable cible créée")
        except Exception as e:
            st.error(f"❌ Erreur de prétraitement : {e}")
            logger.error(f"Preprocessing error: {e}")
            return

    # Step 3: Prepare features
    st.header("Étape 3 : Préparation des features")
    try:
        features_df = preprocessor.prepare_features(data)
        # Use full data with target column for get_feature_importance_data
        X, y = preprocessor.get_feature_importance_data(data)
        st.success(f"✅ Features préparées : {X.shape[0]} lignes, {X.shape[1]} colonnes")
    except Exception as e:
        st.error(f"❌ Erreur de préparation : {e}")
        logger.error(f"Feature preparation error: {e}")
        return

    # Step 4: Split data
    st.header("Étape 4 : Division des données")
    try:
        # Use full data with target column for split_data
        train, val, test = preprocessor.split_data(data, time_series_split=True)
        st.success(f"✅ Division : Train={len(train)}, Val={len(val)}, Test={len(test)}")
    except Exception as e:
        st.error(f"❌ Erreur de division : {e}")
        logger.error(f"Data split error: {e}")
        return

    # Step 5: Train model
    st.header("Étape 5 : Entraînement du modèle")
    with st.spinner("Entraînement du modèle..."):
        try:
            from src.models import HybridModel
            X_train, y_train = preprocessor.get_feature_importance_data(train)
            # Create DataFrame with column names for training
            # Use X_train columns directly (excluding target and forward_return)
            feature_cols = [col for col in train.columns if col not in ["target", "forward_return"]]
            # X_train has 25 columns (24 features + target), use only first 24
            X_train_df = pd.DataFrame(X_train[:, :-1], columns=feature_cols)
            model = HybridModel()
            # Pass feature names to model
            model.train(X_train_df, y_train)
            st.success("✅ Modèle entraîné")
        except Exception as e:
            st.error(f"❌ Erreur d'entraînement : {e}")
            logger.error(f"Model training error: {e}")
            return

    # Step 6: Get prediction
    st.header("Étape 6 : Prédiction")
    try:
        latest_features = X[-1:].copy()
        # Use only features (exclude target column)
        latest_features = latest_features[:, :-1]
        prediction = model.predict(latest_features)[0]
        details = model.predict_with_details(latest_features)
        st.success(f"✅ Prédiction : {prediction}")
    except Exception as e:
        st.error(f"❌ Erreur de prédiction : {e}")
        logger.error(f"Prediction error: {e}")
        return

    # Display recommendation
    st.header("📊 Recommandation Actuelle")

    try:
        from src.utils.config import Config
        decision_label = Config.DECISION_CLASSES[prediction]
        confidence = details["hybrid_confidence"][0]
        source = details["decision_source"][0]

        if prediction == 2:  # BUY
            st.markdown(f'<div class="recommendation-buy"><h2>🟢 ACHETER</h2></div>', unsafe_allow_html=True)
        elif prediction == 0:  # SELL
            st.markdown(f'<div class="recommendation-sell"><h2>🔴 VENDRE</h2></div>', unsafe_allow_html=True)
        else:  # HOLD
            st.markdown(f'<div class="recommendation-hold"><h2>🟡 CONSERVER</h2></div>', unsafe_allow_html=True)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Confiance", f"{confidence:.1%}")
        with col2:
            st.metric("Source", source)
        with col3:
            st.metric("Symbole", ticker)
    except Exception as e:
        st.error(f"❌ Erreur d'affichage : {e}")
        logger.error(f"Display error: {e}")

    # Price chart
    st.header("📈 Graphique des prix")
    try:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Prix"
        ))
        fig.update_layout(
            title=f"Prix de {ticker}",
            xaxis_title="Date",
            yaxis_title="Prix",
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Erreur de graphique : {e}")
        logger.error(f"Chart error: {e}")

    # Tabs for detailed analysis
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Explications", "🔍 Analyse détaillée", "🔄 Scénarios", "⚙️ Paramètres"])

    with tab1:
        st.header("📋 Explications de la recommandation")

        try:
            from src.argumentation import ArgumentBuilder, ExplanationGenerator
            argument_builder = ArgumentBuilder()
            explanation_generator = ExplanationGenerator(language="fr")

            # Convert latest_features to DataFrame with column names for rule explanations
            latest_features_df = pd.DataFrame(latest_features, columns=preprocessor.feature_columns)

            # Get rule explanations
            rule_explanations = model.rule_model.get_explanation(latest_features_df)

            # Generate summary
            summary = explanation_generator.generate_summary(prediction, confidence, source)
            st.info(summary)

            # Detailed explanations
            if rule_explanations:
                explanation = rule_explanations[0]
                
                # Overall sentiment
                st.subheader("📊 Analyse globale")
                buy_count = explanation["buy_signals"]
                sell_count = explanation["sell_signals"]
                hold_count = explanation["hold_signals"]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Signaux d'achat", buy_count, delta_color="normal")
                with col2:
                    st.metric("Signaux de vente", sell_count, delta_color="inverse")
                with col3:
                    st.metric("Signaux de maintien", hold_count)
                
                # Detailed rule explanations by category
                st.subheader("🔍 Analyse détaillée par indicateur")
                
                # Get current values for display
                current_values = latest_features_df.iloc[0].to_dict()
                
                # RSI Analysis
                if "rsi" in current_values and not pd.isna(current_values["rsi"]):
                    rsi_value = current_values["rsi"]
                    st.markdown("### 📈 RSI (Relative Strength Index)")
                    st.write(f"**Valeur actuelle :** {rsi_value:.2f}")
                    
                    if rsi_value < 30:
                        st.success("🟢 Le RSI est en zone de survente (<30), ce qui indique que le titre est potentiellement sous-évalué et pourrait rebondir.")
                    elif rsi_value > 70:
                        st.error("🔴 Le RSI est en zone de surachat (>70), ce qui indique que le titre est potentiellement surévalué et pourrait corriger.")
                    else:
                        st.info("🟡 Le RSI est dans une zone neutre (30-70), sans signal fort d'achat ou de vente.")
                    st.caption("Le RSI mesure la vitesse et l'amplitude des variations de prix. Un RSI < 30 suggère une opportunité d'achat, > 70 suggère une opportunité de vente.")
                
                # Moving Averages Analysis
                if "sma_20" in current_values and "sma_50" in current_values:
                    sma20 = current_values["sma_20"]
                    sma50 = current_values["sma_50"]
                    st.markdown("### 📊 Moyennes Mobiles")
                    st.write(f"**SMA 20 jours :** {sma20:.2f}")
                    st.write(f"**SMA 50 jours :** {sma50:.2f}")
                    
                    if sma20 > sma50:
                        st.success("🟢 La moyenne mobile courte (20j) est au-dessus de la moyenne mobile longue (50j), ce qui indique une tendance haussière.")
                    else:
                        st.error("🔴 La moyenne mobile courte (20j) est en dessous de la moyenne mobile longue (50j), ce qui indique une tendance baissière.")
                    st.caption("Les moyennes mobiles lissent les fluctuations de prix. Le croisement des moyennes signale des changements de tendance.")
                
                # MACD Analysis
                if "macd" in current_values and "macd_signal" in current_values:
                    macd = current_values["macd"]
                    macd_signal = current_values["macd_signal"]
                    st.markdown("### 📉 MACD")
                    st.write(f"**MACD :** {macd:.4f}")
                    st.write(f"**Signal :** {macd_signal:.4f}")
                    
                    if macd > macd_signal:
                        st.success("🟢 Le MACD est au-dessus de sa ligne de signal, ce qui indique un momentum haussier.")
                    else:
                        st.error("🔴 Le MACD est en dessous de sa ligne de signal, ce qui indique un momentum baissier.")
                    st.caption("Le MACD mesure la force de la tendance. Au-dessus du signal = momentum positif, en dessous = momentum négatif.")
                
                # Bollinger Bands Analysis
                if "bb_upper" in current_values and "bb_lower" in current_values and "Close" in current_values:
                    bb_upper = current_values["bb_upper"]
                    bb_lower = current_values["bb_lower"]
                    close_price = current_values["Close"]
                    st.markdown("### 📊 Bandes de Bollinger")
                    st.write(f"**Prix actuel :** {close_price:.2f}")
                    st.write(f"**Bande supérieure :** {bb_upper:.2f}")
                    st.write(f"**Bande inférieure :** {bb_lower:.2f}")
                    
                    if close_price < bb_lower:
                        st.success("🟢 Le prix est sous la bande inférieure, ce qui peut indiquer une opportunité d'achat (survente).")
                    elif close_price > bb_upper:
                        st.error("🔴 Le prix est au-dessus de la bande supérieure, ce qui peut indiquer une opportunité de vente (surachat).")
                    else:
                        st.info("🟡 Le prix est à l'intérieur des bandes, dans une zone normale.")
                    st.caption("Les bandes de Bollinger mesurent la volatilité. En dehors des bandes = situation extrême.")
                
                # Momentum Analysis
                if "momentum_5" in current_values and not pd.isna(current_values["momentum_5"]):
                    momentum = current_values["momentum_5"]
                    st.markdown("### 🚀 Momentum (5 jours)")
                    st.write(f"**Momentum :** {momentum*100:.2f}%")
                    
                    if momentum > 0.02:
                        st.success("🟢 Momentum positif fort (>2%), le prix monte rapidement.")
                    elif momentum < -0.02:
                        st.error("🔴 Momentum négatif fort (<-2%), le prix baisse rapidement.")
                    else:
                        st.info("🟡 Momentum neutre, pas de mouvement directionnel fort.")
                    st.caption("Le momentum mesure la vitesse de variation du prix sur une période donnée.")
                
                # Volatility Analysis
                if "volatility_20" in current_values and not pd.isna(current_values["volatility_20"]):
                    volatility = current_values["volatility_20"]
                    st.markdown("### 📊 Volatilité (20 jours)")
                    st.write(f"**Volatilité :** {volatility*100:.2f}%")
                    
                    if volatility > 0.03:
                        st.warning("⚠️ Volatilité élevée (>3%), le marché est instable. Prudence recommandée.")
                    else:
                        st.success("🟢 Volatilité normale, le marché est relativement stable.")
                    st.caption("La volatilité mesure l'amplitude des variations de prix. Plus elle est élevée, plus le marché est risqué.")
                
                # Summary of applied rules
                st.subheader("📋 Règles techniques appliquées")
                for rule in explanation["rules_applied"]:
                    st.write(f"• {rule}")
            else:
                st.warning("Aucune règle technique appliquée")
        except Exception as e:
            st.error(f"❌ Erreur d'explication : {e}")
            logger.error(f"Explanation error: {e}", exc_info=True)

    with tab2:
        st.header("🔍 Analyse détaillée")

        try:
            # Feature importance
            st.subheader("Importance des features")
            feature_importance = model.get_feature_importance()
            st.dataframe(feature_importance.head(10), use_container_width=True)

            # Feature importance chart
            top_10 = feature_importance.head(10)
            fig = go.Figure(go.Bar(
                x=top_10["importance"].values,
                y=top_10["feature"].values,
                orientation="h"
            ))
            fig.update_layout(
                title="Top 10 Features",
                xaxis_title="Importance",
                yaxis_title="Feature",
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Erreur d'analyse : {e}")
            logger.error(f"Analysis error: {e}")

    with tab3:
        st.header("🔄 Scénarios contrefactuels")

        st.info("Les scénarios contrefactuels montrent comment changer les conditions pour obtenir une recommandation différente.")

        try:
            from src.xai import CounterfactualExplainer
            
            # DEBUG: Log feature names and model info
            logger.info(f"DEBUG preprocessor.feature_columns: {preprocessor.feature_columns}")
            logger.info(f"DEBUG model.ml_model.feature_names: {model.ml_model.feature_names}")
            logger.info(f"DEBUG latest_features shape: {latest_features.shape}")
            
            # Use feature names from the ML model
            feature_names = model.ml_model.feature_names if model.ml_model.feature_names else preprocessor.feature_columns
            logger.info(f"DEBUG Using feature_names: {feature_names}")
            
            cf_explainer = CounterfactualExplainer(model.ml_model.model, feature_names=feature_names)
            
            # Generate multiple counterfactuals
            num_scenarios = st.slider("Nombre de scénarios", 1, 5, 3)
            counterfactuals = cf_explainer.generate_multiple_counterfactuals(
                latest_features, num_counterfactuals=num_scenarios, target_class=None
            )
            
            # Filter successful counterfactuals
            successful_cfs = [cf for cf in counterfactuals if cf["success"]]
            
            if successful_cfs:
                st.success(f"{len(successful_cfs)} scénario(s) contrefactuel(s) généré(s) avec succès !")
                
                # Display each counterfactual
                for i, cf in enumerate(successful_cfs, 1):
                    st.subheader(f"Scénario {i}: {cf['original_prediction_label']} → {cf['target_class_label']}")
                    
                    # Display changes
                    changes_df = pd.DataFrame(cf["changes"][:5])
                    if not changes_df.empty:
                        st.dataframe(changes_df, use_container_width=True)
                    
                    # Text explanation
                    cf_text = cf_explainer.get_counterfactual_text(cf)
                    st.write(cf_text)
                    
                    # Distance metric
                    st.caption(f"Distance: {cf['distance']:.4f}")
                    
                    st.divider()
                
                # Summary of all counterfactuals
                summary = cf_explainer.get_counterfactual_summary(counterfactuals)
                st.subheader("Résumé des scénarios")
                st.write(f"**Total:** {summary['total']} | **Réussis:** {summary['successful']} | **Échoués:** {summary['failed']}")
                if summary['average_distance']:
                    st.write(f"**Distance moyenne:** {summary['average_distance']:.4f}")
                
                if summary['common_changes']:
                    st.subheader("Changements les plus fréquents")
                    common_df = pd.DataFrame(summary['common_changes'][:5])
                    st.dataframe(common_df, use_container_width=True)
            else:
                st.warning("Impossible de générer des scénarios contrefactuels valides.")
                if counterfactuals:
                    st.write(f"Raison: {counterfactuals[0].get('counterfactual_prediction_label', 'Inconnu')}")
        except Exception as e:
            st.error(f"❌ Erreur de scénario : {e}")
            logger.error(f"Counterfactual error: {e}", exc_info=True)

    with tab4:
        st.header("⚙️ Paramètres du modèle")

        try:
            st.subheader("Configuration hybride")
            st.write(f"**Poids ML :** {ml_weight:.1%}")
            st.write(f"**Poids Règles :** {rule_weight:.1%}")
            st.write(f"**Seuil de confiance :** {confidence_threshold:.1%}")

            st.subheader("Informations sur le modèle")
            model_summary = model.get_model_summary()
            for key, value in model_summary.items():
                st.write(f"**{key} :** {value}")
        except Exception as e:
            st.error(f"❌ Erreur de paramètres : {e}")
            logger.error(f"Parameters error: {e}")

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Projet 48 - IA Explicable pour Décisions d'Investissement</p>
        <p>Équipe : Lans Léo, Esnault Wandrille, Jezequel Martin</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

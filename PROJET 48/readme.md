EQUIPE
Lans Léo
Esnault Wandrille
Jezequel Martin 

Projet : 48 - IA explicable pour décisions d'investissement

Sujet : 
Description du problème et contexte Les modèles ML en finance (trading, gestion de portefeuille) sont souvent des boîtes noires incompatibles avec les exigences réglementaires de justification des décisions. L'IA explicable (XAI) combine l'argumentation computationnelle avec les techniques d'explicabilité pour fournir des justifications compréhensibles et auditables des recommandations d'investissement.

Références multiples

CFA Institute : Explainable AI in Finance: Addressing the Needs of Diverse Stakeholders - CFA Institute 2025
Revue systématique : A Systematic Review of Explainable AI in Finance - arXiv 2025
BIS : How regulators can address AI explainability - Bank for International Settlements 2024
XAI Review : Explainable AI (XAI) in finance: a systematic literature review - AI Review 2024
Approches suggérées

Implémenter un modèle de recommandation d'investissement (ML ou basé règles)
Intégrer des techniques XAI (SHAP, LIME, counterfactual explanations)
Développer un système d'argumentation pour structurer les justifications
Créer une interface présentant les recommandations avec explications
Technologies pertinentes

Python avec SHAP, LIME ou Captum pour l'explicabilité
TweetyProject ou frameworks d'argumentation pour la structuration
LLMs pour la génération d'explications en langage naturel
Streamlit/Dash pour l'interface de visualisation

## Installation

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le dépôt :
```bash
git clone <repository-url>
cd "PROJET 48"
```

2. Créer un environnement virtuel (recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env avec vos clés API si nécessaire
```

## Utilisation

### Lancer l'application Streamlit

```bash
streamlit run app/app.py
```

L'application sera accessible à l'adresse `http://localhost:8501`

### Utiliser les modules Python

```python
from src.data import DataLoader, DataPreprocessor
from src.models import HybridModel
from src.xai import SHAPExplainer, LIMEExplainer, CounterfactualExplainer
from src.argumentation import ArgumentBuilder, ExplanationGenerator

# Charger les données
loader = DataLoader()
data = loader.load_yahoo_data("AAPL", period="5y")

# Prétraiter
preprocessor = DataPreprocessor()
data = preprocessor.clean_data(data)
data = preprocessor.compute_technical_indicators(data)
data = preprocessor.create_target_variable(data)

# Entraîner le modèle
model = HybridModel()
X_train, y_train = preprocessor.get_feature_importance_data(train)
model.train(X_train, y_train)

# Faire des prédictions
prediction = model.predict(X_test)

# Expliquer avec SHAP
shap_explainer = SHAPExplainer(model.ml_model.model, X_train)
explanation = shap_explainer.explain_instance(X_test, index=0)
```

## Structure du projet

```
PROJET 48/
├── app/
│   └── app.py              # Application Streamlit principale
├── data/
│   ├── raw/                # Données brutes
│   ├── processed/           # Données traitées
│   └── cache/              # Cache des données
├── src/
│   ├── data/
│   │   ├── load_data.py     # Chargement des données
│   │   └── preprocess.py   # Prétraitement
│   ├── models/
│   │   ├── ml_model.py      # Modèle ML
│   │   ├── rule_based.py    # Modèle basé sur règles
│   │   └── hybrid_model.py  # Modèle hybride
│   ├── xai/
│   │   ├── shap_explainer.py      # Explications SHAP
│   │   ├── lime_explainer.py      # Explications LIME
│   │   └── counterfactual.py     # Scénarios contrefactuels
│   ├── argumentation/
│   │   ├── argument_builder.py      # Construction d'arguments
│   │   └── explanation_generator.py # Génération d'explications
│   └── utils/
│       └── config.py        # Configuration
├── tests/                  # Tests unitaires
├── notebooks/              # Jupyter notebooks pour l'exploration
├── requirements.txt         # Dépendances Python
├── setup.py               # Configuration du package
├── .env.example           # Exemple de variables d'environnement
└── README.md             # Ce fichier
```

## Technologies utilisées

| Composant | Technologie |
|-----------|-------------|
| Langage | Python |
| ML | XGBoost, scikit-learn |
| XAI | SHAP, LIME |
| Interface | Streamlit |
| Visualisation | Plotly, Matplotlib |
| Données | yfinance |

## Licence

Ce projet est sous licence MIT.

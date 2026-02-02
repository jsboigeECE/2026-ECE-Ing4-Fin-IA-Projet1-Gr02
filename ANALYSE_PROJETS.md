# Analyse des Projets - ECE Ing4 Finance IA - Groupe 02

**Date d'analyse:** 1er février 2026
**Évaluateur:** Système automatisé + revue manuelle

---

## Grille d'Évaluation

| Critère | Pondération | Description |
|---------|-------------|-------------|
| **Fonctionnalité** | 25% | Le code fonctionne-t-il ? Atteint-il les objectifs ? |
| **Qualité du code** | 20% | Structure, lisibilité, modularité, respect des bonnes pratiques |
| **Documentation** | 15% | README, commentaires, documentation technique |
| **Innovation/Complexité** | 20% | Algorithmes utilisés, approche technique, originalité |
| **Interface utilisateur** | 10% | UI/UX (si applicable), facilité d'utilisation |
| **Tests & Robustesse** | 10% | Gestion des erreurs, tests, cas limites |

---

## Récapitulatif des Notes

| Projet | Équipe | Sujet | Note /20 | Statut |
|--------|--------|-------|----------|--------|
| **64/** | Jules, Raphaël, Hugo, Cian | Robo-advisor Monte Carlo | **14.5** | Complet |
| **Gr02-Louis_Giraudeau_Gisclon-Sujet40/** | Arthur Louis, Manon Giraudeau, Noam Gisclon | MILP + CVaR Optimizer | **17.0** | Excellent |
| **groupe-02-systeme-expert-medical/** | El Bakkali Badr, El Yousoufi Zakaria, Id El Ouali Kawthar | Système Expert Médical | **16.0** | Très Bien |
| **groupe-JVX/** | Jean-François, Valentin, Xavier | Trading GA + WFA | **16.5** | Très Bien |
| **BDT/** | Delplace Bousso TBO | - | **2.0** | Non rendu |
| **hcjr/** | Jules, Hugo, Raphaël, Cian | - | **2.0** | Non rendu |
| **knowledgeGraph/** | Groupe 2 (Sujet 46) | Knowledge Graph Risques | **5.0** | README seul |

**Écart-type des notes (projets complets):** σ = 1.15

---

## Analyses Détaillées

---

### 1. Projet 64/ - Robo-Advisor Goal-Based (Monte Carlo)

**Équipe:** Jules (Interface), Raphaël (Modélisation), Hugo (Optimisation), Cian (Simulation)
**Sujet:** Robo-advisor orienté objectifs avec simulations Monte Carlo

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 14 | Monte Carlo fonctionne mais valeurs aberrantes détectées lors des tests (médiane astronomique). Optimiseur cvxpy fonctionnel. |
| Qualité du code | 15 | Bonne structure modulaire, imports propres, docstrings présentes |
| Documentation | 16 | README complet avec instructions d'installation et exemples |
| Innovation | 14 | Approche goal-based intéressante mais classique, Cholesky pour corrélations |
| Interface | 15 | Streamlit fonctionnel avec Plotly, UX correcte |
| Tests & Robustesse | 12 | Notebook avec erreur (fonction non définie), pas de tests unitaires |

**Note finale: 14.5/20**

#### Points forts
- Architecture modulaire bien pensée (data_fetcher, optimizer, monte_carlo)
- Interface Streamlit fonctionnelle avec visualisations
- Documentation claire avec exemples de résultats

#### Points faibles
- Bug dans le calcul Monte Carlo (valeurs exponentiellement trop grandes)
- Notebook de démo avec erreur d'import
- Pas de tests automatisés
- Dépendance cvxpy non standard (difficile à installer)

#### Questions de Présentation

**Niveau Facile:**
1. Expliquez ce qu'est une simulation Monte Carlo et pourquoi on l'utilise en finance.
   > *Réponse attendue : Une simulation Monte Carlo génère des milliers de scénarios aléatoires pour estimer la distribution des résultats possibles. En finance, elle permet de quantifier l'incertitude sur la valeur future d'un portefeuille.*

2. Qu'est-ce que le ratio de Sharpe et comment l'interprète-t-on ?
   > *Réponse attendue : Le ratio de Sharpe mesure le rendement excédentaire par unité de risque (écart-type). Un ratio > 1 est généralement considéré comme bon, > 2 très bon.*

3. Pourquoi utilise-t-on 252 jours dans vos calculs annualisés ?
   > *Réponse attendue : 252 correspond au nombre approximatif de jours de trading dans une année (hors week-ends et jours fériés).*

**Niveau Intermédiaire:**
4. Comment la décomposition de Cholesky permet-elle de générer des rendements corrélés ?
   > *Réponse attendue : La décomposition de Cholesky transforme la matrice de covariance en une matrice triangulaire L telle que Σ = LL^T. En multipliant un vecteur de variables aléatoires indépendantes par L, on obtient des variables avec les corrélations souhaitées.*

5. Expliquez la formule de l'optimisation quadratique que vous avez implémentée.
   > *Réponse attendue : On minimise w^T Σ w (variance) sous contrainte que w^T μ ≥ rendement_cible et Σw = 1, où w sont les poids, Σ la matrice de covariance et μ les rendements attendus.*

6. Pourquoi avoir choisi une approche "goal-based" plutôt qu'une optimisation Markowitz classique ?
   > *Réponse attendue : L'approche goal-based est plus intuitive pour les clients car elle définit des objectifs concrets (montant cible à une date donnée) plutôt qu'un compromis abstrait risque/rendement.*

**Niveau Difficile:**
7. Votre simulation Monte Carlo produit des valeurs aberrantes (médiane de plusieurs trillions). Pouvez-vous identifier le bug ?
   > *Réponse attendue : Le problème vient probablement de l'application du rendement journalier comme multiplicateur sans tenir compte que c'est un rendement logarithmique ou de l'oubli de diviser les rendements annuels par 252 avant simulation.*

8. Comment gérez-vous le rebalancing du portefeuille dans votre modèle ?
   > *Réponse attendue : L'étudiant doit expliquer s'il y a rebalancing périodique (ex: mensuel) ou si les poids dérivent naturellement. Dans le code actuel, les poids sont fixes sur toute la période.*

9. Quelles sont les limites de l'hypothèse de normalité des rendements que vous utilisez ?
   > *Réponse attendue : Les rendements réels présentent des "fat tails" (événements extrêmes plus fréquents que prévu), de l'asymétrie, et des clusters de volatilité que la loi normale ne capture pas.*

---

### 2. Projet Gr02-Louis_Giraudeau_Gisclon-Sujet40 - MILP + CVaR Portfolio Optimizer

**Équipe:** Arthur Louis, Manon Giraudeau, Noam Gisclon
**Sujet:** Optimisation de portefeuille sous contraintes pratiques (MILP & CSP)

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 18 | Parfaitement fonctionnel, testé avec succès sur données synthétiques |
| Qualité du code | 17 | Excellent usage de dataclasses, typing, modularité exemplaire |
| Documentation | 18 | README exceptionnel avec flux de décision, troubleshooting, concepts expliqués |
| Innovation | 17 | MILP avec CVaR, contraintes réalistes (cardinalité, turnover, secteurs) |
| Interface | 16 | Streamlit v2 professionnel + Desktop Tkinter + CLI |
| Tests & Robustesse | 15 | Bonne gestion d'erreurs, messages clairs, mais pas de pytest |

**Note finale: 17.0/20**

#### Points forts
- Formulation MILP complète avec toutes les contraintes professionnelles
- Triple interface (Web Streamlit, Desktop Tkinter, CLI)
- Documentation exceptionnelle avec diagrammes de flux
- Presets de tickers pour démonstration rapide
- Gestion CVaR (Conditional Value at Risk) avancée

#### Points faibles
- Pas de tests unitaires automatisés
- Shorting non implémenté (NotImplementedError)
- Interface desktop basique comparée à Streamlit

#### Questions de Présentation

**Niveau Facile:**
1. Qu'est-ce que le CVaR et en quoi diffère-t-il de la VaR classique ?
   > *Réponse attendue : La VaR indique la perte maximale avec une certaine probabilité (ex: 95%). Le CVaR (Expected Shortfall) calcule la perte moyenne dans les cas où on dépasse la VaR, capturant ainsi la sévérité des pertes extrêmes.*

2. Expliquez la contrainte de cardinalité et son utilité pratique.
   > *Réponse attendue : La contrainte de cardinalité limite le nombre d'actifs en portefeuille (ex: max 10 titres). Elle réduit les coûts de transaction et simplifie la gestion pour les petits portefeuilles.*

3. Pourquoi avoir trois interfaces différentes (Web, Desktop, CLI) ?
   > *Réponse attendue : Chaque interface répond à un cas d'usage : CLI pour l'automatisation/scripts, Desktop pour une utilisation hors-ligne, Web pour l'accessibilité et le partage.*

**Niveau Intermédiaire:**
4. Comment fonctionne la sélection binaire des actifs dans votre formulation MILP ?
   > *Réponse attendue : On introduit une variable binaire z_i ∈ {0,1} pour chaque actif. La contrainte w_i ≤ M·z_i force le poids à 0 si l'actif n'est pas sélectionné. La cardinalité devient Σz_i ≤ k.*

5. Expliquez le rôle du paramètre lambda (risk aversion) dans votre fonction objectif.
   > *Réponse attendue : Lambda pondère le compromis entre rendement et risque dans la fonction objectif : max(rendement - λ·risque). Un λ élevé privilégie la réduction du risque.*

6. Comment gérez-vous les coûts de transaction dans l'optimisation ?
   > *Réponse attendue : Les coûts de transaction sont ajoutés à la fonction objectif proportionnellement aux changements de poids |w_new - w_old|, ce qui pénalise le turnover excessif.*

**Niveau Difficile:**
7. Montrez mathématiquement comment vous linéarisez le calcul du CVaR pour le MILP.
   > *Réponse attendue : On utilise la formulation de Rockafellar-Uryasev : CVaR = VaR + (1/α)·E[max(perte - VaR, 0)]. On introduit des variables auxiliaires u_s ≥ perte_s - VaR et u_s ≥ 0 pour chaque scénario.*

8. Pourquoi utiliser OR-Tools plutôt que CVXPY pour ce problème ? Quels sont les avantages ?
   > *Réponse attendue : OR-Tools est optimisé pour les problèmes MILP avec variables binaires. CVXPY est plus adapté à l'optimisation convexe continue. OR-Tools offre aussi des solveurs puissants intégrés (SCIP, CBC).*

9. Comment évitez-vous l'overfitting aux données historiques dans votre optimisation ?
   > *Réponse attendue : On peut utiliser la validation croisée temporelle, des contraintes de régularisation sur les poids, ou des techniques de shrinkage sur la matrice de covariance.*

10. Comment pourriez-vous étendre votre modèle pour supporter le shorting ?
    > *Réponse attendue : Il faut autoriser w_i < 0, ajouter des contraintes de marge, et potentiellement séparer les variables en positions longues et courtes pour gérer les coûts d'emprunt.*

---

### 3. Projet groupe-02-systeme-expert-medical - Système Expert Médical

**Équipe:** El Bakkali Badr, El Yousoufi Zakaria, Id El Ouali Kawthar
**Sujet:** Système expert médical avec moteur d'inférence

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 17 | Chaînage avant/arrière fonctionnels, tests validés |
| Qualité du code | 16 | Bonne structure, dataclasses, typage Python |
| Documentation | 16 | README clair avec exemples de cas de test |
| Innovation | 15 | Approche classique système expert mais bien implémentée |
| Interface | 16 | Frontend HTML/JS moderne + API FastAPI |
| Tests & Robustesse | 15 | Gestion des symptômes inconnus, validation robuste |

**Note finale: 16.0/20**

#### Points forts
- Double mode d'inférence (chaînage avant ET arrière)
- Gestion de l'incertitude avec facteurs de confiance
- Interface web moderne et responsive
- API REST bien conçue avec FastAPI
- Base de connaissances extensible en JSON

#### Points faibles
- Base de connaissances limitée (10 règles, 14 diagnostics)
- Pas de machine learning ou d'apprentissage
- Pas de persistance des sessions utilisateur

#### Questions de Présentation

**Niveau Facile:**
1. Quelle est la différence entre chaînage avant et chaînage arrière ?
   > *Réponse attendue : Le chaînage avant part des faits connus pour déduire de nouvelles conclusions (data-driven). Le chaînage arrière part d'une hypothèse et cherche les faits qui la confirment (goal-driven).*

2. Comment fonctionne un facteur de confiance dans votre système ?
   > *Réponse attendue : Chaque règle et fait a un score de confiance [0,1]. Quand une règle s'applique, le score de la conclusion est combiné avec les scores des prémisses pour refléter l'incertitude cumulative.*

3. Pourquoi avoir choisi JSON pour la base de connaissances plutôt qu'une ontologie ?
   > *Réponse attendue : JSON est simple à lire/écrire, facilement éditable sans outil spécialisé, et suffit pour un système à règles plates. Une ontologie (OWL/RDF) serait utile pour des relations hiérarchiques complexes.*

**Niveau Intermédiaire:**
4. Expliquez la formule de combinaison des scores : `score = 1 - (1-score) * (1-score_ajoute)`. Pourquoi cette formule ?
   > *Réponse attendue : C'est une combinaison probabiliste "noisy-OR". Elle modélise l'idée que plusieurs indices indépendants augmentent la confiance sans jamais atteindre 1. Chaque nouvel indice réduit le "doute restant".*

5. Comment gérez-vous les symptômes optionnels (si_un) vs obligatoires (si_tous) ?
   > *Réponse attendue : "si_tous" exige que tous les symptômes soient présents (ET logique). "si_un" déclenche la règle si au moins un symptôme est présent (OU logique), avec un score proportionnel au nombre de matches.*

6. Quels sont les avantages et inconvénients d'utiliser FastAPI vs Flask ?
   > *Réponse attendue : FastAPI offre la validation automatique (Pydantic), la documentation OpenAPI générée, et le support async natif. Flask est plus simple mais nécessite plus de code manuel pour ces fonctionnalités.*

**Niveau Difficile:**
7. Comment pourriez-vous intégrer du machine learning pour améliorer les règles d'inférence ?
   > *Réponse attendue : On pourrait apprendre les poids/confiances des règles à partir de cas diagnostiqués, utiliser un classifieur pour suggérer de nouvelles règles, ou combiner le système expert avec un modèle probabiliste.*

8. Comment gérer les conflits quand plusieurs règles se contredisent ?
   > *Réponse attendue : Stratégies possibles : priorité par spécificité (règle plus précise gagne), par récence (dernière règle ajoutée), par confiance (score le plus élevé), ou demander à l'utilisateur de trancher.*

9. Comment évolueriez-vous vers une approche probabiliste type réseau bayésien ?
   > *Réponse attendue : Remplacer les règles par un graphe de dépendances probabilistes, définir les P(maladie|symptômes) via des tables de probabilités conditionnelles, et utiliser l'inférence bayésienne pour propager les croyances.*

10. Quelles sont les implications éthiques/légales d'un système expert médical ?
    > *Réponse attendue : Responsabilité en cas d'erreur de diagnostic, nécessité de validation clinique, respect du RGPD pour les données de santé, obligation de transparence sur les limites du système, et supervision par un professionnel de santé.*

---

### 4. Projet groupe-JVX - Trading par Algorithmes Génétiques

**Équipe:** Jean-François, Valentin, Xavier
**Sujet:** Stratégies de trading optimisées par algorithmes génétiques

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 16 | Architecture complète, dépendance backtrader manquante pour test |
| Qualité du code | 17 | Excellent : docstrings, typing, modularité, commentaires détaillés |
| Documentation | 17 | README professionnel avec diagrammes Mermaid, références académiques |
| Innovation | 18 | NSGA-II multi-objectif + Walk-Forward Analysis = approche robuste |
| Interface | 16 | Dashboard Streamlit avec CSS personnalisé "cyberpunk" |
| Tests & Robustesse | 14 | Bonne gestion d'erreurs mais dépendances pas vérifiées |

**Note finale: 16.5/20**

#### Points forts
- Utilisation avancée de DEAP avec NSGA-II (multi-objectif)
- Walk-Forward Analysis pour validation réaliste
- Stratégie de trading complète avec SMA, RSI, Stop-Loss, Take-Profit
- Dashboard avec design professionnel personnalisé
- Références académiques (MDPI 2024)

#### Points faibles
- Dépendance backtrader nécessaire (pas toujours facile à installer)
- Temps d'exécution potentiellement long pour l'optimisation
- Pas de backtesting multi-actifs

#### Questions de Présentation

**Niveau Facile:**
1. Qu'est-ce qu'un algorithme génétique et quels sont ses opérateurs principaux ?
   > *Réponse attendue : Un AG simule l'évolution naturelle pour optimiser. Opérateurs : sélection (choisir les meilleurs), croisement (combiner deux parents), mutation (variations aléatoires).*

2. Expliquez ce qu'est le RSI (Relative Strength Index) et comment vous l'utilisez.
   > *Réponse attendue : Le RSI mesure la vitesse et l'amplitude des mouvements de prix sur une échelle 0-100. RSI < 30 = survente (signal d'achat), RSI > 70 = surachat (signal de vente).*

3. Qu'est-ce que le drawdown maximum et pourquoi est-il important ?
   > *Réponse attendue : Le drawdown max est la plus grande perte depuis un pic de valeur du portefeuille. Il mesure le risque de perte extrême et la capacité psychologique à supporter des pertes temporaires.*

**Niveau Intermédiaire:**
4. Pourquoi utiliser NSGA-II plutôt qu'un algorithme génétique simple ?
   > *Réponse attendue : NSGA-II optimise plusieurs objectifs simultanément (rendement ET risque) sans les agréger artificiellement. Il génère un front de Pareto de solutions non-dominées parmi lesquelles choisir.*

5. Expliquez le concept de Walk-Forward Analysis et son importance contre l'overfitting.
   > *Réponse attendue : La WFA divise les données en périodes successives : optimisation sur une fenêtre, test sur la suivante, puis glissement. Cela simule les conditions réelles où on optimise sur le passé pour trader le futur.*

6. Comment fonctionne un ordre "bracket" dans Backtrader ?
   > *Réponse attendue : Un bracket order combine trois ordres liés : l'ordre principal (entrée), un stop-loss (sortie si perte), et un take-profit (sortie si gain). Quand l'un des deux ordres de sortie s'exécute, l'autre est annulé.*

**Niveau Difficile:**
7. Comment évitez-vous le curve-fitting (surapprentissage) sur les données historiques ?
   > *Réponse attendue : Walk-Forward Analysis, validation out-of-sample, pénalisation de la complexité (peu de paramètres), tests de robustesse sur différentes périodes/actifs, et méfiance envers les performances trop parfaites.*

8. Expliquez la fonction de fitness multi-objectifs et comment NSGA-II gère le front de Pareto.
   > *Réponse attendue : Chaque solution a plusieurs scores (rendement, Sharpe, drawdown). NSGA-II trie par dominance (A domine B si meilleur sur tous les objectifs) et crowding distance pour maintenir la diversité sur le front.*

9. Comment pourriez-vous améliorer la stratégie en ajoutant d'autres indicateurs génétiques ?
   > *Réponse attendue : Ajouter MACD, Bollinger Bands, ou indicateurs de volume au génome. L'AG sélectionnerait automatiquement les indicateurs et paramètres les plus pertinents.*

10. Quelles sont les limites de l'optimisation génétique pour le trading algorithmique ?
    > *Réponse attendue : Risque d'overfitting malgré les précautions, hypothèse que le passé prédit le futur, coûts de transaction non nuls, slippage, et changements de régime de marché non anticipés.*

---

### 5. Projet BDT/ - Non Rendu

**Équipe:** Delplace Bousso TBO
**Sujet:** Non défini

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 0 | Aucun code |
| Qualité du code | 0 | N/A |
| Documentation | 4 | Uniquement un README avec les noms |
| Innovation | 0 | N/A |
| Interface | 0 | N/A |
| Tests & Robustesse | 0 | N/A |

**Note finale: 2.0/20** (présence du dossier et du README)

#### Questions de Présentation
1. Quel était votre sujet prévu ?
2. Pourquoi le projet n'a-t-il pas été rendu ?
3. Avez-vous rencontré des difficultés particulières ?

---

### 6. Projet hcjr/ - Non Rendu

**Équipe:** Jules, Hugo, Raphaël, Cian (même équipe que 64/)
**Sujet:** "On sait pas encore" (citation du README)

#### Évaluation

**Note finale: 2.0/20** (présence du dossier uniquement)

**Remarque:** Il semble que cette équipe ait également contribué au projet 64/. Ce dossier pourrait être un brouillon abandonné.

#### Questions de Présentation
1. Ce dossier était-il prévu comme un deuxième projet ?
2. Comment avez-vous réparti le travail entre ce dossier et 64/ ?

---

### 7. Projet knowledgeGraph/ - README Seul

**Équipe:** Groupe 2 - Sujet 46
**Sujet:** Graphe de connaissances pour la gestion des risques financiers

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 0 | Aucun code implémenté |
| Qualité du code | 0 | N/A |
| Documentation | 15 | README très détaillé avec architecture, références, stack technique |
| Innovation | 8 | Concept intéressant (GNN + Knowledge Graph) mais non implémenté |
| Interface | 0 | N/A |
| Tests & Robustesse | 0 | N/A |

**Note finale: 5.0/20** (README de qualité mais aucun code)

#### Points positifs du README
- Architecture bien pensée (Neo4j, PyKEEN, spaCy)
- Références académiques pertinentes (FEEKG, FinReflectKG)
- Structure de projet claire

#### Questions de Présentation

**Niveau Facile:**
1. Qu'est-ce qu'un graphe de connaissances et comment diffère-t-il d'une base de données relationnelle ?
   > *Réponse attendue : Un KG stocke des triplets (entité-relation-entité) et permet des requêtes sur les chemins/relations. Une BDD relationnelle utilise des tables avec schéma fixe. Le KG est plus flexible pour les données interconnectées.*

2. Quelles sont les entités et relations que vous aviez prévues ?
   > *Réponse attendue : Entités : entreprises, secteurs, indicateurs financiers, événements. Relations : "appartient_au_secteur", "dépend_de", "impacte", "corrélé_avec".*

**Niveau Intermédiaire:**
3. Comment un GNN (Graph Neural Network) pourrait-il aider à prédire la propagation des risques ?
   > *Réponse attendue : Un GNN apprend des représentations vectorielles des nœuds en agrégeant l'information des voisins. Il peut ainsi capturer comment un choc sur une entreprise se propage via ses connexions (fournisseurs, secteur, etc.).*

4. Expliquez le concept de "link prediction" dans un knowledge graph.
   > *Réponse attendue : La link prediction prédit les relations manquantes entre entités. Ex: si A fournit B et B fournit C, le modèle peut inférer une relation indirecte A→C ou prédire de nouvelles dépendances.*

**Niveau Difficile:**
5. Pourquoi le projet n'a-t-il pas été implémenté malgré un README aussi détaillé ?
   > *Réponse attendue : L'étudiant doit expliquer honnêtement les difficultés rencontrées (temps, complexité technique, problèmes d'équipe, etc.).*

6. Comment auriez-vous géré l'extraction automatique des entités depuis des textes financiers ?
   > *Réponse attendue : Utilisation de NER (Named Entity Recognition) avec spaCy ou modèles fine-tunés sur le domaine financier (FinBERT), puis résolution d'entités pour lier les mentions aux nœuds du graphe.*

---

## Recommandations Générales

### Pour les projets excellents (Note >= 16)
- Ajouter des tests unitaires avec pytest
- Dockeriser les applications pour faciliter le déploiement
- Envisager l'ajout de CI/CD (GitHub Actions)

### Pour les projets moyens (Note 12-16)
- Corriger les bugs identifiés (notamment le Monte Carlo du projet 64/)
- Améliorer la gestion des dépendances (requirements.txt complet)
- Ajouter des tests automatisés

### Pour les projets non rendus
- Discussion sur les difficultés rencontrées
- Possibilité de session de rattrapage ?

---

## Annexe : Tests d'Exécution Réalisés

```
# Test 1: Système Expert Médical - OK
Base chargée: 31 symptômes, 10 règles
Test grippe: [('grippe', 0.432), ('covid', 0.27)]
Test migraine: [('migraine', 0.432)]
Test cystite: [('cystite', 0.39)]

# Test 2: MILP Optimizer (Gr02-Louis) - OK
Status: OPTIMAL
Weights: {'AAPL': '25.01%', 'MSFT': '33.34%', 'GOOGL': '41.65%'}

# Test 3: Monte Carlo (64/) - BUG DETECTÉ
Monte Carlo - médiane: 2,598,437,351,702 (valeur aberrante!)
Cause probable: erreur dans le calcul des multiplicateurs journaliers

# Test 4: JVX GA - Non testé (backtrader non installé)
```

---

*Document généré automatiquement - À compléter avec observations lors des présentations*

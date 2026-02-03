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
| **groupe-11-resolution-demineur/** | Sébastien Fermigier, Brieuc Molko, Kimi Ho | Démineur CSP Solver | **15.5** | Bien |
| **groupe-02-wordle-csp-solver/** | Équipe Wordle | Wordle CSP + LLM | **16.5** | Très Bien |
| **groupe2-lamy-coloration-graphe/** | Robin Lamy | Coloration de graphe CSP | **15.0** | Bien |
| **groupe-02-Farina_Lamonerie_calendrier-sportif/** | Léo Farina, Arthur Lamonerie | Calendrier sportif CP-SAT | **16.0** | Très Bien |
| **BDT/** | Delplace Bousso TBO | - | **2.0** | Non rendu |
| **hcjr/** | Jules, Hugo, Raphaël, Cian | - | **2.0** | Non rendu |
| **knowledgeGraph/** | Groupe 2 (Sujet 46) | Knowledge Graph Risques | **5.0** | README seul |
| **PROJET 48/** | Léo Lans, Wandrille Esnault, Martin Jezequel | IA explicable investissement | **5.0** | README seul |

**Écart-type des notes (projets complets):** σ = 0.98

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

### 8. Projet groupe-11-resolution-demineur - Solveur CSP Démineur

**Équipe:** Sébastien Fermigier, Brieuc Molko, Kimi Ho
**Sujet:** Résolution automatique du puzzle Démineur par programmation par contraintes

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 16 | Solveur CSP fonctionnel avec python-constraint |
| Qualité du code | 15 | Code lisible, structure correcte |
| Documentation | 15 | README avec références académiques et instructions |
| Innovation | 15 | Application classique mais bien exécutée du CSP |
| Interface | 15 | Interface graphique Tkinter pour visualisation |
| Tests & Robustesse | 14 | Gestion des cas ambigus, pas de tests automatisés |

**Note finale: 15.5/20**

#### Points forts
- Modélisation CSP correcte du problème (variable booléenne par case)
- Références académiques pertinentes (Bayer & Snyder 2013)
- Propagation de contraintes pour réduire l'espace de recherche
- Interface graphique pour visualiser la résolution

#### Points faibles
- Documentation technique limitée sur l'implémentation
- Pas de tests unitaires automatisés
- Interface graphique basique

#### Questions de Présentation

**Niveau Facile:**
1. Comment modélisez-vous le problème du Démineur comme un CSP ?
   > *Réponse attendue : Chaque case inconnue est une variable booléenne (mine ou pas mine). Pour chaque case révélée avec un chiffre n, on ajoute une contrainte : la somme des variables des 8 cases voisines doit égaler n.*

2. Qu'est-ce que la propagation de contraintes et pourquoi est-elle utile ici ?
   > *Réponse attendue : La propagation réduit les domaines des variables en utilisant les contraintes. Par exemple, si une case affiche 0, toutes ses voisines sont forcément sans mine. Cela réduit drastiquement l'espace de recherche.*

3. Pourquoi le Démineur est-il considéré comme NP-complet ?
   > *Réponse attendue : Dans le cas général, déterminer si une configuration de Démineur a une solution unique nécessite d'explorer exponentiellement de possibilités. C'est équivalent à SAT dans certaines réductions.*

**Niveau Intermédiaire:**
4. Comment gérez-vous les situations ambiguës où plusieurs configurations sont possibles ?
   > *Réponse attendue : Quand la propagation seule ne suffit pas, on doit faire du backtracking : essayer une hypothèse, propager, et revenir en arrière si contradiction. Dans certains cas, le joueur doit deviner.*

5. Quelle est la différence entre arc-consistency et la résolution complète ?
   > *Réponse attendue : L'arc-consistency garantit que chaque valeur du domaine d'une variable est compatible avec au moins une valeur de chaque variable liée. Cela ne garantit pas de solution, contrairement à une résolution complète par backtracking.*

6. Comment optimiseriez-vous votre solveur pour des grilles très grandes ?
   > *Réponse attendue : Utiliser CP-SAT d'OR-Tools au lieu de python-constraint, exploiter le parallélisme, ou décomposer le problème en sous-problèmes indépendants quand les zones sont disjointes.*

**Niveau Difficile:**
7. Démontrez que votre contrainte de somme sur le voisinage est correcte mathématiquement.
   > *Réponse attendue : Si case[i,j] = n, alors Σ(mine[x,y] pour (x,y) ∈ voisins(i,j)) = n. C'est une contrainte de somme exacte sur des variables binaires.*

8. Comment adapteriez-vous votre approche pour résoudre le Démineur en mode "probabiliste" ?
   > *Réponse attendue : Calculer P(mine) pour chaque case en comptant les solutions où elle est mine / solutions totales. Cela permet de choisir la case la moins risquée quand on doit deviner.*

9. Quels sont les cas pathologiques où votre solveur pourrait être lent ?
   > *Réponse attendue : Grilles avec beaucoup de cases inconnues et peu de contraintes, configurations ambiguës nécessitant beaucoup de backtracking, ou grilles de très grande taille (100x100+).*

---

### 9. Projet groupe-02-wordle-csp-solver - Wordle CSP avec LLM

**Équipe:** Projet ECE Paris - IA
**Sujet:** Solveur intelligent de Wordle par CSP avec intégration LLM

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 17 | Solveur CSP complet, multi-stratégies, tests inclus |
| Qualité du code | 17 | Excellente modularité, typage, docstrings |
| Documentation | 18 | README exceptionnel avec exemples, algorithmes, références |
| Innovation | 17 | Intégration LLM avec function calling, théorie de l'information |
| Interface | 16 | CLI colorée intuitive, multi-modes |
| Tests & Robustesse | 15 | Tests unitaires présents, bonne couverture |

**Note finale: 16.5/20**

#### Points forts
- Multiple stratégies d'optimisation (entropie, minimax, fréquence)
- Intégration LLM avec OpenAI function calling
- Support multi-langues (anglais, français)
- Tests unitaires inclus
- Documentation exceptionnelle avec analyse de complexité

#### Points faibles
- Dépendance API OpenAI (coût, disponibilité)
- Performance sur grands dictionnaires à optimiser
- Pas d'interface graphique web

#### Questions de Présentation

**Niveau Facile:**
1. Comment représentez-vous les contraintes Wordle dans votre CSP ?
   > *Réponse attendue : Trois types de contraintes : VERT = lettre fixée à cette position, JAUNE = lettre présente mais pas à cette position, GRIS = lettre absente du mot (sauf si déjà vue ailleurs).*

2. Qu'est-ce que l'entropie et pourquoi l'utilisez-vous pour choisir le meilleur mot ?
   > *Réponse attendue : L'entropie mesure l'incertitude. On choisit le mot qui maximise le gain d'information attendu, c'est-à-dire qui réduit le plus le nombre de candidats possibles en moyenne.*

3. Expliquez la différence entre le mode assistant et le mode automatique.
   > *Réponse attendue : En mode assistant, le solveur suggère des mots et l'utilisateur joue. En mode automatique, le solveur résout seul après qu'on lui donne le mot secret.*

**Niveau Intermédiaire:**
4. Comment fonctionne l'intégration LLM avec function calling ?
   > *Réponse attendue : Le LLM peut appeler des fonctions exposées (apply_constraints, get_possible_words, suggest_best_guess). Il analyse la demande de l'utilisateur, appelle la fonction appropriée, et utilise le résultat pour répondre.*

5. Expliquez la stratégie minimax et quand l'utiliser plutôt que l'entropie.
   > *Réponse attendue : Minimax minimise le pire cas : on choisit le mot qui laisse le moins de candidats dans le scénario le plus défavorable. Utile quand on veut garantir une résolution en N coups maximum.*

6. Comment gérez-vous les lettres répétées (ex: "LLAMA") ?
   > *Réponse attendue : Si une lettre apparaît deux fois et le feedback diffère (un VERT, un GRIS), on sait qu'il y a exactement une occurrence. Il faut compter les occurrences et ajuster les contraintes en conséquence.*

**Niveau Difficile:**
7. Démontrez la formule de calcul d'entropie et comment vous l'appliquez.
   > *Réponse attendue : H = -Σ p(i) log₂(p(i)) où p(i) est la probabilité du pattern i. Pour chaque mot candidat, on calcule les 3^5 patterns possibles et leur distribution sur les mots restants.*

8. Quelle est la complexité temporelle de votre algorithme d'optimisation ?
   > *Réponse attendue : O(n² × m) où n = taille dictionnaire, m = longueur mot. Pour chaque candidat (n), on calcule le pattern contre tous les autres (n), et comparer coûte O(m).*

9. Comment améliorer les performances pour un dictionnaire de 100 000 mots ?
   > *Réponse attendue : Échantillonnage aléatoire des candidats pour l'évaluation, pré-calcul des patterns, mise en cache, parallélisation, ou heuristiques pour élaguer l'espace de recherche.*

---

### 10. Projet groupe2-lamy-coloration-graphe - Coloration de Graphe CSP

**Équipe:** Robin Lamy
**Sujet:** Coloration de graphe et de carte comme CSP

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 16 | K-coloration, minimisation, validation fonctionnelles |
| Qualité du code | 15 | Structure modulaire, CLI complète |
| Documentation | 15 | README avec instructions, datasets inclus |
| Innovation | 14 | Application classique du CSP, bien exécutée |
| Interface | 14 | Visualisation NetworkX/Matplotlib |
| Tests & Robustesse | 15 | Tests pytest, validation des résultats |

**Note finale: 15.0/20**

#### Points forts
- Implémentation correcte avec OR-Tools CP-SAT
- Plusieurs générateurs d'instances (cycle, grille, Erdos-Rényi)
- Datasets réels (états US, départements France)
- Visualisation graphique des colorations
- Tests unitaires avec pytest

#### Points faibles
- Projet individuel (moins de complexité attendue)
- Pas d'interface web
- Optimisations avancées non explorées

#### Questions de Présentation

**Niveau Facile:**
1. Qu'est-ce que le problème de coloration de graphe ?
   > *Réponse attendue : Attribuer une couleur à chaque nœud du graphe de sorte que deux nœuds adjacents (reliés par une arête) n'aient jamais la même couleur, en utilisant le minimum de couleurs.*

2. Pourquoi 4 couleurs suffisent-elles pour colorier une carte ?
   > *Réponse attendue : C'est le théorème des 4 couleurs : tout graphe planaire (représentable sans croisement d'arêtes) est 4-coloriable. Les cartes géographiques sont des graphes planaires.*

3. Comment fonctionne votre algorithme de minimisation ?
   > *Réponse attendue : On teste K=1, puis K=2, etc. jusqu'à trouver le premier K pour lequel une solution existe. C'est une recherche linéaire sur le nombre chromatique.*

**Niveau Intermédiaire:**
4. Expliquez comment vous modélisez le problème en CSP avec OR-Tools.
   > *Réponse attendue : Variables = couleur de chaque nœud (domaine 0..K-1). Contraintes = pour chaque arête (u,v), couleur[u] ≠ couleur[v]. On demande au solveur de trouver une affectation satisfaisante.*

5. Quelle est la différence entre CP-SAT et un solveur SAT classique pour ce problème ?
   > *Réponse attendue : CP-SAT travaille directement avec des variables entières et des contraintes de haut niveau (≠, somme). Un solveur SAT nécessite d'encoder en clauses booléennes, ce qui est plus verbeux.*

6. Comment vérifiez-vous qu'une coloration est valide ?
   > *Réponse attendue : On parcourt toutes les arêtes du graphe et on vérifie que les deux extrémités ont des couleurs différentes. Complexité O(|E|).*

**Niveau Difficile:**
7. Pourquoi le problème de K-coloration est-il NP-complet pour K≥3 ?
   > *Réponse attendue : On peut réduire 3-SAT à 3-coloration en temps polynomial. Le problème de décision "existe-t-il une 3-coloration ?" est donc au moins aussi dur que SAT.*

8. Comment optimiseriez-vous pour des graphes de millions de nœuds ?
   > *Réponse attendue : Heuristiques gloutonnes (Welsh-Powell), métaheuristiques (recuit simulé), décomposition du graphe, ou algorithmes approchés. CP-SAT exact devient trop lent.*

9. Expliquez le lien entre coloration de graphe et allocation de registres en compilation.
   > *Réponse attendue : Les variables du programme forment un graphe d'interférence (arête si deux variables sont vivantes simultanément). Colorier ce graphe = attribuer des registres. K = nombre de registres disponibles.*

---

### 11. Projet groupe-02-Farina_Lamonerie_calendrier-sportif - Calendrier Sportif CP-SAT

**Équipe:** Léo Farina, Arthur Lamonerie
**Sujet:** Génération de calendrier de championnat par programmation par contraintes

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 17 | CP-SAT + MiniZinc fonctionnels, optimisation multi-critères |
| Qualité du code | 16 | Bonne structure, séparation génération/affinement |
| Documentation | 16 | README clair avec contraintes expliquées |
| Innovation | 16 | Combinaison CP-SAT + MiniZinc originale |
| Interface | 16 | Streamlit avec comparaison avant/après |
| Tests & Robustesse | 15 | Validation des contraintes, métriques calculées |

**Note finale: 16.0/20**

#### Points forts
- Double approche CP-SAT (génération) + MiniZinc (affinement)
- Contraintes sportives réalistes (breaks, équité, distances)
- Interface Streamlit avec comparaison visuelle
- Optimisation multi-critères (breaks, distance totale)

#### Points faibles
- Dépendance MiniZinc externe à installer
- Scalabilité non testée sur grands championnats
- Pas de tests automatisés

#### Questions de Présentation

**Niveau Facile:**
1. Qu'est-ce qu'un "break" dans un calendrier sportif et pourquoi le minimiser ?
   > *Réponse attendue : Un break est deux matchs consécutifs à domicile ou à l'extérieur pour une équipe. Les breaks créent de l'inéquité et de la fatigue, il faut les minimiser.*

2. Expliquez le format round-robin que vous implémentez.
   > *Réponse attendue : Chaque équipe rencontre toutes les autres exactement une fois (aller simple) ou deux fois (aller-retour). On cherche à répartir équitablement les matchs sur les journées.*

3. Pourquoi utiliser deux outils (CP-SAT et MiniZinc) ?
   > *Réponse attendue : CP-SAT génère rapidement un calendrier de base satisfaisant les contraintes dures. MiniZinc affine ensuite pour optimiser les critères secondaires (breaks, distances).*

**Niveau Intermédiaire:**
4. Comment modélisez-vous les contraintes d'indisponibilité de stade ?
   > *Réponse attendue : Variable booléenne match[équipe, journée, domicile]. Si le stade est indisponible journée J, on ajoute la contrainte match[équipe, J, domicile=True] = False.*

5. Expliquez l'équilibre domicile/extérieur et comment vous le garantissez.
   > *Réponse attendue : Chaque équipe doit avoir environ 50% de matchs à domicile. On compte les matchs domicile et on contraint ce compte à être dans [n/2 - 1, n/2 + 1].*

6. Comment calculez-vous la distance totale parcourue par une équipe ?
   > *Réponse attendue : On somme les distances entre lieux de matchs consécutifs. Si match J à Paris, match J+1 à Lyon, on ajoute distance(Paris, Lyon) au total.*

**Niveau Difficile:**
7. Montrez comment vous modélisez la contrainte "max N matchs consécutifs à l'extérieur".
   > *Réponse attendue : Pour chaque fenêtre de N+1 journées consécutives, au moins un match doit être à domicile. Formellement : Σ(domicile[j] pour j ∈ [i, i+N]) ≥ 1 pour tout i.*

8. Quelle est la complexité du problème de scheduling sportif ?
   > *Réponse attendue : NP-difficile en général. Trouver un calendrier satisfaisant toutes les contraintes est équivalent à des problèmes d'ordonnancement sous contraintes multiples.*

9. Comment adapteriez-vous votre modèle pour un championnat avec phases éliminatoires ?
   > *Réponse attendue : Ajouter des contraintes de dépendance : le match M ne peut avoir lieu qu'après le match M' si M' détermine les participants de M. Modéliser les arbres de tournoi.*

---

### 12. Projet PROJET 48/ - IA Explicable pour Investissement (README Seul)

**Équipe:** Léo Lans, Wandrille Esnault, Martin Jezequel
**Sujet:** IA explicable (XAI) pour justifier les décisions d'investissement

#### Évaluation

| Critère | Note /20 | Commentaires |
|---------|----------|--------------|
| Fonctionnalité | 0 | Aucun code implémenté |
| Qualité du code | 0 | N/A |
| Documentation | 15 | README avec description du problème et références |
| Innovation | 8 | Concept XAI pertinent mais non implémenté |
| Interface | 0 | N/A |
| Tests & Robustesse | 0 | N/A |

**Note finale: 5.0/20** (README seul, aucune implémentation)

#### Points positifs du README
- Références académiques récentes (CFA Institute 2025, BIS 2024)
- Technologies identifiées (SHAP, LIME, Captum)
- Problématique pertinente (exigences réglementaires)

#### Points faibles
- Aucun code fourni
- README peu structuré (pas de sections claires)
- Pas de slides ou présentation

#### Questions de Présentation

**Niveau Facile:**
1. Qu'est-ce que l'IA explicable (XAI) et pourquoi est-elle importante en finance ?
   > *Réponse attendue : XAI rend les décisions des modèles ML compréhensibles par les humains. En finance, elle est cruciale pour la conformité réglementaire (MiFID II, RGPD) et la confiance des clients.*

2. Expliquez la différence entre SHAP et LIME.
   > *Réponse attendue : SHAP (SHapley Additive exPlanations) utilise la théorie des jeux pour attribuer une contribution à chaque feature. LIME (Local Interpretable Model-agnostic Explanations) crée un modèle linéaire local autour d'une prédiction.*

**Niveau Intermédiaire:**
3. Comment SHAP calcule-t-il l'importance des features ?
   > *Réponse attendue : SHAP utilise les valeurs de Shapley qui mesurent la contribution marginale moyenne de chaque feature sur toutes les coalitions possibles de features.*

4. Qu'est-ce qu'une "counterfactual explanation" et donnez un exemple en finance ?
   > *Réponse attendue : Une explication contrefactuelle indique le minimum de changements nécessaires pour obtenir une décision différente. Ex: "Votre crédit aurait été approuvé si votre revenu était 10% plus élevé."*

**Niveau Difficile:**
5. Pourquoi le projet n'a-t-il pas été implémenté ?
   > *Réponse attendue : L'étudiant doit expliquer honnêtement les difficultés (temps, complexité technique, coordination d'équipe).*

6. Comment intégreriez-vous l'argumentation computationnelle avec SHAP pour structurer les explications ?
   > *Réponse attendue : Utiliser SHAP pour identifier les features importantes, puis construire des arguments formels (prémisses → conclusion) basés sur ces features. Ex: "Parce que volatilité > seuil ET momentum < 0, je recommande de vendre."*

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

# Test 4: JVX GA - OK (Python 3.13)
backtrader et deap installés et fonctionnels

# Test 5: Coloration Graphe - OK
Instance: cycle | nodes=5 edges=5 | K=3 | Valid coloring

# Test 6: Wordle CSP - OK
Imports et solveur fonctionnels

# Test 7: Calendrier Sportif - OK
6 équipes, 5 journées, 16 breaks, validation OK

# Test 8: Démineur CSP - OK
python-constraint, pygame, ortools, z3-solver fonctionnels
```

---

*Document généré automatiquement - Mis à jour le 3 février 2026*

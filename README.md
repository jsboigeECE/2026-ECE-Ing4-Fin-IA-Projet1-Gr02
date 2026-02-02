# Robo-Advisor — Goal-based Portfolio Optimization (Prototype)

Minimal prototype for a goal-based robo-advisor: data ingestion, Monte Carlo simulation,
convex optimization for multi-objective allocation, business-rule CSPs and a Streamlit UI.

Quick start

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Run the UI:

```bash
streamlit run ui/app.py
```

Files
- `data/` — data loaders
- `sim/` — Monte Carlo simulator
- `opt/` — optimization and CSP rules
- `ui/` — Streamlit prototype
- `docs/` — modelling assumptions and experiments
# 2026 - ECE - Ing4 - Fin - IA Exploratoire et Symbolique - Groupe 2

Projet pédagogique d'exploration des approches d'intelligence artificielle symbolique et exploratoire pour les étudiants de l'ECE.

---

## 📅 Modalités du projet

### Échéances importantes
- **20 janvier** :  Présentation des sujets proposés
- **02 février** : Présentation finale et rendu

### Taille des groupes
La taille standard d'un groupe est de 3 personnes, avec +1 pour les groupes de 2 et -1 pour les groupes de 4

### Évaluation
- Présentation/communication
- Contenu théorique, contexte et perspectives
- Contenu technique, performances, qualité du code et du logiciel
- Organisation/Collaboration (notamment activité git)

### Livrables attendus
- Code source documenté
- README de présentation avec infos essentielles, procédure d'installation et tests
- Slides de la présentation

### 📋 Instructions de soumission

#### ⚠️ IMPORTANT : Organisation du travail

> **ATTENTION** : Tout votre travail **DOIT** être organisé dans un **sous-répertoire dédié** à votre groupe.
>
> **Structure obligatoire** :
> ```
> /groupe-XX-nom-sujet/
> ├── README.md          # Documentation de votre projet
> ├── src/               # Code source
> ├── docs/              # Documentation technique
> ├── slides/            # Support de présentation (PDF ou lien)
> └── ...
> ```
>
> ❌ **Ne pas** mettre vos fichiers à la racine du dépôt
> ✅ **Tout** doit être dans votre sous-répertoire de groupe

#### Soumission du code et de la documentation
1. **Créer un fork** de ce dépôt sur votre compte GitHub (vous n'avez pas les droits d'écriture sur ce dépôt)
2. **Créer un sous-répertoire** pour votre groupe : `groupe-XX-nom-sujet/` (ex: `groupe-03-portfolio-csp/`)
3. **Développer votre projet** exclusivement dans ce sous-répertoire
4. **Soumettre une Pull Request** vers ce dépôt **au moins 2 jours avant la présentation** (soit le **31 janvier 2026** au plus tard)
5. La PR doit inclure :
   - Le code source complet et fonctionnel dans votre sous-répertoire
   - Un README détaillé dans votre sous-répertoire (installation, utilisation, tests)
   - La documentation technique

#### Soumission du support de présentation
- Les slides de présentation doivent être soumises **avant le début de la présentation** (soit le **02 février 2026** au matin)
- Format accepté : PDF, PowerPoint, ou lien vers Google Slides/Canva
- Ajouter les slides dans votre sous-répertoire (`groupe-XX/slides/`) ou partager le lien dans le README de votre sous-répertoire

#### Checklist de soumission
- [ ] Fork du dépôt créé
- [ ] Sous-répertoire `groupe-XX-nom-sujet/` créé avec tout le contenu dedans
- [ ] README avec procédure d'installation et tests dans le sous-répertoire
- [ ] Pull Request créée et reviewable
- [ ] Slides de présentation soumises (dans le sous-répertoire ou lien dans README)
- [ ] Tous les membres du groupe identifiés dans la PR (noms + GitHub usernames)

---

## 🎯 Sujets détaillés pour le projet

### 9. Solveur de Wordle par CSP (et LLM)

**Description du problème et contexte**
Wordle est un jeu de mots dans lequel à chaque tentative de mot, on obtient des indications de lettres bien placées, mal placées ou absentes. Ces indices se traduisent par des contraintes sur le mot secret : certaines positions doivent contenir certaines lettres, d'autres non, etc. Un programme peut appliquer ces contraintes à un dictionnaire pour filtrer les mots possibles. Par exemple, une approche par contraintes définit des variables pour chaque lettre du mot secret et impose les retours (vert, jaune, gris) comme contraintes logiques sur ces variables.

**Références multiples**
- **Approche CSP** : [Beating Wordle: Constraint Programming](https://medium.com/better-programming/beating-wordle-constraint-programming-ef0b0b6897fe) - Utilisation d'un solver de contraintes sur un dataset de mots
- **Implémentation** : hakank.org - Implémentation d'un solveur Wordle en OR-Tools CP-SAT
- **Function calling** : [OpenAI Function calling documentation](https://platform.openai.com/docs/guides/function-calling) - Appel de fonctions pour déléguer des tâches (ex. solveur externe)
- **Intégration LLM** : On peut intégrer un LLM en function-calling pour qu'il exploite un solveur CSP sous-jacent et propose des coups optimisés

**Approches suggérées**
- Définir des variables pour chaque lettre du mot secret et imposer les contraintes de retour (vert/jaune/gris)
- Utiliser un solveur de contraintes pour réduire l'espace des solutions à chaque coup
- Intégrer un LLM via function calling pour déduire les contraintes linguistiques
- Développer une stratégie d'optimisation pour minimiser le nombre de tentatives

**Technologies pertinentes**
- Python avec python-constraint ou OR-Tools CP-SAT pour la résolution
- Dictionnaires de mots français/anglais pour les domaines de variables
- API OpenAI ou modèles locaux pour l'intégration LLM
- Interface web avec React/Vue pour une expérience interactive

---

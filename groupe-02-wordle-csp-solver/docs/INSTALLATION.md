# 📦 Guide d'Installation et Lancement

## Installation

### Prérequis

- **Python** : 3.8 ou supérieur
- **pip** : Gestionnaire de paquets Python
- **Optionnel** : Clé API OpenAI (pour le mode LLM)

### Vérifier l'installation Python

```bash
python --version
pip --version
```

### Étapes d'installation

#### 1️⃣ Cloner et naviguer dans le dossier

```bash
cd wordle-csp-solver
```

#### 2️⃣ Installer les dépendances

```bash
pip install -r src/requirements.txt
```

**Dépendances installées** :
- `colorama` - Interface CLI colorée
- `python-dotenv` - Gestion configuration
- `openai` - Intégration LLM (optionnel)

#### 3️⃣ Configuration (optionnel pour LLM)

Pour utiliser le mode LLM-Enhanced (Mode 3) :

```bash
# Copier le fichier exemple
cp src/.env.example src/.env

# Éditer src/.env et ajouter votre clé API OpenAI
OPENAI_API_KEY=sk-...votre_clé...
```

**Où obtenir la clé API ?**
1. Aller sur https://platform.openai.com/api-keys
2. Créer une nouvelle clé secrète
3. La copier dans src/.env

## Lancement

### 🎮 Jouer au jeu

```bash
python src/game_interface.py
```

**Menu** :
- Mode 1 : Assistant (le solveur vous aide)
- Mode 2 : Automatique (regardez résoudre)
- Mode 3 : LLM-Enhanced (IA avancée - nécessite API)

**Langue** :
- 1 : Anglais
- 2 : Français

### 🎯 Lancer les démonstrations

```bash
# Démo complète (6 démonstrations interactives)
python src/demo.py

# Interface jeu - Mode anglais
python src/jouer_english_complet.py

# Interface jeu - Mode français
python src/jouer_francais_perso.py
```

### 🧪 Lancer les tests

```bash
# Tests du solveur CSP (7 tests)
python src/test_csp_solver.py

# Tests de l'optimiseur (8 tests)
python src/test_optimizer.py

# Test de régression (bug SNAIL)
python src/test_snail_bug.py
```

**Résultat attendu** : ✓ All tests passed!

## Mode d'emploi détaillé

### Mode 1 : Assistant

L'interface vous guide pas à pas :

```
🎮 Bienvenue au Wordle CSP Solver !
Choisissez un mode:
  1. Mode Assistant - Je vous aide à résoudre
  2. Mode Auto - Regardez-moi résoudre
  3. Mode LLM - Assistance IA

Votre choix (1-3): 1

Choisissez une langue:
  1. English
  2. Français

Votre choix (1-2): 1

═══ Attempt 1/6 ═══

💡 Suggested guess: AROSE

Enter the word you guessed (or press Enter for 'AROSE'): arose
Enter feedback (G/Y/X): XXYGX

Your guess: ⬜ ⬜ 🟨 🟩 🟩

Solver Statistics:
  Total words in dictionary: 500
  Possible words remaining: 47
  Elimination rate: 90.6%
  Attempts used: 1/6

💡 Suggested guess: HOUSE
```

**Codes de feedback** :
- `G` = 🟩 Green (vert - correct)
- `Y` = 🟨 Yellow (jaune - présent)
- `X` = ⬜ Gray (gris - absent)

**Exemple** : `GGYXX` signifie vert-vert-jaune-gris-gris

### Mode 2 : Automatique

```
═══ Attempt 1/6 ═══
Solver guesses: AROSE
Feedback: ⬜⬜🟨🟩🟩
→ Possible words remaining: 47

═══ Attempt 2/6 ═══
Solver guesses: MOUSE
Feedback: ⬜🟩🟩🟩🟩
→ Possible words remaining: 3

═══ Attempt 3/6 ═══
Solver guesses: HOUSE
Feedback: 🟩🟩🟩🟩🟩
🎉 SOLVED! Found 'HOUSE' in 3 attempts!
```

### Mode 3 : LLM-Enhanced

```
🤖 LLM-Enhanced Mode activé

Vous:    "J'ai essayé AROSE et obtenu gris-gris-jaune-vert-vert"

IA:      "Excellente première tentative ! Le feedback indique que...
          Il reste 47 mots possibles dont HOUSE, MOUSE...
          Je recommande d'essayer HOUSE qui éliminera le maximum
          de mots quoi qu'il arrive."

Vous:    "Pourquoi HOUSE plutôt que MOUSE ?"

IA:      "Bonne question ! HOUSE a une entropie plus élevée (2.43 bits
          vs 2.21), ce qui signifie qu'il fournit plus d'information
          en moyenne. Statistiquement, cela réduit plus de candidats..."
```

## Dépannage

### ❌ Problème : "ModuleNotFoundError: No module named 'colorama'"

**Solution** :
```bash
pip install -r src/requirements.txt
```

### ❌ Problème : "FileNotFoundError: Dictionary file not found"

**Solution** : Les dictionnaires se chargent automatiquement par défaut. C'est normal. Vous pouvez aussi :
```python
dict_mgr.load_default_english()  # Charger explicitement
```

### ❌ Problème : "OpenAI API key not found"

**Solution** :
```bash
# Copier l'exemple
cp src/.env.example src/.env

# Éditer et ajouter votre clé
nano src/.env  # ou votre éditeur préféré

# Vérifier le fichier
cat src/.env
```

### ❌ Problème : Les tests échouent

**Solution** :
```bash
# Réinstaller les dépendances
pip install --upgrade -r src/requirements.txt

# Relancer les tests
python src/test_csp_solver.py -v
```

## Personnalisation

### Utiliser un dictionnaire personnalisé

```python
from src.dictionary_manager import DictionaryManager

dict_mgr = DictionaryManager(word_length=5)

# Charger depuis un fichier
dict_mgr.load_from_file("../data/mon_dictionnaire.txt")

# Ou ajouter des mots manuellement
dict_mgr.add_words(["hello", "world", "custom"])

# Utiliser
words = dict_mgr.get_words()
```

**Format du fichier** : un mot par ligne (5 lettres)

```
house
mouse
arose
crane
trace
```

### Changer la stratégie d'optimisation

```python
from src.csp_solver import WordleCSPSolver

solver = WordleCSPSolver(5, dictionary)

# Stratégies disponibles
best = solver.get_best_guess(strategy="max_info")      # Entropie (recommandée)
best = solver.get_best_guess(strategy="minimax")       # Pire cas minimisé
best = solver.get_best_guess(strategy="frequency")     # Fréquence des lettres
```

## Commandes utiles

```bash
# Installation
pip install -r src/requirements.txt

# Jouer
python src/game_interface.py

# Démos
python src/demo.py

# Tests
python src/test_csp_solver.py
python src/test_optimizer.py
python src/test_snail_bug.py

# Vérifier la structure
ls -la src/

# Voir les fichiers Python
find src -name "*.py"
```

## Version et dépendances

### Versions testées
- Python 3.8, 3.9, 3.10, 3.11
- colorama >= 0.4.3
- python-dotenv >= 0.19.0
- openai >= 0.27.0 (optionnel)

### Vérifier les versions installées
```bash
pip list | grep -E "colorama|python-dotenv|openai"
```

## Environnement virtuel (optionnel mais recommandé)

Pour isoler les dépendances :

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r src/requirements.txt

# Pour désactiver :
deactivate
```

## Prochaines étapes

- ✅ Installation complète ? → Lancez `python src/demo.py`
- ✅ Prêt à jouer ? → Lancez `python src/game_interface.py`
- ✅ Besoin de détails techniques ? → Consultez `DOCUMENTATION.md`
- ✅ Questions ? → Lisez le `README.md`

## Support

| Problème | Solution |
|----------|----------|
| Module not found | `pip install -r src/requirements.txt` |
| Permission denied | `chmod +x src/*.py` (macOS/Linux) |
| Dictionnaire vide | `dict_mgr.load_default_english()` |
| API OpenAI error | Vérifier clé dans `src/.env` |
| Tests failing | Réinstaller les dépendances |

---

**Prêt ?** Lancez :
```bash
python src/demo.py
```

ou

```bash
python src/game_interface.py
```

Bon jeu ! 🎮🧠

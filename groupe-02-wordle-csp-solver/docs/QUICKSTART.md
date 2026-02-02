# Guide de démarrage rapide - Wordle CSP Solver

## Installation rapide

```bash
# 1. Se placer dans le dossier
cd wordle-csp-solver

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. (Optionnel) Configurer OpenAI pour LLM
cp .env.example .env
# Éditer .env et ajouter: OPENAI_API_KEY=your_key_here
```

## Lancer la démonstration

```bash
python demo.py
```

Cette démo interactive montre toutes les capacités du solveur.

## Jouer maintenant

```bash
cd src
python game_interface.py
```

Choisissez ensuite :
- **Mode 1** : Assistant vous aide à résoudre
- **Mode 2** : Regardez le solveur résoudre automatiquement
- **Mode 3** : Assistant avec IA (nécessite OpenAI API)

## Test rapide

```bash
# Tester le solveur CSP
cd tests
python test_csp_solver.py

# Tester l'optimiseur
python test_optimizer.py
```

## Utilisation programmatique simple

```python
from src.csp_solver import WordleCSPSolver, Feedback
from src.dictionary_manager import DictionaryManager

# Setup
dict_mgr = DictionaryManager()
dict_mgr.load_default_english()

solver = WordleCSPSolver(5, dict_mgr.get_words())

# Exemple: Le mot est "HOUSE"
# Vous essayez "AROSE" et obtenez: gris-gris-jaune-vert-vert

solver.add_feedback("arose", [
    Feedback.ABSENT,   # A: gris
    Feedback.ABSENT,   # R: gris
    Feedback.PRESENT,  # O: jaune (dans le mot mais pas ici)
    Feedback.CORRECT,  # S: vert (correct!)
    Feedback.CORRECT   # E: vert (correct!)
])

# Voir les mots possibles
print(solver.get_possible_words())  # ['horse', 'house', 'mouse', ...]

# Obtenir la meilleure suggestion
print(solver.get_best_guess())  # 'house'
```

## Codes des feedbacks

Dans Wordle :
- 🟩 **Vert (GREEN)** = Lettre correcte, bonne position → `Feedback.CORRECT`
- 🟨 **Jaune (YELLOW)** = Lettre dans le mot, mauvaise position → `Feedback.PRESENT`
- ⬜ **Gris (GRAY)** = Lettre absente du mot → `Feedback.ABSENT`

Dans l'interface CLI, entrez le feedback avec :
- `G` pour vert
- `Y` pour jaune
- `X` pour gris

Exemple : `GGYXX` signifie vert-vert-jaune-gris-gris

## Exemples d'utilisation

### Exemple 1 : Mode assistant

```
$ python src/game_interface.py
> Choisir mode: 1

═══ Attempt 1/6 ═══
💡 Suggested guess: AROSE

Enter the word you guessed: arose
Enter feedback (G/Y/X): XXYGX

[Le solveur filtre automatiquement]
Possible words remaining: 47
Sample possible words: house, mouse, louse, ...

💡 Suggested guess: HOUSE
```

### Exemple 2 : Mode automatique

```
$ python src/game_interface.py
> Choisir mode: 2
> Enter secret word: HOUSE

═══ Attempt 1/6 ═══
Solver guesses: AROSE
Feedback: ⬜ ⬜ 🟨 🟩 🟩
Possible words remaining: 47

═══ Attempt 2/6 ═══
Solver guesses: MOUSE
Feedback: ⬜ 🟩 🟩 🟩 🟩
Possible words remaining: 3

═══ Attempt 3/6 ═══
Solver guesses: HOUSE
Feedback: 🟩 🟩 🟩 🟩 🟩
🎉 SOLVED!
```

## Architecture simple

```
src/
├── csp_solver.py        ← Cœur du solveur CSP
├── dictionary_manager.py ← Gère les dictionnaires
├── optimizer.py         ← Stratégies avancées
├── llm_integration.py   ← Intégration OpenAI
└── game_interface.py    ← Interface utilisateur
```

## Concepts clés en 2 minutes

### 1. CSP (Constraint Satisfaction Problem)
Chaque feedback de Wordle = contrainte :
- Vert : `position[i] = lettre`
- Jaune : `lettre ∈ mot ET position[i] ≠ lettre`
- Gris : `lettre ∉ mot`

Le solveur filtre tous les mots qui ne satisfont pas ces contraintes.

### 2. Optimisation par entropie
Choisit le mot qui donne le plus d'information :
- Haute entropie = beaucoup de patterns possibles = beaucoup d'information
- Calcul : `H = -Σ p(i) log₂(p(i))`

### 3. Stratégies
- **Max Info** : Maximise l'entropie (meilleur en moyenne)
- **Minimax** : Minimise le pire cas
- **Fréquence** : Favorise les lettres communes

## Troubleshooting

### Problème : Module not found
```bash
# Vérifier que vous êtes dans le bon dossier
pwd  # Devrait afficher .../wordle-csp-solver

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème : OpenAI API error
```bash
# Mode LLM optionnel, utiliser les modes 1 ou 2 sans API
# Ou vérifier votre clé dans .env
cat .env
```

### Problème : Dictionnaire vide
```python
# Le dictionnaire se charge automatiquement
# Sinon, charger manuellement :
dict_mgr.load_default_english()  # ou load_default_french()
```

## Personnalisation rapide

### Ajouter vos propres mots

```python
dict_mgr = DictionaryManager()
dict_mgr.add_words(["hello", "world", "custom"])
```

### Changer la stratégie

```python
# Dans csp_solver.py, modifier get_best_guess()
solver.get_best_guess(strategy="minimax")  # Au lieu de "max_info"
```

### Utiliser un dictionnaire externe

```python
dict_mgr = DictionaryManager()
dict_mgr.load_from_file("mon_dictionnaire.txt")
```

Format du fichier : un mot par ligne (5 lettres).

## Ressources

- **README.md** : Documentation complète
- **demo.py** : Démonstrations interactives
- **tests/** : Tests unitaires

## Support

Pour des questions :
1. Lire le README.md complet
2. Regarder les exemples dans demo.py
3. Examiner les tests dans tests/

Bon jeu ! 🎮

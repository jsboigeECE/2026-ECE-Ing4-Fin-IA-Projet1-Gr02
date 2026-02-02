# 📚 Documentation Technique Complète

## Table des matières

- [Architecture générale](#architecture-générale)
- [Modules principaux](#modules-principaux)
- [Concepts théoriques](#concepts-théoriques)
- [Guide des algorithmes](#guide-des-algorithmes)
- [API complète](#api-complète)
- [Exemples avancés](#exemples-avancés)
- [Performance et optimisations](#performance-et-optimisations)

## Architecture générale

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────┐
│                  game_interface.py                  │
│         (Interface CLI - 3 modes de jeu)            │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼──┐   ┌────▼──┐  ┌───▼───┐
    │  CSP  │   │Optimizer  │  LLM  │
    │Solver │   │  (Optim)  │Engine │
    └────┬──┘   └────┬──┘  └───┬───┘
         │           │         │
         └───────────┼─────────┘
                     │
         ┌───────────▼────────────┐
         │ Dictionary Manager     │
         │ (Gestion du lexique)   │
         └───────────────────────┘
```

### Flux de données

```
1. Utilisateur entre feedback
   ↓
2. game_interface capture input
   ↓
3. CSP Solver applique contraintes
   ↓
4. Optimizer calcule meilleur mot
   ↓
5. LLM (optionnel) fournit contexte
   ↓
6. Interface affiche résultats
```

## Modules principaux

### 1. csp_solver.py (~240 lignes)

**Responsabilité** : Implémentation du Constraint Satisfaction Problem

#### Classe : `Feedback` (Enum)
```python
class Feedback(Enum):
    CORRECT = "green"     # 🟩 Lettre correcte, bonne position
    PRESENT = "yellow"    # 🟨 Lettre présente, mauvaise position
    ABSENT = "gray"       # ⬜ Lettre absente du mot
```

#### Classe : `WordleCSPSolver`

**Initialisation** :
```python
solver = WordleCSPSolver(word_length=5, dictionary=["house", "mouse", ...])
```

**Attributs internes** :
```python
self.word_length: int                         # Longueur des mots
self.dictionary: List[str]                    # Dictionnaire complet
self.possible_words: Set[str]                 # Mots satisfaisant les contraintes
self.correct_positions: Dict[int, str]        # {position: lettre} correcte
self.present_letters: Set[str]                # Lettres présentes mais mal placées
self.absent_letters: Set[str]                 # Lettres à éliminer
self.wrong_positions: Dict[str, Set[int]]     # {lettre: {positions interdites}}
```

**Méthodes principales** :

```python
def add_feedback(self, guess: str, feedback: List[Feedback]) -> None:
    """
    Ajoute un feedback et met à jour les contraintes.
    
    Args:
        guess: Le mot essayé (5 lettres)
        feedback: Liste de 5 Feedback (CORRECT, PRESENT, ou ABSENT)
    
    Exemple:
        solver.add_feedback("arose", [
            Feedback.ABSENT,   # A
            Feedback.ABSENT,   # R
            Feedback.PRESENT,  # O
            Feedback.CORRECT,  # S
            Feedback.CORRECT   # E
        ])
    """
```

```python
def get_possible_words(self) -> List[str]:
    """
    Retourne tous les mots satisfaisant les contraintes.
    
    Returns:
        Liste triée des mots possibles
    
    Complexité: O(n) où n = taille du dictionnaire
    """
```

```python
def get_best_guess(self, strategy: str = "max_info") -> Optional[str]:
    """
    Suggère le meilleur prochain mot.
    
    Args:
        strategy: "max_info" (entropie), "minimax", ou "frequency"
    
    Returns:
        Meilleur mot selon la stratégie
    """
```

```python
def get_stats(self) -> Dict:
    """
    Retourne les statistiques actuelles.
    
    Returns: {
        "total_words": int,
        "possible_words": int,
        "elimination_rate": float,  # Entre 0 et 1
        "correct_positions": Dict[int, str],
        "present_letters": Set[str],
        "absent_letters": Set[str]
    }
    """
```

```python
def reset() -> None:
    """Réinitialise le solveur à l'état initial."""
```

**Algorithme interne** :

```
Pour chaque feedback reçu:
  1. Marquer les positions correctes (vert)
  2. Ajouter les lettres présentes (jaune)
  3. Ajouter les lettres absentes (gris)
  4. Filtrer le dictionnaire

Filtrage:
  - Vérifier chaque mot du dictionnaire
  - Évaluer s'il satisfait TOUTES les contraintes
  - Conserver uniquement les mots valides
```

### 2. optimizer.py (~280 lignes)

**Responsabilité** : Calcul des meilleures stratégies d'optimisation

#### Classe : `WordleOptimizer`

**Initialisation** :
```python
optimizer = WordleOptimizer(words)
```

**Stratégies d'optimisation** :

#### Strategy 1 : Entropie maximale

```python
def calculate_entropy(self, word: str, candidates: List[str]) -> float:
    """
    Calcule l'entropie de Shannon pour un mot.
    
    Entropie = -Σ p(i) × log₂(p(i))
    
    où p(i) est la probabilité du pattern i
    
    Complexité: O(n²) où n = nombre de candidats
    """
```

**Exemple** :
```python
entropy = optimizer.calculate_entropy("house", candidates)
# Retourne: 2.43 bits
# Signification: "house" fournit 2.43 bits d'information en moyenne
```

#### Strategy 2 : Minimax

```python
def get_minimax_guess(self, candidates: List[str]) -> str:
    """
    Sélectionne le mot minimisant le pire cas.
    
    Minimise: max(nombre de mots restants pour chaque pattern)
    
    Objectif: Garantir une résolution en 6 coups maximum
    """
```

#### Strategy 3 : Fréquence des lettres

```python
def get_letter_frequencies(self, words: List[str]) -> Dict[tuple, float]:
    """
    Calcule la fréquence de chaque lettre à chaque position.
    
    Returns: {
        (position, lettre): fréquence,
        (0, 'a'): 0.15,
        (0, 'b'): 0.08,
        ...
    }
    """
```

```python
def score_word_by_frequency(self, word: str, frequencies: Dict) -> float:
    """Score un mot basé sur les fréquences.
    
    Score = Σ frequencies[(position, lettre)]
    + bonus pour lettres uniques
    """
```

**Autres méthodes** :

```python
def get_strategic_first_guess(self, words: List[str]) -> str:
    """Retourne le meilleur premier mot (ex: "arose", "slate")"""

def get_hard_mode_guess(self, candidates: List[str], constraints: Dict) -> str:
    """Sélectionne un mot respectant les contraintes (mode difficile)"""

def analyze_word_patterns(self, words: List[str]) -> Dict:
    """Analyse les patterns linguistiques (préfixes, suffixes, voyelles)"""
```

### 3. dictionary_manager.py (~150 lignes)

**Responsabilité** : Gestion des dictionnaires

#### Classe : `DictionaryManager`

```python
def __init__(self, word_length: int = 5):
    """Initialise avec une longueur de mot cible"""
```

**Chargement de dictionnaires** :

```python
def load_from_file(self, filepath: str) -> None:
    """
    Charge les mots d'un fichier texte.
    
    Format: un mot par ligne (5 lettres)
    
    Args:
        filepath: Chemin relatif au module (résolu automatiquement)
    
    Exemple: load_from_file("../data/mon_dictionnaire.txt")
    """
```

```python
def load_default_english() -> None:
    """Charge ~500 mots anglais intégrés"""

def load_default_french() -> None:
    """Charge ~150 mots français intégrés"""
```

**Opérations** :

```python
def add_words(self, words: List[str]) -> None:
    """Ajoute des mots au dictionnaire"""

def get_words(self) -> List[str]:
    """Retourne tous les mots (triés)"""

def contains(self, word: str) -> bool:
    """Vérifie si un mot est dans le dictionnaire"""

def size(self) -> int:
    """Retourne le nombre de mots"""
```

### 4. llm_integration.py (~240 lignes)

**Responsabilité** : Intégration OpenAI avec function calling

#### Classe : `WordleLLMAssistant`

```python
def __init__(self, api_key: str = None):
    """
    Initialise l'assistant LLM.
    
    Args:
        api_key: Clé API OpenAI (ou depuis .env)
    """
```

**Fonctions exposées au LLM** :

1. **apply_wordle_constraints**
   ```python
   {
       "guess": "arose",
       "feedback": ["absent", "absent", "present", "correct", "correct"]
   }
   ```
   Applique les contraintes d'un feedback Wordle.

2. **get_possible_words**
   ```python
   {"limit": 20}
   ```
   Retourne les mots satisfaisant les contraintes actuelles.

3. **suggest_best_guess**
   ```python
   {"strategy": "max_info"}
   ```
   Suggère le meilleur prochain mot.

4. **get_solver_stats**
   Retourne les statistiques du solveur.

5. **analyze_word_pattern**
   ```python
   {"aspect": "letter_frequency"}
   ```
   Analyse les patterns linguistiques.

**Interaction** :

```python
def chat_with_context(self, message: str, functions: Dict) -> str:
    """
    Envoie un message au LLM avec les fonctions disponibles.
    
    Le LLM peut appeler les fonctions pour répondre.
    
    Args:
        message: Message de l'utilisateur
        functions: Dict de fonctions disponibles
    
    Returns:
        Réponse du LLM
    """
```

### 5. game_interface.py (~320 lignes)

**Responsabilité** : Interface CLI interactive

#### Classe : `WordleGameInterface`

```python
def __init__(self, 
             word_length: int = 5,
             language: str = "english",
             use_llm: bool = False):
    """Initialise l'interface de jeu"""
```

**Modes de jeu** :

```python
def play_assistant_mode(self) -> None:
    """
    Mode assistant : Le solveur aide l'utilisateur.
    
    Flux:
    1. Suggère un mot
    2. Capte le feedback utilisateur
    3. Affiche les mots restants
    4. Répète jusqu'à victoire
    """

def play_solver_mode(self, secret_word: str) -> None:
    """
    Mode automatique : Le solveur résout seul.
    
    Flux:
    1. Génère le feedback (mot secret connu)
    2. Suggère le meilleur mot
    3. Affiche les statistiques
    4. Répète jusqu'à résolution
    """
```

**Utilitaires** :

```python
def display_stats(self) -> None:
    """Affiche les statistiques en temps réel"""

def parse_feedback(self, feedback_str: str) -> Optional[List[Feedback]]:
    """Parse 'GGYXX' en liste de Feedback"""

def display_word_colored(self, word: str, feedback: List) -> str:
    """Affiche un mot avec les codes couleur Wordle"""
```

## Concepts théoriques

### 1. Constraint Satisfaction Problem (CSP)

#### Définition formelle

Un CSP est un triplet (V, D, C) où :
- **V** = ensemble de variables
- **D** = domaines de chaque variable
- **C** = ensemble de contraintes

#### Dans Wordle

```
Variables: position[0], position[1], ..., position[4]
Domaines: {a-z} pour chaque position
Contraintes:
  - position[0] = 's'  (si vert pour 's' en position 0)
  - position[1] ≠ 'o'  (si jaune pour 'o' en position 1)
  - 'a' ∉ mot          (si gris pour 'a')
```

#### Algorithme de propagation

```python
def apply_constraints(guess, feedback):
    for i, (letter, fb) in enumerate(zip(guess, feedback)):
        if fb == CORRECT:
            # position[i] = letter
            correct_positions[i] = letter
            domain[i] = {letter}
        elif fb == PRESENT:
            # letter ∈ word AND position[i] ≠ letter
            present_letters.add(letter)
            wrong_positions[letter].add(i)
        elif fb == ABSENT:
            # letter ∉ word
            absent_letters.add(letter)
            for i in range(5):
                domain[i].remove(letter)  # Si lettre unique
```

### 2. Théorie de l'information

#### Entropie de Shannon

```
H(X) = -Σ p(i) × log₂(p(i))
```

où p(i) est la probabilité du pattern i.

**Interprétation** :
- H = 0 : Certitude absolue (1 mot possible)
- H = 1 : Bonne réduction
- H = 3+ : Peu d'information gagnée

#### Gain d'information

```
IG = H(avant) - H(après)
```

Plus le gain est élevé, meilleur est le mot choisi.

#### Application à Wordle

Pour chaque mot candidat :
1. Calculer tous les patterns possibles
2. Compter les mots pour chaque pattern
3. Calculer la probabilité de chaque pattern
4. Calculer l'entropie
5. Choisir le mot maximisant l'entropie

### 3. Stratégie Minimax

```
Pour chaque mot candidat:
  Pour chaque pattern possible:
    Compter les mots restants
  Compter le maximum
Choisir le mot minimisant ce maximum
```

**Objective** : Garantir une résolution en nombre de coups limité.

## Guide des algorithmes

### Algorithme CSP - Filtrage

```python
def filter_dictionary(constraints):
    """
    Filtre le dictionnaire selon les contraintes.
    
    Complexité: O(n × m) où:
    - n = taille du dictionnaire
    - m = longueur des mots
    """
    filtered = []
    for word in dictionary:
        if satisfies_all_constraints(word, constraints):
            filtered.append(word)
    return filtered

def satisfies_all_constraints(word, constraints):
    # Vérifier positions correctes
    for pos, letter in constraints.correct_positions.items():
        if word[pos] != letter:
            return False
    
    # Vérifier lettres présentes
    for letter in constraints.present_letters:
        if letter not in word:
            return False
    
    # Vérifier lettres absentes
    for letter in constraints.absent_letters:
        if letter in word:
            return False
    
    # Vérifier positions interdites
    for letter, positions in constraints.wrong_positions.items():
        for pos in positions:
            if word[pos] == letter:
                return False
    
    return True
```

### Algorithme Entropie

```python
def calculate_entropy(word, candidates):
    """Calcule l'entropie pour un mot proposé."""
    
    # Étape 1: Compter les patterns
    patterns = {}
    for candidate in candidates:
        pattern = generate_pattern(word, candidate)
        patterns[pattern] = patterns.get(pattern, 0) + 1
    
    # Étape 2: Calculer l'entropie
    total = len(candidates)
    entropy = 0
    
    for count in patterns.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy

def generate_pattern(guess, secret):
    """Génère le pattern pour un (guess, secret) pair."""
    pattern = [None] * 5
    secret_chars = list(secret)
    
    # Première passe: positions correctes
    for i, (g, s) in enumerate(zip(guess, secret)):
        if g == s:
            pattern[i] = 'correct'
            secret_chars[i] = None
    
    # Deuxième passe: lettres présentes
    for i, g in enumerate(guess):
        if pattern[i] is None:  # Pas déjà marqué
            if g in secret_chars:
                pattern[i] = 'present'
                secret_chars[secret_chars.index(g)] = None
            else:
                pattern[i] = 'absent'
    
    return tuple(pattern)
```

## API complète

### Classe WordleCSPSolver

```python
class WordleCSPSolver:
    # Initialisation
    __init__(word_length: int, dictionary: List[str]) -> None
    
    # Interaction
    add_feedback(guess: str, feedback: List[Feedback]) -> None
    reset() -> None
    
    # Requêtes
    get_possible_words() -> List[str]
    get_best_guess(strategy: str = "max_info") -> Optional[str]
    get_stats() -> Dict
    
    # Interne
    _satisfies_constraints(word: str) -> bool
    _propagate_constraints() -> None
```

### Classe WordleOptimizer

```python
class WordleOptimizer:
    # Initialisation
    __init__(words: List[str]) -> None
    
    # Calculs
    calculate_entropy(word: str, candidates: List[str]) -> float
    get_letter_frequencies(words: List[str]) -> Dict
    score_word_by_frequency(word: str, frequencies: Dict) -> float
    
    # Stratégies
    get_best_guess_by_entropy(candidates: List[str]) -> str
    get_minimax_guess(candidates: List[str]) -> str
    get_strategic_first_guess(words: List[str]) -> str
    get_hard_mode_guess(candidates: List[str], constraints: Dict) -> str
    
    # Analyse
    analyze_word_patterns(words: List[str]) -> Dict
```

### Classe DictionaryManager

```python
class DictionaryManager:
    # Initialisation
    __init__(word_length: int = 5) -> None
    
    # Chargement
    load_from_file(filepath: str) -> None
    load_default_english() -> None
    load_default_french() -> None
    
    # Opérations
    add_words(words: List[str]) -> None
    get_words() -> List[str]
    contains(word: str) -> bool
    size() -> int
```

### Classe WordleLLMAssistant

```python
class WordleLLMAssistant:
    # Initialisation
    __init__(api_key: str = None) -> None
    
    # Interaction
    chat_with_context(message: str, functions: Dict) -> str
    
    # Fonctions pour LLM
    apply_wordle_constraints(guess: str, feedback: List[str]) -> Dict
    get_possible_words(limit: int = 20) -> Dict
    suggest_best_guess(strategy: str = "max_info") -> Dict
    get_solver_stats() -> Dict
    analyze_word_pattern(aspect: str) -> Dict
```

## Exemples avancés

### Exemple 1 : Résolution complète en code

```python
from src.csp_solver import WordleCSPSolver, Feedback
from src.dictionary_manager import DictionaryManager
from src.optimizer import WordleOptimizer

# Setup
dict_mgr = DictionaryManager()
dict_mgr.load_default_english()
words = dict_mgr.get_words()

solver = WordleCSPSolver(5, words)
optimizer = WordleOptimizer(words)

# Tentative 1: Utiliser une première suggestion optimale
guess1 = optimizer.get_strategic_first_guess(words)
print(f"Tentative 1: {guess1}")  # "arose"

# Feedback simulé
feedback1 = [Feedback.ABSENT, Feedback.ABSENT, Feedback.PRESENT, 
             Feedback.CORRECT, Feedback.CORRECT]
solver.add_feedback(guess1, feedback1)

# Tentative 2: Meilleur mot selon entropie
possible = solver.get_possible_words()
guess2 = optimizer.get_best_guess_by_entropy(possible)
print(f"Tentative 2: {guess2}")  # "house"

# Vérifier si c'est la solution
if guess2 == secret:
    print("🎉 Résolu en 2 tentatives !")
```

### Exemple 2 : Avec intégration LLM

```python
from src.llm_integration import WordleLLMAssistant
from src.csp_solver import WordleCSPSolver

solver = WordleCSPSolver(5, words)
llm = WordleLLMAssistant(api_key="sk-...")

# Définir les fonctions disponibles
functions = {
    "apply_constraints": lambda g, f: solver.add_feedback(g, f),
    "get_words": lambda: solver.get_possible_words(),
    "suggest": lambda: solver.get_best_guess(),
    "stats": lambda: solver.get_stats()
}

# Converser avec le LLM
response = llm.chat_with_context(
    "Je viens de trouver que la 1ère lettre est S, et A n'est pas dans le mot. Que me conseilles-tu ?",
    functions
)
print(response)
```

### Exemple 3 : Analyse de stratégies

```python
from src.optimizer import WordleOptimizer

optimizer = WordleOptimizer(words)

# Comparer les stratégies
strategies_results = {}

for strategy in ["max_info", "minimax", "frequency"]:
    attempts = []
    solver = WordleCSPSolver(5, words)
    
    for attempt in range(6):
        guess = solver.get_best_guess(strategy=strategy) or "failed"
        attempts.append(guess)
        
        if attempt < 2:  # Simul feedback
            solver.add_feedback(guess, [Feedback.ABSENT] * 5)
    
    strategies_results[strategy] = attempts

# Afficher résultats
for strategy, attempts in strategies_results.items():
    print(f"{strategy}: {' → '.join(attempts)}")
```

## Performance et optimisations

### Complexité algorithmique

| Opération | Complexité | Notes |
|-----------|-----------|-------|
| add_feedback | O(n) | n = taille dictionnaire |
| get_possible_words | O(n × m) | m = longueur mots |
| calculate_entropy | O(n²) | n = candidats |
| get_best_guess | O(n² × c) | c = candidats |

### Optimisations implémentées

1. **Lazy evaluation** : Calculs retardés jusqu'à la demande
2. **Caching** : Résultats en mémoire
3. **Pruning** : Élagage de l'espace de recherche
4. **Early termination** : Arrêt prématuré si réponse trouvée

### Conseils pour améliorer les performances

```python
# Limiter l'espace de recherche
candidates = solver.get_possible_words()[:100]  # Top 100
best = optimizer.get_best_guess_by_entropy(candidates)

# Cacher les calculs coûteux
entropy_cache = {}
for word in candidates:
    if word not in entropy_cache:
        entropy_cache[word] = calculate_entropy(word, candidates)

# Utiliser un dictionnaire réduit
small_dict = [w for w in words if w in common_words]
solver = WordleCSPSolver(5, small_dict)
```

---

**Pour plus d'infos** :
- Consultez les fichiers source dans `src/`
- Lancez les tests : `python src/test_*.py`
- Exécutez les démos : `python src/demo.py`

# Guide d'intégration LLM - Wordle CSP Solver

## 📖 Vue d'ensemble

Ce guide explique comment le solveur Wordle utilise le **function calling** d'OpenAI pour combiner raisonnement linguistique (LLM) et résolution par contraintes (CSP).

## 🎯 Concept : Function Calling

Le function calling permet au LLM d'appeler des fonctions Python pendant une conversation, combinant ainsi :
- **Raisonnement linguistique** du LLM
- **Calculs précis** du solveur CSP
- **Optimisation mathématique** de la théorie de l'information

### Architecture

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Utilisateur│────────▶│      LLM     │────────▶│  CSP Solver  │
│              │ Question│   (OpenAI)   │ Function│              │
│              │         │              │  Call   │              │
│              │◀────────│              │◀────────│              │
│              │ Réponse │              │ Résultat│              │
└──────────────┘         └──────────────┘         └──────────────┘
```

## 🔧 Fonctions exposées au LLM

### 1. apply_wordle_constraints
Applique les contraintes d'un feedback Wordle.

```python
{
    "name": "apply_wordle_constraints",
    "description": "Apply constraints from a Wordle guess feedback",
    "parameters": {
        "guess": str,      # Le mot essayé (5 lettres)
        "feedback": list   # ["green", "yellow", "gray"] pour chaque lettre
    }
}
```

**Exemple d'utilisation par le LLM** :
```
User: "J'ai essayé AROSE et j'ai obtenu gris-gris-jaune-vert-vert"

LLM pense: Je dois appeler apply_wordle_constraints
LLM appelle: apply_wordle_constraints(
    guess="arose",
    feedback=["gray", "gray", "yellow", "green", "green"]
)
Résultat: {"words_remaining": 47, "success": true}

LLM répond: "D'accord ! Avec ce feedback, il reste 47 mots possibles.
Le 'O' est dans le mot mais pas en position 2, et les lettres S et E
sont correctes aux positions 3 et 4. Je suggère d'essayer HOUSE."
```

### 2. get_possible_words
Récupère la liste des mots encore possibles.

```python
{
    "name": "get_possible_words",
    "description": "Get list of all words that satisfy current constraints",
    "parameters": {
        "limit": int  # Nombre max de mots à retourner (défaut: 20)
    }
}
```

**Exemple** :
```
LLM appelle: get_possible_words(limit=10)
Résultat: ["house", "horse", "mouse", "louse", ...]

LLM répond: "Les 10 mots les plus probables sont : house, horse,
mouse... Remarquez qu'ils partagent tous les lettres O, S, E."
```

### 3. suggest_best_guess
Suggère le meilleur prochain mot selon une stratégie.

```python
{
    "name": "suggest_best_guess",
    "description": "Get the optimal next guess",
    "parameters": {
        "strategy": str  # "max_info", "minimax", ou "random"
    }
}
```

**Exemple** :
```
LLM appelle: suggest_best_guess(strategy="max_info")
Résultat: {"guess": "house", "entropy": 2.43}

LLM répond: "Je recommande HOUSE. Ce mot maximise le gain d'information
attendu (entropie de 2.43 bits) et devrait éliminer le plus de candidats."
```

### 4. get_solver_stats
Obtient les statistiques actuelles du solveur.

```python
{
    "name": "get_solver_stats",
    "description": "Get current statistics about the solving process",
    "parameters": {}
}
```

**Exemple** :
```
LLM appelle: get_solver_stats()
Résultat: {
    "total_words": 500,
    "possible_words": 12,
    "elimination_rate": 0.976,
    "correct_positions": {3: "s", 4: "e"},
    "present_letters": ["o"],
    "absent_letters": ["a", "r"]
}

LLM répond: "Excellent progrès ! Vous avez éliminé 97.6% des mots.
Il ne reste que 12 candidats. Vous savez que S et E sont correctement
placés, et que O est dans le mot."
```

### 5. analyze_word_pattern
Analyse les patterns linguistiques dans les mots restants.

```python
{
    "name": "analyze_word_pattern",
    "description": "Analyze linguistic patterns in remaining words",
    "parameters": {
        "aspect": str  # "letter_frequency", "vowel_positions", etc.
    }
}
```

**Exemple** :
```
LLM appelle: analyze_word_pattern(aspect="letter_frequency")
Résultat: {
    "most_common": [("h", 8), ("o", 12), ("u", 7)],
    "patterns": ["_ou_e", "_o_se"]
}

LLM répond: "En analysant les mots restants, je remarque que O apparaît
dans tous les mots et que le pattern _OU_E est très fréquent.
Les mots se terminent presque tous par SE."
```

## 💡 Cas d'usage complets

### Cas 1 : Assistant de résolution

```python
from llm_integration import WordleLLMAssistant
from csp_solver import WordleCSPSolver
from dictionary_manager import DictionaryManager

# Setup
dict_mgr = DictionaryManager()
dict_mgr.load_default_english()
solver = WordleCSPSolver(5, dict_mgr.get_words())
llm = WordleLLMAssistant(api_key="your-key")

# Définir les fonctions disponibles
functions = {
    "apply_wordle_constraints": lambda guess, feedback: {
        "success": solver.add_feedback(guess, feedback),
        "words_remaining": len(solver.get_possible_words())
    },
    "get_possible_words": lambda limit=20: {
        "words": solver.get_possible_words()[:limit],
        "total": len(solver.get_possible_words())
    },
    "suggest_best_guess": lambda strategy="max_info": {
        "guess": solver.get_best_guess(strategy),
        "strategy_used": strategy
    },
    "get_solver_stats": lambda: solver.get_stats(),
    "analyze_word_pattern": lambda aspect: {
        "aspect": aspect,
        "analysis": "Pattern analysis result..."
    }
}

# Conversation
response = llm.chat_with_context(
    "J'ai essayé AROSE et obtenu: A gris, R gris, O jaune, S vert, E vert. Que dois-je faire ?",
    functions
)

print(response)
# Output: "Excellente première tentative ! Le feedback indique que..."
```

### Cas 2 : Analyse stratégique

```python
# Demander une analyse approfondie
response = llm.chat_with_context(
    "Analyse la situation actuelle et explique quelle stratégie utiliser",
    functions
)

# Le LLM va :
# 1. Appeler get_solver_stats() pour voir l'état
# 2. Appeler analyze_word_pattern() pour trouver des patterns
# 3. Appeler suggest_best_guess() pour différentes stratégies
# 4. Comparer et expliquer

print(response)
# Output: "Basé sur les 12 mots restants, voici mon analyse..."
```

### Cas 3 : Apprentissage interactif

```python
# L'utilisateur veut comprendre
response = llm.chat_with_context(
    "Pourquoi suggères-tu HOUSE plutôt que MOUSE ?",
    functions
)

# Le LLM peut :
# 1. Calculer l'entropie de chaque mot
# 2. Expliquer la théorie de l'information
# 3. Montrer les patterns éliminés

print(response)
# Output: "Excellente question ! HOUSE élimine en moyenne 8.3 mots..."
```

## 🎓 Avantages de l'approche hybride

### 1. Précision mathématique
Le CSP garantit que tous les mots satisfont les contraintes :
```python
# CSP vérifie automatiquement TOUTES les contraintes
for word in dictionary:
    if satisfies_all_constraints(word):
        possible_words.add(word)
```

### 2. Raisonnement linguistique
Le LLM comprend le contexte et explique :
```
User: "Je veux minimiser le pire cas"
LLM: "D'accord, j'utilise la stratégie minimax alors..."
[Appelle suggest_best_guess(strategy="minimax")]
```

### 3. Flexibilité conversationnelle
```
User: "Et si le mot a deux lettres identiques ?"
LLM: "Bonne question ! Avec le CSP, cela crée des contraintes
supplémentaires. Par exemple, si 'E' apparaît en jaune deux fois..."
```

## 🔍 Exemples de conversations complètes

### Conversation 1 : Résolution guidée

```
User: Aide-moi à résoudre Wordle

LLM: Bien sûr ! Commençons. Pour la première tentative, je recommande
AROSE qui maximise la couverture des voyelles.

User: J'ai essayé AROSE: A-gris, R-gris, O-jaune, S-vert, E-vert

LLM: [Appelle apply_wordle_constraints("arose", ["gray", "gray", "yellow", "green", "green"])]
[Appelle get_possible_words(limit=10)]

LLM: Parfait ! Il reste 47 mots possibles. Les plus probables sont:
house, horse, mouse, louse. Je recommande HOUSE car il éliminera
le maximum de mots quoi qu'il arrive.

User: Ok, HOUSE: H-vert, O-vert, U-vert, S-vert, E-vert !

LLM: 🎉 Félicitations ! Vous avez trouvé le mot en 2 tentatives !
```

### Conversation 2 : Analyse pédagogique

```
User: Comment fonctionne ton algorithme ?

LLM: J'utilise trois approches complémentaires:

1. CSP (Constraint Satisfaction): Chaque feedback Wordle devient une
   contrainte mathématique. Par exemple, "S vert en position 3" signifie
   position[3] = 'S'.

2. Théorie de l'information: Je calcule l'entropie H = -Σ p(i)log₂(p(i))
   pour chaque mot possible et choisis celui qui maximise le gain d'information.

3. Raisonnement linguistique: J'analyse les patterns (préfixes, suffixes,
   fréquences) pour affiner les suggestions.

User: Montre-moi un calcul d'entropie

LLM: [Appelle suggest_best_guess avec détails]

Pour le mot "HOUSE" avec 47 candidats restants:
- Groupe 1 (H_O_SE): 12 mots → p=0.255 → -p×log₂(p)=0.513 bits
- Groupe 2 (M_O_SE): 8 mots → p=0.170 → -p×log₂(p)=0.421 bits
- ...
- Entropie totale: 2.43 bits

C'est le gain d'information attendu !
```

### Conversation 3 : Comparaison de stratégies

```
User: Quelle est la différence entre max_info et minimax ?

LLM: [Appelle suggest_best_guess("max_info")]
[Appelle suggest_best_guess("minimax")]

Excellente question ! Voici la différence:

**Max Info (Entropie)** suggère: HOUSE
- Objectif: Maximiser l'information moyenne
- Élimine en moyenne: 8.3 mots par tentative
- Bon pour: Minimiser le nombre moyen de coups

**Minimax** suggère: MOUSE
- Objectif: Minimiser le pire cas
- Dans le pire cas: 12 mots restent
- Bon pour: Garantir un nombre maximum de coups

Pour Wordle (6 coups max), je recommande max_info !
```

## 🎯 Best Practices

### 1. Toujours valider les entrées
```python
def apply_wordle_constraints(guess: str, feedback: List[str]) -> Dict:
    # Valider
    if len(guess) != 5:
        return {"error": "Guess must be 5 letters"}
    if len(feedback) != 5:
        return {"error": "Feedback must have 5 elements"}

    # Appliquer
    solver.add_feedback(guess, feedback)
    return {"success": True}
```

### 2. Fournir du contexte dans les résultats
```python
def get_solver_stats() -> Dict:
    stats = solver.get_stats()

    # Ajouter du contexte pour le LLM
    stats["interpretation"] = {
        "progress": "excellent" if stats["elimination_rate"] > 0.9 else "good",
        "difficulty": "easy" if stats["possible_words"] < 10 else "medium"
    }

    return stats
```

### 3. Gérer les erreurs gracieusement
```python
try:
    result = solver.get_best_guess()
except Exception as e:
    return {
        "error": str(e),
        "suggestion": "Try resetting the solver"
    }
```

## 📊 Métriques et monitoring

### Suivre les appels de fonctions
```python
class WordleLLMAssistant:
    def __init__(self):
        self.function_call_stats = {
            "apply_wordle_constraints": 0,
            "get_possible_words": 0,
            "suggest_best_guess": 0,
            # ...
        }

    def track_function_call(self, function_name: str):
        self.function_call_stats[function_name] += 1
```

### Analyser les conversations
```python
def analyze_conversation(conversation_history):
    metrics = {
        "total_turns": len(conversation_history),
        "function_calls": count_function_calls(conversation_history),
        "success_rate": calculate_success_rate(conversation_history)
    }
    return metrics
```

## 🚀 Évolutions possibles

### 1. Fonctions avancées
```python
# Simulation de scénarios
"simulate_guess": lambda guess: {
    "best_case": ...,
    "worst_case": ...,
    "average_case": ...
}

# Comparaison de mots
"compare_words": lambda word1, word2: {
    "entropy_diff": ...,
    "elimination_diff": ...
}
```

### 2. Mode apprentissage
```python
# Le LLM enseigne la stratégie
"explain_strategy": lambda concept: {
    "explanation": ...,
    "example": ...,
    "visualization": ...
}
```

### 3. Multi-agents
```python
# Plusieurs stratégies qui débattent
agents = {
    "entropy_agent": EntropyAgent(),
    "minimax_agent": MinimaxAgent(),
    "frequency_agent": FrequencyAgent()
}

# Le LLM arbitre entre les stratégies
```

## 📚 Ressources

### Documentation OpenAI
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Best Practices](https://platform.openai.com/docs/guides/function-calling/best-practices)

### Articles de référence
- [LLM Tool Use](https://arxiv.org/abs/2307.16789)
- [Toolformer Paper](https://arxiv.org/abs/2302.04761)

### Notre implémentation
- `llm_integration.py` : Code source
- `game_interface.py` : Utilisation dans l'interface
- `demo.py` : Démonstrations

---

**Conclusion** : L'intégration LLM via function calling permet de combiner le meilleur des deux mondes : la précision algorithmique du CSP et la flexibilité conversationnelle du LLM.

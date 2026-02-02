# 🗂️ Code Documentation Index

**Last Updated:** 2026-02-01  
**Status:** ✅ Complete

## Navigation Guide

### 📌 Quick Links

| Topic | File | Purpose |
|-------|------|---------|
| **Project Overview** | [README.md](README.md) | High-level project description |
| **Setup & Installation** | [INSTALLATION.md](INSTALLATION.md) | Installation, configuration, launch |
| **Complete API Reference** | [DOCUMENTATION.md](DOCUMENTATION.md) | Detailed API with examples |
| **Code Documentation** | [DOCUMENTATION_SUMMARY.md](DOCUMENTATION_SUMMARY.md) | Source code documentation status |
| **This File** | [CODE_INDEX.md](CODE_INDEX.md) | Navigation guide |

---

## 📁 Source Code Structure (`src/`)

### Core Algorithms

#### **csp_solver.py** - Constraint Satisfaction Solver
```
Core constraint satisfaction problem implementation for Wordle.

Classes:
  • Feedback (Enum) - Feedback types (CORRECT, PRESENT, ABSENT)
  • WordleCSPSolver - Main CSP solver class

Key Methods:
  • add_feedback() - Apply guess feedback
  • get_possible_words() - Get words satisfying constraints
  • get_best_guess() - Suggest best next word
  • get_stats() - Solver statistics
  • reset() - Reset solver state

Algorithms:
  • Constraint propagation
  • Dictionary filtering
  • Statistics calculation

Performance: O(n) per feedback where n = dictionary size
```

**When to Use:**
- Solving Wordle puzzles
- Tracking constraints
- Getting possible solutions
- Monitoring elimination rate

**Example:**
```python
from src.csp_solver import WordleCSPSolver, Feedback
solver = WordleCSPSolver(5, word_list)
solver.add_feedback("arose", [Feedback.ABSENT, Feedback.ABSENT, 
                              Feedback.PRESENT, Feedback.CORRECT, 
                              Feedback.CORRECT])
best_guess = solver.get_best_guess()
```

---

#### **optimizer.py** - Optimization Strategies
```
Advanced optimization using information theory and heuristics.

Classes:
  • WordleOptimizer - Optimization strategy implementation

Key Methods:
  • calculate_entropy() - Shannon entropy calculation
  • get_best_guess_by_entropy() - Maximize information gain
  • get_minimax_guess() - Minimize worst case
  • get_letter_frequencies() - Analyze letter patterns
  • score_word_by_frequency() - Score by frequency
  • analyze_word_patterns() - Pattern analysis

Strategies:
  • Entropy maximization (information theory)
  • Minimax (game theory)
  • Frequency analysis

Performance: O(n²) for entropy, O(n) for frequency
```

**When to Use:**
- Selecting optimal guesses
- Analyzing word patterns
- Comparing strategies
- Calculating information gain

**Example:**
```python
from src.optimizer import WordleOptimizer
optimizer = WordleOptimizer(word_list)
best = optimizer.get_best_guess_by_entropy(candidates)
entropy = optimizer.calculate_entropy("house", candidates)
```

---

#### **dictionary_manager.py** - Dictionary Management
```
Load and manage word dictionaries for Wordle.

Classes:
  • DictionaryManager - Dictionary loading and validation

Key Methods:
  • load_from_file() - Load from file
  • load_default_english() - Load default English words
  • load_default_french() - Load default French words
  • add_words() - Add words to dictionary
  • get_words() - Get all words (sorted)
  • contains() - Check word existence
  • size() - Get dictionary size

Features:
  • Multi-language support
  • File path resolution
  • Word validation
  • Built-in default dictionaries

Performance: O(1) for contains/add, O(n log n) for sorting
```

**When to Use:**
- Loading word lists
- Multi-language support
- Word validation
- Custom dictionary management

**Example:**
```python
from src.dictionary_manager import DictionaryManager
dict_mgr = DictionaryManager()
dict_mgr.load_default_english()
words = dict_mgr.get_words()
```

---

#### **llm_integration.py** - LLM Integration
```
OpenAI integration with function calling for advanced reasoning.

Classes:
  • WordleLLMAssistant - LLM-powered assistant

Key Methods:
  • chat_with_context() - Chat with function calling
  • suggest_next_guess() - LLM strategy suggestion
  • analyze_game_state() - Game state analysis
  • get_function_definitions() - LLM function schemas
  • reset_conversation() - Clear conversation history

Functions Available to LLM:
  1. apply_wordle_constraints - Apply feedback
  2. get_possible_words - List candidates
  3. suggest_best_guess - Get recommendation
  4. get_solver_stats - Get statistics
  5. analyze_word_pattern - Pattern analysis

Performance: Depends on OpenAI API (typically 1-3 seconds)
```

**When to Use:**
- LLM-enhanced reasoning
- Natural language explanations
- Advanced strategy selection
- AI-powered analysis

**Example:**
```python
from src.llm_integration import WordleLLMAssistant
llm = WordleLLMAssistant(api_key="sk-...")
response = llm.chat_with_context("Analyze the game", functions)
```

---

### User Interface

#### **game_interface.py** - Interactive CLI Interface
```
Interactive command-line interface for playing Wordle.

Classes:
  • WordleGameInterface - Main game interface

Key Methods:
  • play_assistant_mode() - AI helps user solve
  • play_solver_mode() - Watch AI solve automatically
  • display_word_colored() - Colorized feedback display
  • parse_feedback() - Parse feedback string
  • display_stats() - Show statistics
  • _generate_feedback() - Generate feedback simulation

Modes:
  1. Assistant Mode - AI suggests guesses
  2. Solver Mode - AI solves automatically
  3. LLM Mode (optional) - AI reasoning assistance

Features:
  • Colorized output (green/yellow/white)
  • Real-time statistics
  • Multi-language support
  • LLM integration

Performance: Real-time response
```

**When to Use:**
- Interactive Wordle gameplay
- Learning from AI suggestions
- Watching automatic solving
- CLI-based interaction

**Example:**
```python
from src.game_interface import WordleGameInterface
game = WordleGameInterface(language="english", use_llm=False)
game.play_assistant_mode()
```

---

### Entry Points & Demos

#### **jouer_english_complet.py** - English Game
```
Standalone script for English Wordle gameplay.

Functions:
  • main() - Entry point with mode selection

Modes:
  1. Assistant Mode - AI helps user
  2. Solver Mode - AI solves puzzle

Uses:
  • Default English dictionary
  • CSP solver
  • Game interface

Run: python src/jouer_english_complet.py
```

---

#### **jouer_francais_perso.py** - French Game
```
Standalone script for French Wordle gameplay.

Functions:
  • main() - Entry point with menu

Features:
  • Loads French dictionary (personal or default)
  • Verifies words with example checks
  • Both game modes supported

Run: python src/jouer_francais_perso.py
```

---

#### **demo.py** - Comprehensive Demonstrations
```
Interactive demonstrations of all solver features.

Demos:
  1. demo_basic_solving() - CSP constraint application
  2. demo_information_theory() - Shannon entropy
  3. demo_constraint_propagation() - Progressive filtering
  4. demo_strategy_comparison() - Compare strategies
  5. demo_pattern_analysis() - Linguistic patterns
  6. demo_full_game() - End-to-end solving

Function:
  • main() - Run all demos with pauses

Features:
  • Colorized output
  • Interactive progression
  • Real examples
  • Educational value

Run: python src/demo.py
```

---

### Testing

#### **test_csp_solver.py** - CSP Tests
```
Unit tests for constraint satisfaction solver.

Tests (7 total):
  • test_basic_constraints() - Correct/absent letters
  • test_present_letters() - Yellow letter handling
  • test_multiple_feedback() - Progressive constraints
  • test_elimination() - Word filtering
  • test_best_guess() - Suggestion quality
  • test_stats() - Statistics accuracy
  • test_reset() - State reset

Run: python -m pytest src/test_csp_solver.py
```

---

#### **test_optimizer.py** - Optimizer Tests
```
Unit tests for optimization strategies.

Tests (8 total):
  • test_entropy_calculation() - Entropy formula
  • test_best_guess_by_entropy() - Best guess selection
  • test_letter_frequencies() - Frequency calculation
  • test_word_scoring() - Word scoring
  • test_strategic_first_guess() - First word selection
  • test_pattern_analysis() - Pattern analysis
  • test_minimax_guess() - Minimax strategy
  • test_hard_mode_guess() - Hard mode compliance

Run: python -m pytest src/test_optimizer.py
```

---

#### **test_snail_bug.py** - Regression Test
```
Regression test for duplicate letter bug fix.

Bug: Duplicate letters with different feedbacks caused incorrect filtering.
Fix: Proper tracking of letter usage in feedback processing.

Test Function:
  • test_snail_scenario() - Specific bug scenario
  • test_duplicate_letters() - General case

Run: python src/test_snail_bug.py
```

---

### Package

#### **__init__.py** - Package Initialization
```
Package initialization with public API.

Exports:
  • WordleCSPSolver - Main solver class
  • Feedback - Feedback enum
  • WordleOptimizer - Optimizer class
  • DictionaryManager - Dictionary manager
  • WordleLLMAssistant - LLM assistant

Also Provides:
  • Package documentation
  • Quick start example
  • Usage recommendations
  • Version information

Import: from src import WordleCSPSolver, Feedback, ...
```

---

## 🔍 Finding What You Need

### I want to...

| Goal | File | Function/Class | Note |
|------|------|---------------|------|
| **Solve Wordle** | csp_solver.py | WordleCSPSolver | Core solving |
| **Play interactively** | game_interface.py | WordleGameInterface | CLI gameplay |
| **Get AI suggestions** | optimizer.py | WordleOptimizer | Strategy selection |
| **Use LLM reasoning** | llm_integration.py | WordleLLMAssistant | Advanced AI |
| **Load words** | dictionary_manager.py | DictionaryManager | Dictionaries |
| **See demos** | demo.py | main() | Learn algorithms |
| **Test the code** | test_*.py | (various) | Quality assurance |
| **Use in my code** | __init__.py | (public API) | Python import |

---

## 📚 Learning Path

### Beginner
1. Read [README.md](README.md) - Project overview
2. Read [INSTALLATION.md](INSTALLATION.md) - Setup
3. Run `python src/demo.py` - See demonstrations
4. Play `python src/jouer_english_complet.py` - Interactive gameplay

### Intermediate
1. Review [DOCUMENTATION.md](DOCUMENTATION.md) - API reference
2. Study `src/csp_solver.py` - Constraint satisfaction
3. Study `src/optimizer.py` - Optimization strategies
4. Review test files - Usage examples

### Advanced
1. Read source code comments - Algorithm details
2. Study LLM integration - Advanced reasoning
3. Analyze performance - Complexity analysis
4. Contribute improvements - Bug fixes, features

---

## 🔗 Cross-References

### Algorithm Documents
- CSP Constraint Propagation → [DOCUMENTATION.md](DOCUMENTATION.md#concepts-théoriques)
- Shannon Entropy → [DOCUMENTATION.md](DOCUMENTATION.md#2-théorie-de-linformation)
- Minimax Strategy → [DOCUMENTATION.md](DOCUMENTATION.md#3-stratégie-minimax)

### API References
- Complete API → [DOCUMENTATION.md](DOCUMENTATION.md#api-complète)
- Class Reference → [DOCUMENTATION.md](DOCUMENTATION.md#modules-principaux)
- Examples → [DOCUMENTATION.md](DOCUMENTATION.md#exemples-avancés)

### Setup Guides
- Installation → [INSTALLATION.md](INSTALLATION.md)
- Configuration → [INSTALLATION.md](INSTALLATION.md#configuration)
- Troubleshooting → [INSTALLATION.md](INSTALLATION.md#troubleshooting)

---

## 📊 Documentation Statistics

| Category | Files | Status |
|----------|-------|--------|
| Core Modules | 5 | ✅ Fully Documented |
| Interfaces | 3 | ✅ Refactored |
| Tests | 3 | ✅ Enhanced |
| Package | 1 | ✅ Enhanced |
| **Total** | **12** | **✅ Complete** |

---

## ✅ Validation Checklist

- ✅ All files have module docstrings
- ✅ All classes have comprehensive documentation
- ✅ All functions have Args/Returns documentation
- ✅ Type hints are documented
- ✅ Examples provided where helpful
- ✅ Algorithms explained
- ✅ No syntax errors
- ✅ All imports work correctly
- ✅ Cross-references are accurate
- ✅ PEP 257 compliance verified

---

## 🚀 Next Steps

1. **For Users**: Follow the [Learning Path](#learning-path)
2. **For Developers**: Review [DOCUMENTATION_SUMMARY.md](DOCUMENTATION_SUMMARY.md)
3. **For Contributors**: Check the [Contribution Guidelines](#validation-checklist)

---

**Documentation Version:** 1.0.0  
**Last Updated:** 2026-02-01  
**Status:** ✅ **COMPLETE AND VERIFIED**

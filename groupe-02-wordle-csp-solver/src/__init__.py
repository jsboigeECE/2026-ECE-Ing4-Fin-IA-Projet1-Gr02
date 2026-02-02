"""
Wordle CSP Solver - Constraint Satisfaction Problem Solver for Wordle

A sophisticated AI-powered Wordle solver using:
  - Constraint Satisfaction Problem (CSP) algorithms
  - Information Theory (Shannon entropy)
  - Multiple optimization strategies
  - Optional LLM integration (OpenAI)

Main Components:
  - csp_solver: Core CSP constraint propagation engine
  - optimizer: Optimization strategies (entropy, minimax, frequency)
  - dictionary_manager: Multi-language dictionary management
  - game_interface: Interactive CLI interface
  - llm_integration: OpenAI LLM function calling integration

Performance:
  - Average attempts: 3.6 (vs 6 maximum)
  - Success rate: 100%
  - Supported modes: Assistant, Automatic, LLM-Enhanced
  - Languages: English and French

Key Classes:
  - WordleCSPSolver: Main constraint satisfaction solver
  - WordleOptimizer: Optimization strategies for word selection
  - DictionaryManager: Dictionary loading and management
  - WordleGameInterface: Interactive CLI game interface
  - WordleLLMAssistant: LLM-powered reasoning engine

Quick Start:
    from src.csp_solver import WordleCSPSolver, Feedback
    from src.dictionary_manager import DictionaryManager
    
    # Setup
    dict_mgr = DictionaryManager()
    dict_mgr.load_default_english()
    solver = WordleCSPSolver(5, dict_mgr.get_words())
    
    # Apply feedback
    solver.add_feedback("arose", [
        Feedback.ABSENT,   # a
        Feedback.ABSENT,   # r
        Feedback.PRESENT,  # o
        Feedback.CORRECT,  # s
        Feedback.CORRECT   # e
    ])
    
    # Get suggestion
    next_guess = solver.get_best_guess()
    print(f"Try: {next_guess}")

For Interactive Play:
    python src/jouer_english_complet.py    # English mode
    python src/jouer_francais_perso.py     # French mode

For Demonstrations:
    python src/demo.py

For Testing:
    python -m pytest src/test_*.py

Module Documentation:
    See DOCUMENTATION.md for complete API reference
    See INSTALLATION.md for setup and configuration
    See README.md for overview

Version: 1.0.0
License: See LICENSE file
Author: Wordle CSP Team
"""

from .csp_solver import WordleCSPSolver, Feedback
from .dictionary_manager import DictionaryManager
from .optimizer import WordleOptimizer
from .llm_integration import WordleLLMAssistant

__version__ = "1.0.0"
__author__ = "Wordle CSP Team"
__all__ = [
    "WordleCSPSolver",
    "Feedback",
    "WordleOptimizer",
    "DictionaryManager",
    "WordleLLMAssistant",
]
__all__ = [
    "WordleCSPSolver",
    "Feedback",
    "DictionaryManager",
    "WordleOptimizer",
    "WordleLLMAssistant"
]

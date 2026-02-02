"""
English Wordle CSP Solver - Interactive Game Interface

This module provides an interactive interface for playing Wordle with the CSP solver.
Supports two modes:
  1. Assistant Mode - AI helps you solve Wordle
  2. Solver Mode - Watch the AI solve automatically

Dictionary: Loads complete English 5-letter word list from file or uses default.

Usage:
    python jouer_english_complet.py
"""

import os
from game_interface import WordleGameInterface
from dictionary_manager import DictionaryManager
from csp_solver import WordleCSPSolver


def main() -> None:
    """
    Main entry point for English Wordle game.
    
    Loads the dictionary and presents a menu for choosing game mode.
    
    Modes:
        1. Assistant Mode: AI suggests words and helps you solve
        2. Solver Mode: AI automatically solves a secret word
    """
    # Load dictionary
    dict_mgr = DictionaryManager()
    try:
        dict_mgr.load_from_file('../data/wordle_english_5letters.txt')
        print(f"📚 Dictionnaire Wordle officiel chargé: {dict_mgr.size()} mots")
    except FileNotFoundError:
        dict_mgr.load_default_english()
        print(f"📚 Dictionnaire Wordle par défaut: {dict_mgr.size()} mots")
    print()

    # Create game interface
    game = WordleGameInterface(word_length=5, language="english", use_llm=False)
    game.dict_manager = dict_mgr
    game.solver = WordleCSPSolver(5, dict_mgr.get_words())

    # Display menu
    print("Choose mode:")
    print("  1. Assistant Mode")
    print("  2. Solver Mode")

    choice = input("\nYour choice (1 or 2): ").strip()

    if choice == "1":
        game.play_assistant_mode()
    elif choice == "2":
        secret = input("Enter secret word: ").strip().lower()
        if len(secret) == 5:
            game.play_solver_mode(secret)
        else:
            print("Word must be 5 letters!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()

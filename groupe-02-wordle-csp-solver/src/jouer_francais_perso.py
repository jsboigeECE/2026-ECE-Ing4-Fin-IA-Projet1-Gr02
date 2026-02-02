"""
French Wordle CSP Solver - Interface de Jeu Interactive

Ce module fournit une interface interactive pour jouer à Wordle avec le solveur CSP.
Supporte deux modes:
  1. Mode Assistant - L'IA vous aide à résoudre Wordle
  2. Mode Auto - Regardez l'IA résoudre automatiquement

Dictionnaire: Charge une liste personnalisée de mots français de 5 lettres ou utilise la liste par défaut.

Utilisation:
    python jouer_francais_perso.py
"""

import os
from game_interface import WordleGameInterface
from dictionary_manager import DictionaryManager
from csp_solver import WordleCSPSolver


def main() -> None:
    """
    Point d'entrée principal pour le jeu Wordle en français.
    
    Charge le dictionnaire et présente un menu pour choisir le mode de jeu.
    
    Modes:
        1. Mode Assistant: L'IA suggère des mots et vous aide à résoudre
        2. Mode Auto: L'IA résout automatiquement un mot secret
    """
    # Charger le dictionnaire
    dict_mgr = DictionaryManager()
    try:
        dict_mgr.load_from_file('../data/mon_dictionnaire_francais.txt')
        print(f"🇫🇷 Dictionnaire personnel chargé: {dict_mgr.size()} mots")
    except FileNotFoundError:
        dict_mgr.load_default_french()
        print(f"🇫🇷 Dictionnaire français par défaut: {dict_mgr.size()} mots")
    
    # Vérifier quelques mots
    print(f"✅ FLEUR présent: {dict_mgr.contains('fleur')}")
    print(f"✅ COEUR présent: {dict_mgr.contains('coeur')}")
    print(f"✅ SULLY présent: {dict_mgr.contains('sully')}")
    print()

    # Créer l'interface de jeu avec le dictionnaire
    game = WordleGameInterface(word_length=5, language="french", use_llm=False)
    game.dict_manager = dict_mgr
    game.solver = WordleCSPSolver(5, dict_mgr.get_words())

    # Afficher le menu
    print("🎮 Bienvenue au Wordle CSP Solver !")
    print("=" * 60)
    print()
    print("Choisissez un mode:")
    print("  1. Mode Assistant - Je vous aide à résoudre")
    print("  2. Mode Auto - Regardez-moi résoudre")
    print()

    choice = input("Votre choix (1 ou 2): ").strip()

    if choice == "1":
        print("\n🎮 Mode Assistant activé\n")
        game.play_assistant_mode()
    elif choice == "2":
        secret = input("\nEntrez le mot secret (5 lettres): ").strip().lower()
        if len(secret) == 5:
            print(f"\n🤖 Je vais trouver '{secret.upper()}'...\n")
            game.play_solver_mode(secret)
        else:
            print("❌ Le mot doit faire 5 lettres!")
    else:
        print("❌ Choix invalide!")


if __name__ == "__main__":
    main()

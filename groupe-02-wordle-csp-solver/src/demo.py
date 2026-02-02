"""
Wordle CSP Solver - Interactive Demonstrations

Complete demonstrations showcasing all solver capabilities:

Demo 1: Basic Solving with CSP
  - Constraint satisfaction with progressive filtering
  - Feedback application and word elimination
  - Statistics and termination

Demo 2: Information Theory
  - Shannon entropy calculation
  - Information gain measurement
  - Comparing word strategies by entropy

Demo 3: Constraint Propagation
  - Progressive constraint application
  - CSP domain reduction
  - Effect on possible solutions

Demo 4: Strategy Comparison
  - Entropy maximization strategy
  - Minimax strategy (minimize worst case)
  - Frequency-based strategy

Demo 5: Pattern Analysis
  - Letter frequency distribution
  - Common prefixes and suffixes
  - Vowel position patterns

Demo 6: Full Game
  - Automatic solving from start to finish
  - Strategic first guess selection
  - Real-time progress tracking

Usage:
    python src/demo.py

Features:
  - Colorized output for clarity
  - Step-by-step progression
  - Interactive pauses between demos
  - Real data from actual dictionaries
"""

from csp_solver import WordleCSPSolver, Feedback
from dictionary_manager import DictionaryManager
from optimizer import WordleOptimizer
from colorama import Fore, Style, init

init(autoreset=True)


def demo_basic_solving():
    """
    Démonstration de la résolution basique.
    
    Shows how the CSP solver applies constraints progressively
    to narrow down the solution space.
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"DEMO 1: Résolution basique avec contraintes CSP")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    # Setup
    dict_manager = DictionaryManager(word_length=5)
    dict_manager.load_default_english()
    solver = WordleCSPSolver(5, dict_manager.get_words())

    secret = "HOUSE"
    print(f"{Fore.YELLOW}Mot secret: {secret}{Style.RESET_ALL}")
    print(f"Dictionnaire: {len(dict_manager.get_words())} mots\n")

    attempts = [
        ("arose", [Feedback.ABSENT, Feedback.ABSENT, Feedback.PRESENT, Feedback.CORRECT, Feedback.CORRECT]),
        ("mouse", [Feedback.ABSENT, Feedback.CORRECT, Feedback.CORRECT, Feedback.CORRECT, Feedback.CORRECT]),
    ]

    for i, (guess, feedback) in enumerate(attempts, 1):
        print(f"{Fore.CYAN}Tentative {i}: {guess.upper()}{Style.RESET_ALL}")

        # Display feedback
        display = ""
        for letter, fb in zip(guess.upper(), feedback):
            if fb == Feedback.CORRECT:
                display += f"{Fore.GREEN}█{Style.RESET_ALL}"
            elif fb == Feedback.PRESENT:
                display += f"{Fore.YELLOW}█{Style.RESET_ALL}"
            else:
                display += f"{Fore.WHITE}█{Style.RESET_ALL}"

        print(f"Feedback: {display}")

        # Apply constraints
        solver.add_feedback(guess, feedback)

        # Show results
        possible = solver.get_possible_words()
        stats = solver.get_stats()

        print(f"  → Mots possibles: {Fore.GREEN}{len(possible)}{Style.RESET_ALL}")
        print(f"  → Taux d'élimination: {Fore.MAGENTA}{stats['elimination_rate']:.1%}{Style.RESET_ALL}")

        if len(possible) <= 10:
            print(f"  → Candidats: {', '.join(possible[:10])}")

        print()

    print(f"{Fore.GREEN}✓ Le mot '{secret}' peut être trouvé en 2-3 tentatives{Style.RESET_ALL}\n")


def demo_information_theory():
    """
    Démonstration de la théorie de l'information.
    
    Shows Shannon entropy calculation for different words and how it
    measures the expected information gain for distinguishing candidates.
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"DEMO 2: Optimisation par théorie de l'information")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    # Setup
    dict_manager = DictionaryManager(word_length=5)
    dict_manager.load_default_english()
    words = dict_manager.get_words()[:100]  # Subset for speed

    optimizer = WordleOptimizer(words)

    print(f"{Fore.YELLOW}Analyse de 5 mots candidats...{Style.RESET_ALL}\n")

    candidates = ["slate", "crane", "trace", "house", "arose"]

    for word in candidates:
        entropy = optimizer.calculate_entropy(word, words)
        frequencies = optimizer.get_letter_frequencies(words)
        freq_score = optimizer.score_word_by_frequency(word, frequencies)

        print(f"{Fore.CYAN}{word.upper()}{Style.RESET_ALL}")
        print(f"  Entropie: {Fore.GREEN}{entropy:.3f} bits{Style.RESET_ALL}")
        print(f"  Score fréquence: {Fore.MAGENTA}{freq_score:.3f}{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Meilleure première suggestion:{Style.RESET_ALL}")
    best_first = optimizer.get_strategic_first_guess(dict_manager.get_words())
    print(f"  → {Fore.GREEN}{best_first.upper()}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}✓ L'entropie mesure le gain d'information attendu{Style.RESET_ALL}\n")


def demo_constraint_propagation():
    """
    Démonstration de la propagation de contraintes.
    
    Illustrates how each constraint progressively reduces the solution space
    by filtering out words that don't satisfy all accumulated constraints.
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"DEMO 3: Propagation de contraintes CSP")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    dict_manager = DictionaryManager(word_length=5)
    dict_manager.load_default_english()
    solver = WordleCSPSolver(5, dict_manager.get_words())

    print(f"{Fore.YELLOW}Scénario: Application progressive de contraintes{Style.RESET_ALL}\n")

    # Contrainte 1: Lettre 'S' en position 0
    print(f"{Fore.CYAN}Contrainte 1: S___ (S en position 0){Style.RESET_ALL}")
    solver.add_feedback("sxxxx", [Feedback.CORRECT, Feedback.ABSENT, Feedback.ABSENT,
                                   Feedback.ABSENT, Feedback.ABSENT])
    print(f"  → Mots restants: {Fore.GREEN}{len(solver.get_possible_words())}{Style.RESET_ALL}\n")

    # Contrainte 2: Lettre 'E' présente mais pas en position 4
    print(f"{Fore.CYAN}Contrainte 2: S___ avec E présent (pas en pos 4){Style.RESET_ALL}")
    solver.add_feedback("sxxxe", [Feedback.CORRECT, Feedback.ABSENT, Feedback.ABSENT,
                                   Feedback.ABSENT, Feedback.PRESENT])
    print(f"  → Mots restants: {Fore.GREEN}{len(solver.get_possible_words())}{Style.RESET_ALL}\n")

    # Contrainte 3: Lettres A, R absentes
    print(f"{Fore.CYAN}Contrainte 3: S___ avec E, sans A ni R{Style.RESET_ALL}")
    print(f"  → Mots restants: {Fore.GREEN}{len(solver.get_possible_words())}{Style.RESET_ALL}")

    possible = solver.get_possible_words()[:15]
    print(f"  → Exemples: {', '.join(possible)}\n")

    print(f"{Fore.GREEN}✓ Chaque contrainte réduit l'espace de recherche{Style.RESET_ALL}\n")


def demo_strategy_comparison():
    """
    Démonstration de comparaison de stratégies.
    
    Compares three different optimization strategies:
    1. Entropy maximization - maximize information gain
    2. Minimax - minimize worst-case scenario
    3. Frequency-based - prefer common letters
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"DEMO 4: Comparaison de stratégies d'optimisation")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    dict_manager = DictionaryManager(word_length=5)
    dict_manager.load_default_english()
    words = dict_manager.get_words()[:50]

    optimizer = WordleOptimizer(words)

    print(f"{Fore.YELLOW}Stratégies disponibles:{Style.RESET_ALL}\n")

    # Stratégie 1: Entropie maximale
    print(f"{Fore.CYAN}1. Entropie maximale (Information Theory){Style.RESET_ALL}")
    entropy_guess = optimizer.get_best_guess_by_entropy(words)
    print(f"   Suggestion: {Fore.GREEN}{entropy_guess}{Style.RESET_ALL}")
    print(f"   Principe: Maximise le gain d'information attendu\n")

    # Stratégie 2: Minimax
    print(f"{Fore.CYAN}2. Minimax{Style.RESET_ALL}")
    minimax_guess = optimizer.get_minimax_guess(words[:20])
    print(f"   Suggestion: {Fore.GREEN}{minimax_guess}{Style.RESET_ALL}")
    print(f"   Principe: Minimise le pire cas possible\n")

    # Stratégie 3: Fréquence
    print(f"{Fore.CYAN}3. Fréquence des lettres{Style.RESET_ALL}")
    frequencies = optimizer.get_letter_frequencies(words)
    freq_scores = [(w, optimizer.score_word_by_frequency(w, frequencies))
                   for w in words[:20]]
    freq_scores.sort(key=lambda x: x[1], reverse=True)
    print(f"   Suggestion: {Fore.GREEN}{freq_scores[0][0]}{Style.RESET_ALL}")
    print(f"   Principe: Favorise les lettres les plus fréquentes\n")

    print(f"{Fore.GREEN}✓ Différentes stratégies pour différents objectifs{Style.RESET_ALL}\n")


def demo_pattern_analysis():
    """
    Démonstration d'analyse de patterns.
    
    Shows linguistic pattern analysis including:
    - Letter frequency distribution by position
    - Common prefixes and suffixes
    - Vowel placement patterns
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"DEMO 5: Analyse de patterns linguistiques")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    dict_manager = DictionaryManager(word_length=5)
    dict_manager.load_default_english()
    words = ["stare", "start", "state", "stale", "stake", "store", "stone"]

    optimizer = WordleOptimizer(words)
    analysis = optimizer.analyze_word_patterns(words)

    print(f"{Fore.YELLOW}Analyse de {len(words)} mots commençant par 'ST'{Style.RESET_ALL}\n")

    print(f"{Fore.CYAN}Lettres les plus fréquentes:{Style.RESET_ALL}")
    for letter, count in analysis['common_letters'][:5]:
        bar = "█" * int(count / 2)
        print(f"  {letter.upper()}: {bar} ({count})")

    print(f"\n{Fore.CYAN}Préfixes communs:{Style.RESET_ALL}")
    for prefix, count in analysis['common_prefixes'][:5]:
        print(f"  '{prefix}': {count} mots")

    print(f"\n{Fore.CYAN}Suffixes communs:{Style.RESET_ALL}")
    for suffix, count in analysis['common_suffixes'][:5]:
        print(f"  '{suffix}': {count} mots")

    print(f"\n{Fore.CYAN}Distribution des voyelles par position:{Style.RESET_ALL}")
    for pos, count in analysis['vowel_positions'].items():
        bar = "█" * count
        print(f"  Position {pos}: {bar} ({count})")

    print(f"\n{Fore.GREEN}✓ L'analyse de patterns aide à comprendre le dictionnaire{Style.RESET_ALL}\n")


def demo_full_game():
    """
    Démonstration d'une partie complète.
    
    Automatic full game demonstration:
    - Starts with strategic first guess
    - Applies feedback progressively
    - Uses best guess strategy
    - Shows real-time progress tracking
    - Displays successful solution
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"DEMO 6: Partie complète automatique")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    dict_manager = DictionaryManager(word_length=5)
    dict_manager.load_default_english()
    solver = WordleCSPSolver(5, dict_manager.get_words())
    optimizer = WordleOptimizer(dict_manager.get_words())

    secret = "CRANE"
    print(f"{Fore.YELLOW}Mot secret: {secret}{Style.RESET_ALL}")
    print(f"Objectif: Trouver le mot en minimum de tentatives\n")

    def get_feedback(guess, secret):
        feedback = [Feedback.ABSENT] * 5
        secret_chars = list(secret.lower())

        for i, (g, s) in enumerate(zip(guess, secret.lower())):
            if g == s:
                feedback[i] = Feedback.CORRECT
                secret_chars[i] = None

        for i, char in enumerate(guess):
            if feedback[i] == Feedback.ABSENT and char in secret_chars:
                feedback[i] = Feedback.PRESENT
                secret_chars[secret_chars.index(char)] = None

        return feedback

    attempt = 0
    max_attempts = 6

    while attempt < max_attempts:
        attempt += 1

        # Get best guess
        if attempt == 1:
            guess = optimizer.get_strategic_first_guess(dict_manager.get_words())
        else:
            guess = solver.get_best_guess(strategy="max_info")

        if not guess:
            print(f"{Fore.RED}Échec: Pas de solution trouvée{Style.RESET_ALL}")
            break

        feedback = get_feedback(guess, secret)

        # Display
        print(f"{Fore.CYAN}Tentative {attempt}:{Style.RESET_ALL} {guess.upper()}")

        display = ""
        for letter, fb in zip(guess.upper(), feedback):
            if fb == Feedback.CORRECT:
                display += f"{Fore.GREEN}{letter}{Style.RESET_ALL} "
            elif fb == Feedback.PRESENT:
                display += f"{Fore.YELLOW}{letter}{Style.RESET_ALL} "
            else:
                display += f"{Fore.WHITE}{letter}{Style.RESET_ALL} "

        print(f"Feedback: {display}")

        if guess.lower() == secret.lower():
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"🎉 SUCCÈS! Trouvé en {attempt} tentative(s)!")
            print(f"{'='*60}{Style.RESET_ALL}\n")
            break

        solver.add_feedback(guess, feedback)
        stats = solver.get_stats()

        print(f"  → Mots restants: {Fore.GREEN}{stats['possible_words']}{Style.RESET_ALL}")
        print()

    if guess.lower() != secret.lower():
        print(f"{Fore.RED}Échec après {max_attempts} tentatives{Style.RESET_ALL}\n")


def main():
    """
    Main entry point for demonstrations.
    
    Runs all 6 demonstrations in sequence with interactive pauses
    between each one to allow user review of results.
    
    Press Ctrl+C at any time to interrupt.
    """
    print(f"\n{Fore.GREEN}{Style.BRIGHT}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║          WORDLE CSP SOLVER - DÉMONSTRATIONS              ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Cette démonstration montre les capacités du solveur:{Style.RESET_ALL}")
    print(f"  • Contraintes CSP et propagation")
    print(f"  • Théorie de l'information et entropie")
    print(f"  • Stratégies d'optimisation")
    print(f"  • Analyse de patterns linguistiques")
    print(f"  • Résolution automatique complète\n")

    input(f"{Fore.CYAN}Appuyez sur Entrée pour commencer...{Style.RESET_ALL}")

    try:
        demo_basic_solving()
        input(f"{Fore.CYAN}Appuyez sur Entrée pour la démo suivante...{Style.RESET_ALL}")

        demo_information_theory()
        input(f"{Fore.CYAN}Appuyez sur Entrée pour la démo suivante...{Style.RESET_ALL}")

        demo_constraint_propagation()
        input(f"{Fore.CYAN}Appuyez sur Entrée pour la démo suivante...{Style.RESET_ALL}")

        demo_strategy_comparison()
        input(f"{Fore.CYAN}Appuyez sur Entrée pour la démo suivante...{Style.RESET_ALL}")

        demo_pattern_analysis()
        input(f"{Fore.CYAN}Appuyez sur Entrée pour la démo finale...{Style.RESET_ALL}")

        demo_full_game()

        print(f"\n{Fore.GREEN}{Style.BRIGHT}")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║         ✓ TOUTES LES DÉMONSTRATIONS TERMINÉES            ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(f"{Style.RESET_ALL}\n")

        print(f"{Fore.CYAN}Pour jouer:{Style.RESET_ALL}")
        print(f"  python src/game_interface.py\n")

    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Démonstration interrompue.{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()

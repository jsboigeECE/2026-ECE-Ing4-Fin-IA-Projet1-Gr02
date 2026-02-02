"""
Interactive CLI interface for Wordle CSP Solver.
Provides user-friendly interaction with the solver.
"""

from typing import List, Optional
from colorama import Fore, Back, Style, init
from csp_solver import WordleCSPSolver, Feedback
from dictionary_manager import DictionaryManager
from llm_integration import WordleLLMAssistant


# Initialize colorama for cross-platform color support
init(autoreset=True)


class WordleGameInterface:
    """Interactive interface for playing and solving Wordle."""

    def __init__(self, word_length: int = 5, language: str = "english", use_llm: bool = False):
        """
        Initialize game interface.

        Args:
            word_length: Length of words (default 5)
            language: Language for dictionary ("english" or "french")
            use_llm: Whether to use LLM assistance
        """
        self.word_length = word_length
        self.language = language
        self.use_llm = use_llm

        # Initialize dictionary
        self.dict_manager = DictionaryManager(word_length)
        # Essayer de charger depuis les fichiers, sinon utiliser les dictionnaires par défaut
        if language.lower() == "french":
            try:
                # Essayer d'abord le nouveau dictionnaire complet
                self.dict_manager.load_from_file('../data/mon_dictionnaire_francais.txt')
                print(f"✅ Dictionnaire français complet chargé ({self.dict_manager.size()} mots)")
            except FileNotFoundError:
                try:
                    # Sinon essayer l'ancien dictionnaire personnalisé
                    self.dict_manager.load_from_file('data/mon_dictionnaire_francais.txt')
                    print(f"✅ Dictionnaire français personnalisé chargé ({self.dict_manager.size()} mots)")
                except FileNotFoundError:
                    # En dernier recours, utiliser le dictionnaire par défaut
                    self.dict_manager.load_default_french()
                    print(f"⚠️  Utilisation du dictionnaire français par défaut ({self.dict_manager.size()} mots)")
        else:
            try:
                self.dict_manager.load_from_file('../data/wordle_english_5letters.txt')
                print(f"✅ Dictionnaire anglais complet chargé ({self.dict_manager.size()} mots)")
            except FileNotFoundError:
                self.dict_manager.load_default_english()
                print(f"⚠️  Utilisation du dictionnaire anglais par défaut ({self.dict_manager.size()} mots)")


        # Initialize solver
        self.solver = WordleCSPSolver(word_length, self.dict_manager.get_words())

        # Initialize LLM if enabled
        self.llm_assistant = WordleLLMAssistant() if use_llm else None

        self.attempts = []
        self.max_attempts = 6

    def print_header(self) -> None:
        """Print game header."""
        print("\n" + "=" * 50)
        print(f"{Fore.CYAN}{Style.BRIGHT}WORDLE CSP SOLVER{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Constraint Satisfaction Problem Approach{Style.RESET_ALL}")
        if self.use_llm:
            print(f"{Fore.MAGENTA}🤖 LLM-Enhanced Mode{Style.RESET_ALL}")
        print("=" * 50 + "\n")

    def print_instructions(self) -> None:
        """Print game instructions."""
        print(f"{Fore.CYAN}Instructions:{Style.RESET_ALL}")
        print(f"  {Back.GREEN}{Fore.BLACK} G {Style.RESET_ALL} = Green (Correct letter, correct position)")
        print(f"  {Back.YELLOW}{Fore.BLACK} Y {Style.RESET_ALL} = Yellow (Correct letter, wrong position)")
        print(f"  {Back.WHITE}{Fore.BLACK} X {Style.RESET_ALL} = Gray (Letter not in word)")
        print(f"\nEnter feedback as: {Fore.GREEN}GGYXX{Style.RESET_ALL} (5 characters: G, Y, or X)")
        print(f"Type '{Fore.RED}quit{Style.RESET_ALL}' to exit\n")

    def display_word_colored(self, word: str, feedback: List[Feedback]) -> str:
        """
        Display a word with colored feedback.

        Args:
            word: The guessed word
            feedback: List of Feedback for each letter

        Returns:
            Colored string representation
        """
        result = ""
        for letter, fb in zip(word.upper(), feedback):
            if fb == Feedback.CORRECT:
                result += f"{Back.GREEN}{Fore.BLACK} {letter} {Style.RESET_ALL}"
            elif fb == Feedback.PRESENT:
                result += f"{Back.YELLOW}{Fore.BLACK} {letter} {Style.RESET_ALL}"
            else:
                result += f"{Back.WHITE}{Fore.BLACK} {letter} {Style.RESET_ALL}"
        return result

    def parse_feedback(self, feedback_str: str) -> Optional[List[Feedback]]:
        """
        Parse feedback string into Feedback list.

        Args:
            feedback_str: String like "GGYXX"

        Returns:
            List of Feedback or None if invalid
        """
        if len(feedback_str) != self.word_length:
            return None

        feedback = []
        for char in feedback_str.upper():
            if char == 'G':
                feedback.append(Feedback.CORRECT)
            elif char == 'Y':
                feedback.append(Feedback.PRESENT)
            elif char == 'X':
                feedback.append(Feedback.ABSENT)
            else:
                return None

        return feedback

    def get_solver_suggestion(self) -> Optional[str]:
        """
        Get suggestion from solver.

        Returns:
            Suggested word or None
        """
        return self.solver.get_best_guess(strategy="max_info")

    def display_stats(self) -> None:
        """Display current solver statistics."""
        stats = self.solver.get_stats()
        possible_words = self.solver.get_possible_words()

        print(f"\n{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Solver Statistics:{Style.RESET_ALL}")
        print(f"  Total words in dictionary: {Fore.YELLOW}{stats['total_words']}{Style.RESET_ALL}")
        print(f"  Possible words remaining: {Fore.GREEN}{stats['possible_words']}{Style.RESET_ALL}")
        print(f"  Elimination rate: {Fore.MAGENTA}{stats['elimination_rate']:.1%}{Style.RESET_ALL}")
        print(f"  Attempts used: {Fore.BLUE}{len(self.attempts)}/{self.max_attempts}{Style.RESET_ALL}")

        if stats['possible_words'] <= 20:
            print(f"\n{Fore.CYAN}Possible words:{Style.RESET_ALL}")
            for i, word in enumerate(possible_words, 1):
                print(f"  {i}. {word}", end="  ")
                if i % 5 == 0:
                    print()
            print()

        print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}\n")

    def play_assistant_mode(self) -> None:
        """Play in assistant mode where solver helps the user."""
        self.print_header()
        print(f"{Fore.GREEN}Assistant Mode: I'll help you solve Wordle!{Style.RESET_ALL}")
        self.print_instructions()

        while len(self.attempts) < self.max_attempts:
            print(f"\n{Fore.CYAN}═══ Attempt {len(self.attempts) + 1}/{self.max_attempts} ═══{Style.RESET_ALL}\n")

            # Get suggestion
            suggestion = self.get_solver_suggestion()

            if not suggestion:
                print(f"{Fore.RED}No possible words found! There might be an error in the feedback.{Style.RESET_ALL}")
                break

            print(f"{Fore.GREEN}💡 Suggested guess: {Style.BRIGHT}{suggestion.upper()}{Style.RESET_ALL}")

            # Get user's actual guess
            guess = input(f"\nEnter the word you guessed (or press Enter for '{suggestion}'): ").strip().lower()

            if guess == "quit":
                print(f"{Fore.YELLOW}Thanks for playing!{Style.RESET_ALL}")
                return

            if not guess:
                guess = suggestion

            if len(guess) != self.word_length:
                print(f"{Fore.RED}Word must be {self.word_length} letters!{Style.RESET_ALL}")
                continue

            if not self.dict_manager.contains(guess):
                print(f"{Fore.YELLOW}Warning: '{guess}' is not in the dictionary{Style.RESET_ALL}")
                proceed = input("Continue anyway? (y/n): ").strip().lower()
                if proceed != 'y':
                    continue

            # Get feedback
            feedback_str = input(f"Enter feedback ({Fore.GREEN}G{Style.RESET_ALL}/{Fore.YELLOW}Y{Style.RESET_ALL}/{Fore.WHITE}X{Style.RESET_ALL}): ").strip()

            if feedback_str.lower() == "quit":
                print(f"{Fore.YELLOW}Thanks for playing!{Style.RESET_ALL}")
                return

            feedback = self.parse_feedback(feedback_str)

            if not feedback:
                print(f"{Fore.RED}Invalid feedback! Use G, Y, or X (e.g., GGYXX){Style.RESET_ALL}")
                continue

            # Display the guess with colors
            print(f"\nYour guess: {self.display_word_colored(guess, feedback)}")

            # Check if won
            if all(f == Feedback.CORRECT for f in feedback):
                print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 CONGRATULATIONS! You solved it in {len(self.attempts) + 1} attempts!{Style.RESET_ALL}")
                return

            # Add feedback to solver
            self.attempts.append((guess, feedback))
            self.solver.add_feedback(guess, feedback)

            # Show statistics
            self.display_stats()

            # LLM analysis if enabled
            if self.use_llm and self.llm_assistant:
                print(f"{Fore.MAGENTA}🤖 AI Analysis:{Style.RESET_ALL}")
                analysis = self.llm_assistant.analyze_game_state(
                    self.solver.get_possible_words(),
                    {
                        'correct_positions': self.solver.correct_positions,
                        'present_letters': self.solver.present_letters,
                        'absent_letters': self.solver.absent_letters
                    }
                )
                print(f"{Fore.MAGENTA}{analysis}{Style.RESET_ALL}\n")

        print(f"\n{Fore.RED}Game over! Maximum attempts reached.{Style.RESET_ALL}")

    def play_solver_mode(self, secret_word: str) -> None:
        """
        Automatic solver mode - solver tries to find the secret word.

        Args:
            secret_word: The secret word to find
        """
        self.print_header()
        print(f"{Fore.GREEN}Solver Mode: Watching the AI solve Wordle...{Style.RESET_ALL}\n")

        secret_word = secret_word.lower()
        if not self.dict_manager.contains(secret_word):
            print(f"{Fore.YELLOW}Warning: '{secret_word}' is not in the dictionary{Style.RESET_ALL}\n")

        attempts = 0
        while attempts < self.max_attempts:
            attempts += 1
            print(f"\n{Fore.CYAN}═══ Attempt {attempts}/{self.max_attempts} ═══{Style.RESET_ALL}\n")

            # Get guess from solver
            guess = self.get_solver_suggestion()

            if not guess:
                print(f"{Fore.RED}Solver failed: No possible words!{Style.RESET_ALL}")
                return

            print(f"{Fore.BLUE}Solver guesses: {Style.BRIGHT}{guess.upper()}{Style.RESET_ALL}")

            # Generate feedback
            feedback = self._generate_feedback(guess, secret_word)

            # Display with colors
            print(f"Feedback: {self.display_word_colored(guess, feedback)}")

            # Check if won
            if guess == secret_word:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 SOLVED! Found '{secret_word.upper()}' in {attempts} attempts!{Style.RESET_ALL}")
                return

            # Add feedback to solver
            self.solver.add_feedback(guess, feedback)

            # Show statistics
            self.display_stats()

            input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

        print(f"\n{Fore.RED}Failed to solve! The word was: {secret_word.upper()}{Style.RESET_ALL}")

    def _generate_feedback(self, guess: str, secret: str) -> List[Feedback]:
        """
        Generate feedback for a guess against secret word.

        Args:
            guess: The guessed word
            secret: The secret word

        Returns:
            List of Feedback
        """
        feedback = [Feedback.ABSENT] * len(guess)
        secret_chars = list(secret)

        # First pass: mark correct positions
        for i, (g, s) in enumerate(zip(guess, secret)):
            if g == s:
                feedback[i] = Feedback.CORRECT
                secret_chars[i] = None

        # Second pass: mark present letters
        for i, char in enumerate(guess):
            if feedback[i] == Feedback.ABSENT and char in secret_chars:
                feedback[i] = Feedback.PRESENT
                secret_chars[secret_chars.index(char)] = None

        return feedback


def main():
    """Main entry point."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}╔═══════════════════════════════════════════╗")
    print(f"║   WORDLE CSP SOLVER - Main Menu       ║")
    print(f"╚═══════════════════════════════════════════╝{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}Choose mode:{Style.RESET_ALL}")
    print(f"  1. {Fore.GREEN}Assistant Mode{Style.RESET_ALL} - I help you solve Wordle")
    print(f"  2. {Fore.BLUE}Solver Mode{Style.RESET_ALL} - Watch me solve automatically")
    print(f"  3. {Fore.MAGENTA}LLM-Enhanced Assistant{Style.RESET_ALL} - AI-powered assistance")

    choice = input(f"\n{Fore.CYAN}Enter choice (1-3):{Style.RESET_ALL} ").strip()

    # Language selection
    print(f"\n{Fore.YELLOW}Choose language:{Style.RESET_ALL}")
    print(f"  1. English")
    print(f"  2. French")
    lang_choice = input(f"{Fore.CYAN}Enter choice (1-2):{Style.RESET_ALL} ").strip()
    language = "french" if lang_choice == "2" else "english"

    if choice == "1":
        game = WordleGameInterface(language=language, use_llm=False)
        game.play_assistant_mode()

    elif choice == "2":
        secret = input(f"\n{Fore.CYAN}Enter secret word (5 letters):{Style.RESET_ALL} ").strip().lower()
        if len(secret) != 5:
            print(f"{Fore.RED}Word must be 5 letters!{Style.RESET_ALL}")
            return

        game = WordleGameInterface(language=language, use_llm=False)
        game.play_solver_mode(secret)

    elif choice == "3":
        game = WordleGameInterface(language=language, use_llm=True)
        game.play_assistant_mode()

    else:
        print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

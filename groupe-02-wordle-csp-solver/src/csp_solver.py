"""
CSP Solver for Wordle using Constraint Satisfaction
Implements constraint satisfaction to solve Wordle puzzles efficiently.
No external CSP libraries needed - uses pure Python constraint propagation.
"""

from typing import List, Dict, Set, Tuple
from enum import Enum


class Feedback(Enum):
    """Feedback types for Wordle guesses"""
    CORRECT = "green"    # Letter in correct position
    PRESENT = "yellow"   # Letter in word but wrong position
    ABSENT = "gray"      # Letter not in word


class WordleCSPSolver:
    """
    Constraint Satisfaction Problem solver for Wordle.
    Uses OR-Tools CP-SAT to find words matching all constraints.
    """

    def __init__(self, word_length: int = 5, dictionary: List[str] = None):
        """
        Initialize the Wordle CSP solver.

        Args:
            word_length: Length of words to solve for (default 5)
            dictionary: List of valid words
        """
        self.word_length = word_length
        self.dictionary = dictionary or []
        self.constraints = []
        self.possible_words = set(self.dictionary)

        # Track letter information
        self.correct_positions: Dict[int, str] = {}  # position -> letter
        self.present_letters: Set[str] = set()  # letters in word but position unknown
        self.absent_letters: Set[str] = set()  # letters not in word
        self.wrong_positions: Dict[str, Set[int]] = {}  # letter -> positions where it's not
        self.max_letter_count: Dict[str, int] = {}  # letter -> max number of occurrences

    def add_feedback(self, guess: str, feedback: List[Feedback]) -> None:
        """
        Add feedback from a guess to update constraints.

        Args:
            guess: The guessed word
            feedback: List of Feedback for each letter
        """
        if len(guess) != self.word_length or len(feedback) != self.word_length:
            raise ValueError(f"Guess and feedback must be of length {self.word_length}")

        # First pass: count CORRECT and PRESENT occurrences of each letter
        letter_counts = {}
        for i, (letter, fb) in enumerate(zip(guess, feedback)):
            if fb == Feedback.CORRECT or fb == Feedback.PRESENT:
                letter_counts[letter] = letter_counts.get(letter, 0) + 1

        # Second pass: apply constraints
        for i, (letter, fb) in enumerate(zip(guess, feedback)):
            if fb == Feedback.CORRECT:
                self.correct_positions[i] = letter
                self.present_letters.add(letter)

            elif fb == Feedback.PRESENT:
                self.present_letters.add(letter)
                if letter not in self.wrong_positions:
                    self.wrong_positions[letter] = set()
                self.wrong_positions[letter].add(i)

            elif fb == Feedback.ABSENT:
                # If this letter appears elsewhere as CORRECT/PRESENT,
                # we know the EXACT count
                if letter in letter_counts:
                    # Set max count to the number of CORRECT/PRESENT occurrences
                    self.max_letter_count[letter] = letter_counts[letter]
                else:
                    # Letter is completely absent
                    self.absent_letters.add(letter)

        self._apply_constraints()

    def _apply_constraints(self) -> None:
        """Apply all constraints to filter possible words."""
        filtered_words = set()

        for word in self.possible_words:
            if self._satisfies_constraints(word):
                filtered_words.add(word)

        self.possible_words = filtered_words

    def _satisfies_constraints(self, word: str) -> bool:
        """
        Check if a word satisfies all current constraints.

        Args:
            word: Word to check

        Returns:
            True if word satisfies all constraints
        """
        # Check correct positions
        for pos, letter in self.correct_positions.items():
            if word[pos] != letter:
                return False

        # Check present letters are in the word
        for letter in self.present_letters:
            if letter not in word:
                return False

        # Check absent letters are not in the word
        for letter in self.absent_letters:
            if letter in word:
                return False

        # Check wrong positions
        for letter, positions in self.wrong_positions.items():
            for pos in positions:
                if word[pos] == letter:
                    return False

        # Check maximum letter counts
        for letter, max_count in self.max_letter_count.items():
            actual_count = word.count(letter)
            if actual_count > max_count:
                return False

        return True

    def get_possible_words(self) -> List[str]:
        """
        Get all words that satisfy current constraints.

        Returns:
            List of possible words
        """
        return sorted(list(self.possible_words))

    def get_best_guess(self, strategy: str = "max_info") -> str:
        """
        Get the best next guess based on strategy.

        Args:
            strategy: Strategy to use ('max_info', 'random', 'first')

        Returns:
            Best word to guess
        """
        possible = self.get_possible_words()

        if not possible:
            return None

        if strategy == "first" or len(possible) == 1:
            return possible[0]

        elif strategy == "max_info":
            # Use information theory to find word that eliminates most candidates
            return self._get_max_information_word(possible)

        else:
            import random
            return random.choice(possible)

    def _get_max_information_word(self, candidates: List[str]) -> str:
        """
        Find word that maximizes expected information gain.
        Uses letter frequency analysis.

        Args:
            candidates: List of candidate words

        Returns:
            Word with maximum expected information
        """
        # Count letter frequencies in remaining words
        letter_freq: Dict[Tuple[int, str], int] = {}

        for word in candidates:
            for pos, letter in enumerate(word):
                key = (pos, letter)
                letter_freq[key] = letter_freq.get(key, 0) + 1

        # Score each word by sum of its letter frequencies
        best_word = None
        best_score = -1

        for word in candidates:
            score = sum(letter_freq.get((pos, letter), 0)
                       for pos, letter in enumerate(word))

            # Bonus for unique letters (more information)
            unique_letters = len(set(word))
            score += unique_letters * 0.1

            if score > best_score:
                best_score = score
                best_word = word

        return best_word

    def reset(self) -> None:
        """Reset all constraints and start fresh."""
        self.constraints = []
        self.possible_words = set(self.dictionary)
        self.correct_positions = {}
        self.present_letters = set()
        self.absent_letters = set()
        self.wrong_positions = {}
        self.max_letter_count = {}

    def get_stats(self) -> Dict:
        """
        Get current solver statistics.

        Returns:
            Dictionary with solver stats
        """
        return {
            "total_words": len(self.dictionary),
            "possible_words": len(self.possible_words),
            "correct_positions": len(self.correct_positions),
            "present_letters": len(self.present_letters),
            "absent_letters": len(self.absent_letters),
            "elimination_rate": 1 - (len(self.possible_words) / len(self.dictionary)) if self.dictionary else 0
        }

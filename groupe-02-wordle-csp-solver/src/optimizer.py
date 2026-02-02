"""
Advanced optimization strategies for Wordle solving.
Implements information theory and heuristics to minimize attempts.
"""

import math
from typing import List, Dict, Tuple, Set
from collections import Counter
try:
    from .csp_solver import Feedback
except ImportError:
    from csp_solver import Feedback


class WordleOptimizer:
    """
    Advanced optimizer for Wordle solving using information theory.
    Implements strategies to minimize the expected number of guesses.
    """

    def __init__(self, dictionary: List[str]):
        """
        Initialize optimizer.

        Args:
            dictionary: List of valid words
        """
        self.dictionary = dictionary
        self.word_length = len(dictionary[0]) if dictionary else 5

    def calculate_entropy(self, word: str, candidates: List[str]) -> float:
        """
        Calculate expected information (entropy) for a guess.
        Higher entropy means more information gained.

        Args:
            word: Potential guess
            candidates: Current possible solutions

        Returns:
            Expected entropy value
        """
        if not candidates:
            return 0.0

        # Group candidates by the pattern they would produce
        pattern_groups: Dict[Tuple, List[str]] = {}

        for candidate in candidates:
            pattern = self._get_pattern(word, candidate)
            if pattern not in pattern_groups:
                pattern_groups[pattern] = []
            pattern_groups[pattern].append(candidate)

        # Calculate entropy using Shannon's formula
        total = len(candidates)
        entropy = 0.0

        for group in pattern_groups.values():
            probability = len(group) / total
            if probability > 0:
                entropy -= probability * math.log2(probability)

        return entropy

    def _get_pattern(self, guess: str, target: str) -> Tuple[int, ...]:
        """
        Get the pattern that would result from guessing 'guess' when answer is 'target'.
        Returns tuple of: 0=absent, 1=present, 2=correct

        Args:
            guess: The guessed word
            target: The target word

        Returns:
            Pattern tuple
        """
        pattern = [0] * len(guess)
        target_chars = list(target)

        # First pass: mark correct positions
        for i, (g, t) in enumerate(zip(guess, target)):
            if g == t:
                pattern[i] = 2
                target_chars[i] = None

        # Second pass: mark present letters
        for i, char in enumerate(guess):
            if pattern[i] == 0 and char in target_chars:
                pattern[i] = 1
                target_chars[target_chars.index(char)] = None

        return tuple(pattern)

    def get_best_guess_by_entropy(
        self,
        candidates: List[str],
        all_words: List[str] = None
    ) -> str:
        """
        Find the word that maximizes expected information gain.

        Args:
            candidates: Current possible solutions
            all_words: All valid guesses (uses candidates if None)

        Returns:
            Best guess word
        """
        if not candidates:
            return None

        if len(candidates) == 1:
            return candidates[0]

        # Use all words for first guess, candidates for later
        guess_pool = all_words if all_words and len(candidates) > 2 else candidates

        best_word = None
        best_entropy = -1

        for word in guess_pool:
            entropy = self.calculate_entropy(word, candidates)

            if entropy > best_entropy:
                best_entropy = entropy
                best_word = word

        return best_word

    def get_letter_frequencies(self, words: List[str]) -> Dict[Tuple[int, str], float]:
        """
        Calculate letter frequency at each position.

        Args:
            words: List of words to analyze

        Returns:
            Dictionary mapping (position, letter) to frequency
        """
        frequencies: Dict[Tuple[int, str], int] = {}
        total = len(words)

        for word in words:
            for pos, letter in enumerate(word):
                key = (pos, letter)
                frequencies[key] = frequencies.get(key, 0) + 1

        # Normalize to probabilities
        return {k: v / total for k, v in frequencies.items()}

    def score_word_by_frequency(
        self,
        word: str,
        frequencies: Dict[Tuple[int, str], float]
    ) -> float:
        """
        Score a word based on letter frequencies.

        Args:
            word: Word to score
            frequencies: Letter frequency map

        Returns:
            Score (higher is better)
        """
        score = 0.0
        seen_letters = set()

        for pos, letter in enumerate(word):
            freq = frequencies.get((pos, letter), 0)
            score += freq

            # Bonus for unique letters (more info)
            if letter not in seen_letters:
                score += 0.1
                seen_letters.add(letter)

        return score

    def get_strategic_first_guess(self, all_words: List[str]) -> str:
        """
        Get optimal first guess using pre-computed strategy.
        Common good starting words have high vowel and consonant coverage.

        Args:
            all_words: Dictionary of valid words

        Returns:
            Recommended first guess
        """
        # Pre-computed excellent starting words
        good_starters = [
            "arose", "slate", "crane", "soare", "trace",
            "crate", "irate", "stare", "adieu", "audio"
        ]

        # Use first available from pre-computed list
        for word in good_starters:
            if word in all_words:
                return word

        # Fallback: calculate best by entropy
        return self.get_best_guess_by_entropy(all_words[:100], all_words)

    def analyze_word_patterns(self, words: List[str]) -> Dict:
        """
        Analyze patterns in a word list.

        Args:
            words: List of words to analyze

        Returns:
            Dictionary with pattern analysis
        """
        if not words:
            return {}

        # Letter position analysis
        position_letters: Dict[int, Counter] = {
            i: Counter() for i in range(self.word_length)
        }

        for word in words:
            for pos, letter in enumerate(word):
                position_letters[pos][letter] += 1

        # Overall letter frequency
        all_letters = Counter(''.join(words))

        # Vowel analysis
        vowels = set('aeiou')
        vowel_positions = {i: 0 for i in range(self.word_length)}

        for word in words:
            for pos, letter in enumerate(word):
                if letter in vowels:
                    vowel_positions[pos] += 1

        # Common prefixes and suffixes
        prefixes = Counter(word[:2] for word in words)
        suffixes = Counter(word[-2:] for word in words)

        return {
            "total_words": len(words),
            "position_letters": {
                pos: letters.most_common(5)
                for pos, letters in position_letters.items()
            },
            "common_letters": all_letters.most_common(10),
            "vowel_positions": vowel_positions,
            "common_prefixes": prefixes.most_common(5),
            "common_suffixes": suffixes.most_common(5)
        }

    def get_minimax_guess(
        self,
        candidates: List[str],
        all_words: List[str] = None
    ) -> str:
        """
        Find guess that minimizes maximum remaining candidates (minimax strategy).

        Args:
            candidates: Current possible solutions
            all_words: All valid guesses

        Returns:
            Best minimax guess
        """
        if not candidates:
            return None

        if len(candidates) <= 2:
            return candidates[0]

        guess_pool = all_words if all_words else candidates

        best_word = None
        best_max_remaining = float('inf')

        for word in guess_pool[:min(len(guess_pool), 50)]:  # Limit for performance
            # Group candidates by pattern
            pattern_groups: Dict[Tuple, int] = {}

            for candidate in candidates:
                pattern = self._get_pattern(word, candidate)
                pattern_groups[pattern] = pattern_groups.get(pattern, 0) + 1

            # Find max group size
            max_remaining = max(pattern_groups.values()) if pattern_groups else 0

            if max_remaining < best_max_remaining:
                best_max_remaining = max_remaining
                best_word = word

        return best_word

    def get_hard_mode_guess(
        self,
        candidates: List[str],
        known_constraints: Dict
    ) -> str:
        """
        Get best guess in hard mode (must use all revealed information).

        Args:
            candidates: Words satisfying all constraints
            known_constraints: Current known constraints

        Returns:
            Best valid guess
        """
        # In hard mode, we can only guess from valid candidates
        if not candidates:
            return None

        frequencies = self.get_letter_frequencies(candidates)

        best_word = None
        best_score = -1

        for word in candidates:
            score = self.score_word_by_frequency(word, frequencies)

            if score > best_score:
                best_score = score
                best_word = word

        return best_word

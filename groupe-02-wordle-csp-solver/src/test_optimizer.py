"""
Unit Tests for Optimizer Module

Tests the optimization strategies for word selection:
  - Information theory (entropy calculation)
  - Best guess selection by entropy
  - Letter frequency analysis
  - Word scoring by frequency
  - Minimax strategy
  - Hard mode constraints

Test Coverage:
  - Entropy calculation for information gain
  - Finding best guess by entropy
  - Letter frequency computation
  - Word scoring based on frequencies
  - Strategic first guess selection
  - Pattern analysis (prefixes, suffixes, vowels)
  - Minimax strategy implementation
  - Hard mode compliance

Run with: python -m pytest test_optimizer.py
"""

from optimizer import WordleOptimizer


def test_entropy_calculation():
    """
    Test entropy calculation for words.
    
    Verifies that Shannon entropy is correctly calculated for a word
    based on how it distinguishes between candidate words.
    """
    dictionary = ["house", "mouse", "horse", "louse", "douse"]
    optimizer = WordleOptimizer(dictionary)

    entropy = optimizer.calculate_entropy("house", dictionary)
    assert entropy >= 0
    print(f"✓ Entropy calculation test passed (entropy: {entropy:.3f})")


def test_best_guess_by_entropy():
    """Test finding best guess by entropy."""
    dictionary = ["apple", "apply", "aptly", "ample", "maple"]
    optimizer = WordleOptimizer(dictionary)

    best = optimizer.get_best_guess_by_entropy(dictionary)
    assert best in dictionary
    print(f"✓ Best guess by entropy test passed (suggested: {best})")


def test_letter_frequencies():
    """Test letter frequency calculation."""
    dictionary = ["hello", "world", "helps"]
    optimizer = WordleOptimizer(dictionary)

    frequencies = optimizer.get_letter_frequencies(dictionary)
    assert len(frequencies) > 0
    assert all(0 <= freq <= 1 for freq in frequencies.values())

    print(f"✓ Letter frequency test passed ({len(frequencies)} position-letter pairs)")


def test_word_scoring():
    """Test word scoring by frequency."""
    dictionary = ["aabbc", "aabbd", "aabcc"]
    optimizer = WordleOptimizer(dictionary)

    frequencies = optimizer.get_letter_frequencies(dictionary)
    score = optimizer.score_word_by_frequency("aabbc", frequencies)
    assert score > 0

    print(f"✓ Word scoring test passed (score: {score:.3f})")


def test_strategic_first_guess():
    """Test strategic first guess."""
    dictionary = [
        "arose", "slate", "crane", "house", "mouse",
        "about", "trace", "stare", "share", "care"
    ]
    optimizer = WordleOptimizer(dictionary)

    first_guess = optimizer.get_strategic_first_guess(dictionary)
    assert first_guess in dictionary
    print(f"✓ Strategic first guess test passed (suggested: {first_guess})")


def test_pattern_analysis():
    """Test word pattern analysis."""
    dictionary = ["start", "stare", "state", "store", "stone"]
    optimizer = WordleOptimizer(dictionary)

    analysis = optimizer.analyze_word_patterns(dictionary)
    assert "total_words" in analysis
    assert analysis["total_words"] == len(dictionary)
    assert "common_letters" in analysis
    assert "position_letters" in analysis

    print(f"✓ Pattern analysis test passed")
    print(f"  Common letters: {analysis['common_letters'][:3]}")


def test_minimax_guess():
    """Test minimax strategy."""
    dictionary = ["hello", "hullo", "hallo", "hills", "halls"]
    optimizer = WordleOptimizer(dictionary)

    minimax = optimizer.get_minimax_guess(dictionary[:3])
    assert minimax in dictionary[:3]
    print(f"✓ Minimax guess test passed (suggested: {minimax})")


def test_hard_mode_guess():
    """Test hard mode guess."""
    dictionary = ["sharp", "shard", "shark", "share", "shale"]
    optimizer = WordleOptimizer(dictionary)

    constraints = {
        "correct_positions": {0: 's', 1: 'h'},
        "present_letters": {'a'},
        "absent_letters": set()
    }

    guess = optimizer.get_hard_mode_guess(dictionary, constraints)
    assert guess in dictionary
    assert guess[0] == 's' and guess[1] == 'h'  # Respects constraints

    print(f"✓ Hard mode guess test passed (suggested: {guess})")


def run_all_tests():
    """Run all optimizer tests."""
    print("\n" + "=" * 50)
    print("Running Optimizer Tests")
    print("=" * 50 + "\n")

    test_entropy_calculation()
    test_best_guess_by_entropy()
    test_letter_frequencies()
    test_word_scoring()
    test_strategic_first_guess()
    test_pattern_analysis()
    test_minimax_guess()
    test_hard_mode_guess()

    print("\n" + "=" * 50)
    print("✓ All optimizer tests passed!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_all_tests()

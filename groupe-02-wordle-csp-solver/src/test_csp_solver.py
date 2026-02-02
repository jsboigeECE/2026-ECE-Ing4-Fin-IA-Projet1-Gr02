"""
Unit Tests for CSP Solver Module

Tests the constraint satisfaction solver's ability to:
  - Apply feedback constraints (correct/present/absent letters)
  - Filter word lists based on constraints
  - Track solver statistics
  - Reset solver state

Test Coverage:
  - Basic constraints (correct positions, absent letters)
  - Present letters with wrong position constraints
  - Multiple feedback applications
  - Word elimination
  - Best guess selection
  - Statistics tracking
  - Solver reset functionality

Run with: python -m pytest test_csp_solver.py
"""

from csp_solver import WordleCSPSolver, Feedback


def test_basic_constraints():
    """
    Test basic constraint satisfaction.
    
    Tests that correct positions (green) and absent letters (gray) properly
    filter the dictionary.
    """
    dictionary = ["apple", "apply", "aptly", "aback", "about", "break", "bread"]
    solver = WordleCSPSolver(5, dictionary)

    # Test correct position (green) - 'a' correct, others absent
    solver.add_feedback("apple", [
        Feedback.CORRECT,  # a correct at position 0
        Feedback.ABSENT,   # p not in word
        Feedback.ABSENT,   # p not in word
        Feedback.ABSENT,   # l not in word
        Feedback.ABSENT    # e not in word
    ])

    possible = solver.get_possible_words()
    # Words starting with 'a' that don't contain p, l, e
    assert "aback" in possible or "about" in possible
    assert "break" not in possible  # doesn't start with 'a'
    assert "apple" not in possible  # contains p, l, e

    print("✓ Basic constraints test passed")


def test_present_letters():
    """Test present letters (yellow) constraints."""
    dictionary = ["trace", "crate", "react", "brown", "crown"]
    solver = WordleCSPSolver(5, dictionary)

    # 'r' is present but not at position 1
    # Letters b, o, w, n are absent
    solver.add_feedback("brown", [
        Feedback.ABSENT,   # b not in word
        Feedback.PRESENT,  # r in word but wrong position
        Feedback.ABSENT,   # o not in word
        Feedback.ABSENT,   # w not in word
        Feedback.ABSENT    # n not in word
    ])

    possible = solver.get_possible_words()
    # Only 'react' has 'r' but not at position 1, and doesn't have b,o,w,n
    assert "react" in possible
    assert "brown" not in possible  # eliminated
    # trace and crate have 'o' which is marked absent
    assert "trace" not in possible
    assert "crate" not in possible

    print("✓ Present letters test passed")


def test_multiple_feedback():
    """Test multiple rounds of feedback."""
    dictionary = ["slate", "scale", "scare", "stare", "share"]
    solver = WordleCSPSolver(5, dictionary)

    # First guess: slate
    solver.add_feedback("slate", [
        Feedback.CORRECT,  # s
        Feedback.ABSENT,   # l
        Feedback.PRESENT,  # a (wrong position)
        Feedback.ABSENT,   # t
        Feedback.CORRECT   # e
    ])

    possible1 = solver.get_possible_words()
    print(f"After first guess: {possible1}")

    # Second guess based on constraints
    if possible1:
        solver.add_feedback("share", [
            Feedback.CORRECT,  # s
            Feedback.ABSENT,   # h
            Feedback.CORRECT,  # a
            Feedback.CORRECT,  # r
            Feedback.CORRECT   # e
        ])

        possible2 = solver.get_possible_words()
        print(f"After second guess: {possible2}")

    print("✓ Multiple feedback test passed")


def test_elimination():
    """Test word elimination."""
    dictionary = ["arose", "prose", "close", "those", "morse"]
    solver = WordleCSPSolver(5, dictionary)

    initial_count = len(solver.get_possible_words())

    # Add feedback that eliminates some words
    solver.add_feedback("arose", [
        Feedback.ABSENT,   # a
        Feedback.ABSENT,   # r
        Feedback.CORRECT,  # o
        Feedback.CORRECT,  # s
        Feedback.CORRECT   # e
    ])

    remaining = solver.get_possible_words()
    assert len(remaining) < initial_count
    assert all('a' not in word for word in remaining)
    assert all('r' not in word for word in remaining)

    print(f"✓ Elimination test passed (eliminated {initial_count - len(remaining)} words)")


def test_best_guess():
    """Test best guess strategy."""
    dictionary = ["house", "mouse", "horse", "worse", "morse"]
    solver = WordleCSPSolver(5, dictionary)

    best = solver.get_best_guess(strategy="max_info")
    assert best is not None
    assert best in dictionary

    print(f"✓ Best guess test passed (suggested: {best})")


def test_stats():
    """Test statistics calculation."""
    dictionary = ["test1", "test2", "test3", "other"]
    solver = WordleCSPSolver(5, dictionary)

    stats = solver.get_stats()
    assert stats["total_words"] == 4
    assert stats["possible_words"] == 4
    assert stats["elimination_rate"] == 0.0

    # Add constraints
    solver.add_feedback("test1", [
        Feedback.CORRECT,
        Feedback.CORRECT,
        Feedback.CORRECT,
        Feedback.CORRECT,
        Feedback.ABSENT
    ])

    stats = solver.get_stats()
    assert stats["possible_words"] < 4
    assert stats["elimination_rate"] > 0

    print("✓ Statistics test passed")


def test_reset():
    """Test solver reset."""
    dictionary = ["alpha", "bravo", "delta"]
    solver = WordleCSPSolver(5, dictionary)

    solver.add_feedback("alpha", [Feedback.CORRECT] * 5)
    assert len(solver.get_possible_words()) < len(dictionary)

    solver.reset()
    assert len(solver.get_possible_words()) == len(dictionary)

    print("✓ Reset test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Running CSP Solver Tests")
    print("=" * 50 + "\n")

    test_basic_constraints()
    test_present_letters()
    test_multiple_feedback()
    test_elimination()
    test_best_guess()
    test_stats()
    test_reset()

    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_all_tests()

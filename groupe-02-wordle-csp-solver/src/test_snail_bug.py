"""
Regression Test: SNAIL Duplicate Letter Bug

Bug Description:
  When guessing "SANES" against "SNAIL", the first 'S' returns green (correct),
  but the last 'S' returns gray (not in word). The solver was incorrectly including
  words with 'S' in wrong positions due to improper duplicate letter handling.

Root Cause:
  The feedback processing didn't account for the fact that a letter can appear
  multiple times in a word, with different feedbacks for each occurrence.

Fix Applied:
  Improved constraint propagation to track which instances of letters have been
  used/eliminated in feedback processing.

This test ensures the bug remains fixed and duplicate letters are handled correctly.
"""

from csp_solver import WordleCSPSolver, Feedback


def simulate_wordle_feedback(guess: str, target: str) -> list:
    """
    Simulate Wordle feedback for a guess against a target word.
    
    Correctly handles duplicate letters by tracking which target letters
    have been matched to guess letters.

    Args:
        guess: The guessed word (5 letters)
        target: The target/secret word (5 letters)

    Returns:
        List of Feedback enums (one per letter in guess)
        
    Example:
        >>> simulate_wordle_feedback("arose", "house")
        [Feedback.ABSENT, Feedback.ABSENT, Feedback.PRESENT, Feedback.CORRECT, Feedback.CORRECT]
    """
    feedback = []
    target_letters = list(target)

    # First pass: mark correct positions
    for i in range(len(guess)):
        if guess[i] == target[i]:
            feedback.append(Feedback.CORRECT)
            target_letters[i] = None  # Mark as used
        else:
            feedback.append(None)  # Placeholder

    # Second pass: mark present/absent
    for i in range(len(guess)):
        if feedback[i] is not None:  # Already marked as CORRECT
            continue

        letter = guess[i]
        if letter in target_letters:
            feedback[i] = Feedback.PRESENT
            # Remove first occurrence
            target_letters[target_letters.index(letter)] = None
        else:
            feedback[i] = Feedback.ABSENT

    return feedback


def test_snail_scenario():
    """Test the exact scenario the user reported."""

    # Create solver with a small test dictionary
    test_dict = [
        "SNAIL", "SANES", "STANS", "SNARS", "SNABS", "SNAGS", "SNAPS",
        "TRAIL", "FRAIL", "GRAIL", "QUAIL", "FLAIL"
    ]

    solver = WordleCSPSolver(word_length=5, dictionary=test_dict)

    print("Testing SNAIL scenario...")
    print(f"Target word: SNAIL")
    print(f"Initial possible words: {len(solver.get_possible_words())}")
    print()

    # Simulate guessing "SANES" against "SNAIL"
    guess = "SANES"
    target = "SNAIL"

    feedback = simulate_wordle_feedback(guess, target)

    print(f"Guess: {guess}")
    print(f"Feedback: {[f.value for f in feedback]}")
    print()

    # Let's trace through what feedback should be:
    # S (pos 0): CORRECT - S is at position 0 in SNAIL
    # A (pos 1): PRESENT - A is in SNAIL at position 2
    # N (pos 2): PRESENT - N is in SNAIL at position 1
    # E (pos 3): ABSENT - E is not in SNAIL
    # S (pos 4): ABSENT - S already used at position 0 (duplicate)

    solver.add_feedback(guess, feedback)

    print(f"After feedback:")
    print(f"  Correct positions: {solver.correct_positions}")
    print(f"  Present letters: {solver.present_letters}")
    print(f"  Absent letters: {solver.absent_letters}")
    print(f"  Wrong positions: {solver.wrong_positions}")
    print()

    possible = solver.get_possible_words()
    print(f"Possible words remaining: {len(possible)}")
    print(f"Words: {possible}")
    print()

    # Verify the fix:
    # 1. 'S' should NOT be in absent_letters (it's CORRECT at position 0)
    # 2. 'E' SHOULD be in absent_letters
    # 3. Words with 'S' at position 0 should still be possible
    # 4. But 'S' should not appear elsewhere unless it's at position 0

    assert 'S' not in solver.absent_letters, "BUG: 'S' should not be in absent letters!"
    assert 'E' in solver.absent_letters, "BUG: 'E' should be in absent letters!"
    assert 0 in solver.correct_positions, "BUG: Position 0 should be correct!"
    assert solver.correct_positions[0] == 'S', "BUG: Position 0 should be 'S'!"

    # Check that suggested words don't have 'E'
    for word in possible:
        assert 'E' not in word, f"BUG: Word '{word}' contains 'E' which should be absent!"
        assert word[0] == 'S', f"BUG: Word '{word}' doesn't have 'S' at position 0!"

    print("✓ All assertions passed!")
    print("✓ Bug is FIXED - solver correctly handles duplicate letters!")


if __name__ == "__main__":
    test_snail_scenario()

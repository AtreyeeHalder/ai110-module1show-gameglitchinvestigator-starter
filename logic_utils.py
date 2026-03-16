def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIXME: Logic breaks here. Hard range easier than Normal
    # BUG 8: Normal range is 1-100, Hard 1-50
    # FIX: Change Hard range to 1-200 using Claude Code suggestion
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIXME: Logic breaks here. Floating point numbers accepted as valid guesses.
    # BUG 9: parse_guess accepts floating point numbers as valid guesses
    # FIX: Change parse_guess to reject non-integer inputs using Claude Code suggestion
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIXME: Logic breaks here. Hints are backwards.
    # BUG 1: "Too High" message says "Go HIGHER", "Too Low" message says "Go LOWER"
    # FIX: Swap messages for "Too High" and "Too Low" using Claude Code suggestion
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        if str(guess) == secret:
            return "Win", "🎉 Correct!"
        if int(guess) > int(secret):
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIXME: Logic breaks here. Score does not decrease for wrong guesses.
    # BUG 10: Does not decrease score for too high guesses and win score off by 1
    # FIX: Decrease score by 5 for too high guesses using Claude Code suggestion
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

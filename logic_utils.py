def get_range_for_difficulty(difficulty: str):
    """Return the inclusive numeric range for a given difficulty level.

    Maps a difficulty string to a (low, high) tuple that defines the
    secret-number search space for a game round. Falls back to the
    Normal range for any unrecognised difficulty value.

    Args:
        difficulty (str): The difficulty level. Accepted values are
            ``"Easy"``, ``"Normal"``, and ``"Hard"``.

    Returns:
        tuple[int, int]: A ``(low, high)`` pair representing the
        inclusive lower and upper bounds of the guess range.

        +----------+-------+-------+
        | Difficulty |  Low  |  High |
        +----------+-------+-------+
        | Easy       |   1   |   20  |
        | Normal     |   1   |  100  |
        | Hard       |   1   |  200  |
        | (default)  |   1   |  100  |
        +----------+-------+-------+

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 200)
        >>> get_range_for_difficulty("Unknown")
        (1, 100)
    """
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
    """Parse and validate raw user input into an integer guess.

    Converts a string value supplied by the player into an integer,
    returning a structured result that callers can inspect without
    having to catch exceptions themselves.  Non-numeric and empty
    inputs are rejected with a human-readable error message.

    Args:
        raw (str | None): The raw string entered by the user.
            May be ``None`` or an empty string, both of which are
            treated as missing input.

    Returns:
        tuple: A three-element tuple ``(ok, guess_int, error_message)``:

        * **ok** (*bool*) – ``True`` when parsing succeeded, ``False``
          otherwise.
        * **guess_int** (*int | None*) – The parsed integer value when
          ``ok`` is ``True``; ``None`` on failure.
        * **error_message** (*str | None*) – A user-facing error string
          when ``ok`` is ``False``; ``None`` on success.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
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
    """Compare a player's guess against the secret number and return the outcome.

    Evaluates whether the guess equals, exceeds, or falls short of the
    secret value and returns a structured result containing a short
    outcome label and a player-facing hint message.  Both numeric and
    string-typed values are supported; if a direct comparison raises a
    ``TypeError`` the function falls back to integer coercion.

    Args:
        guess (int | str): The value guessed by the player.
        secret (int | str): The secret target value for the round.

    Returns:
        tuple[str, str]: A ``(outcome, message)`` pair where *outcome*
        is one of the strings below and *message* is a display-ready
        hint for the player:

        * ``"Win"`` – the guess matches the secret exactly.
        * ``"Too High"`` – the guess is greater than the secret.
        * ``"Too Low"`` – the guess is less than the secret.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(80, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(20, 50)
        ('Too Low', '📈 Go HIGHER!')
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
    """Calculate and return the updated player score based on the round outcome.

    Applies a scoring formula to *current_score* according to the
    outcome of the latest guess.  A correct guess awards bonus points
    that diminish with each additional attempt, while incorrect guesses
    apply a flat penalty.  The minimum win bonus is clamped to 10
    points so the player always gains something on a correct answer.

    Scoring rules:
        * **Win** – awards ``max(100 - 10 * attempt_number, 10)`` points.
        * **Too High** – deducts 5 points.
        * **Too Low** – deducts 5 points.
        * *(any other outcome)* – score is unchanged.

    Args:
        current_score (int): The player's score before this guess.
        outcome (str): The outcome string returned by :func:`check_guess`.
            Expected values: ``"Win"``, ``"Too High"``, ``"Too Low"``.
        attempt_number (int): The 1-based index of the current attempt
            within the round, used to scale the win bonus.

    Returns:
        int: The updated score after applying the relevant rule.

    Examples:
        >>> update_score(0, "Win", 1)
        90
        >>> update_score(90, "Too High", 2)
        85
        >>> update_score(85, "Win", 3)
        155
    """
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

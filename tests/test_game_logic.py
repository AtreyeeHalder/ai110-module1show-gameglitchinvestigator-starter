from logic_utils import (
    check_guess, get_range_for_difficulty, parse_guess, update_score
)

# -- CHECK_GUESS TESTS --


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ('Win', '🎉 Correct!')


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ('Too High', '📉 Go LOWER!')


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ('Too Low', '📈 Go HIGHER!')


# -- GET_RANGE_FOR_DIFFICULTY TESTS --


def test_hard_range_harder_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard range must be larger than Normal range"


def test_hard_range_is_1_to_200():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200


# -- PARSE_GUESS TESTS --


def test_parse_guess_rejects_float_string():
    ok, value, err = parse_guess("3.7")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_accepts_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_rejects_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_parse_guess_rejects_empty():
    ok, value, _ = parse_guess("")
    assert ok is False
    assert value is None


def test_parse_guess_rejects_none():
    ok, value, _ = parse_guess(None)
    assert ok is False
    assert value is None


# -- UPDATE_SCORE TESTS --


def test_win_score_not_double_penalized():
    score = update_score(0, "Win", 1)
    assert score == 90, f"Expected 90 on attempt 1 win, got {score}"


def test_too_high_always_subtracts():
    score_even = update_score(100, "Too High", 2)
    score_odd = update_score(100, "Too High", 3)
    assert score_even == 95, f"Expected 95 on even attempt Too High, got {score_even}"
    assert score_odd == 95, f"Expected 95 on odd attempt Too High, got {score_odd}"

# -- STRETCH 1 ADVANCED EDGE CASE TESTS --

# Edge case 1: Negative integers
# parse_guess accepts "-5" because int("-5") succeeds, producing a valid integer
# that is outside the 1-200 game range. check_guess must handle it without crashing.
def test_negative_guess_parses_and_is_too_low():
    ok, value, err = parse_guess("-5")
    assert ok is True, "parse_guess should accept a negative integer string"
    assert value == -5
    assert err is None
    outcome, _ = check_guess(-5, 50)
    assert outcome == "Too Low", "A negative guess must be Too Low compared to any positive secret"


# Edge case 2: Extremely large integers
# Python has no integer overflow, so parse_guess("9999999999") succeeds.
# check_guess must handle a huge guess without raising an error.
def test_extremely_large_guess_is_too_high():
    ok, value, err = parse_guess("9999999999")
    assert ok is True, "parse_guess should accept an extremely large integer string"
    assert value == 9999999999
    assert err is None
    outcome, _ = check_guess(9999999999, 100)
    assert outcome == "Too High", "An astronomically large guess must be Too High"


# Edge case 3: Score going negative
# update_score has no floor: if current_score is smaller than the 5-point penalty,
# the returned score will be negative. This verifies the function doesn't crash and
# that callers should be aware the score can dip below zero.
def test_score_can_go_negative():
    result = update_score(2, "Too High", 1)
    assert result == -3, "Score should go negative when penalty exceeds current score (no floor enforced)"


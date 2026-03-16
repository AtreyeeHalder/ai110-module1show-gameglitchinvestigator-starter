import random
import streamlit as st
from logic_utils import (
    check_guess, get_range_for_difficulty, parse_guess, update_score
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

# FIXME: Logic breaks here. Normal has more attempts than Easy.
# BUG 2: Easy=6, Normal=8 backwards
# FIX: Change to Easy=8, Normal=6 using Claude Code suggestion
attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# random number generation does not change every run
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIXME: Logic breaks here. Main window attempts != sidebar attempts first time
# BUG 3: Main window attempts starts at 1, sidebar starts at 0
# FIX: Change main window attempts to start at 0 using Claude Code suggestion
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# FIXME: Logic breaks here. Attempts display does not update after first guess.
# BUG 6: Submit block does not update attempts display after first guess
# FIX: Use st.empty() to create a placeholder for attempts display and update it after each guess using Claude Code suggestion
attempts_display = st.empty()

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    # FIXME: Logic breaks here. New game does not start and become active.
    # BUG 5: Status does not reset to "playing" when starting new game.
    # FIX: Reset status to "playing" and clear history using Claude Code suggestion
    st.session_state.status = "playing"
    st.session_state.history = []
    # FIXME: Logic breaks here. Secret number range is same for all difficulties when starting new game.
    # BUG 4: Secret number range hardcoded to 1-100
    # FIX: Reset secret number in apt range using Claude Code suggestion
    st.session_state.secret = random.randint(low, high)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    # FIXME: Logic breaks here. Out of range guesses accepted.
    # BUG 9: Does not check if guess is within range for difficulty
    # FIX: Add range check if out of range using Claude Code suggestion
    if ok and (guess_int < low or guess_int > high):
        ok = False
        err = f"Guess must be between {low} and {high}."

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIXME: Logic breaks here. Range is same when difficulty changes.
# BUG 4: Range is hardcoded to 1-100 for all difficulties
# FIX: Changed range to {low} and {high} using Claude Code suggestion
attempts_display.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")

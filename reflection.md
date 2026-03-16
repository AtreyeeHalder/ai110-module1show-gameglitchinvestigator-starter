# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The first time I ran the game, it prompted me to guess a number between 1 and 100. I had 7 attempts. On the sidebar, the difficulty was Normal, but the number of attempts on the sidebar was 8, which is a conflict with the main page number of attempts which was 7.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

i. When I guessed 1, the hint asked me to "Go LOWER" even though 1 is the minimum possible number, so I expected it to ask me to go higher. Similarly, when I guessed 100, the hint asked me to "Go HIGHER" even though 100 is the maximum possible number, so it should have asked me to go lower. Thus, the hints were backwards.

ii. Difficulty level Easy has fewer attempts than difficulty level Normal, when I expected Normal to have fewer attempts than Easy. Also, sidebar number of attempts does not match main window number of attempts.

iii. I am unable to start a new game. When I press "New Game" I expected to be able to enter new guesses, but the page is stuck.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code for bug fixes.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

When I asked Claude Code about the bug related to the wrong number of attempts in difficulty levels Easy and Normal, and the mismatch between sidebar and main window attempts, the AI correctly suggested me to swap the attempt numbers for Easy and Normal, and initializing the value of attempts to 0 for the main window so there is no mismatch.

I verified the result by rerunning the game. There was no mismatch, and the number of attempts for the difficulty levels were reasonable.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

When I asked Claude Code about the bug related to the hints being backwards, the AI suggested this was because of passing even numbers as a string for comparison between the guess and the secret number. However, the example it gave was "1" > "50" which gives the expected result, so AI's example did not specifically illustrate the bug. I mentioned that to the AI, and it then corrected itself to give an alternative example, "2" > "19" which would be True for string comparison but expected to be False in the game. Another bug the AI correctly mentioned after this is returning "Too High, Go HIGHER" when guess > secret, but the hint should advise the player to go lower.

I verified the result by rerunning the game. The hints were no longer backwards.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I decided whether a bug was really fixed in two ways:
i. If the bug was within a core logic function, I generated tests using pytest targeting the fixed bugs and ran pytest to see if all tests pass. If all tests pass, the bug is fixed.
ii. If the bug was outside the core logic functions, I ran the Streamlit game and checked if I am experiencing the same bug while playing the game as before. If I do not experience the same bug, it is fixed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

Using pytest, one of the tests I ran for the 'get_range_for_difficulty' function is 'test_hard_range_is_1_to_200'. It is used to ensure the range for Hard difficulty level is 1-200. It asserts that the lower bound is 1 and upper bound 200. The test passed and showed that the bug does not exist anymore, and it would have failed if the test was run on the original code, when the Hard range was 1-50.

- Did AI help you design or understand any tests? How?

AI helped me design pytests. I asked Claude Code to generate tests using pytest for the bugs it fixed in the core logic functions. Instead of asking it to generate all tests at once, I asked it in each separate chat for the different functions where it fixed the bugs. I asked it to generate tests specifically targeting the bugs it fixed.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

Anytime I interact with any element of a Streamlit application, Streamlit reruns the entire Python script. As a result, every rerun generated a new secret number which could not be reached. Thus, I could not win.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Imagine the app is a whiteboard. Every time someone interacts with the board, Streamlit "reruns" erase the entire whiteboard and rewrite it from scratch. Session state, on the other hand, is like a sticky note stuck on the board that does not get erased between Streamlit reruns. So, the score, the guess history, the secret number, could be written on that sticky note and they will be preserved while the game is running without getting erased by the rerun.

- What change did you make that finally gave the game a stable secret number?

I put the code for the new secret number generation within an if condition which checks if a secret number already exists in the session state. On every subsequent Streamlit rerun after the first run, the if condition becomes False so the secret number stays the same for the entire game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

I will use pytest in a separate test file to test my code. I used to write tests in the same file, calling functions without pytest and printing their result, but I did not mention the expected value which made it less detailed. Creating tests in a separate file makes it easier to keep my code organized. Moreover, the assert statements also mention the expected value, making code more readable.

- What is one thing you would do differently next time you work with AI on a coding task?

I will create a new AI chat every time I need to fix a different error. I used to ask AI about all errors in the same chat, which led to the AI making more mistakes. Creating a new chat for each error helps the AI focus on only one error each time, reads the code in the context of one specific error, and suggest fixes for it more effectively.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I learned that AI generated code may contain very subtle errors that could potentially lead to problems in code. To prevent this, whenever I am consulting AI about my code, I should always carefully consider whether its suggestions will improve my code and if it works with base cases.
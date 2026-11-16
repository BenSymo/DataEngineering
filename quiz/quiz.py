"""
Data Engineering Quiz: 10 random multiple-choice questions from all lessons.

Run it:  python quiz/quiz.py
Answer each question by typing a number from 1 to 5. Type q to quit.
"""

import random
import sys

from questions import QUESTIONS

NUM_QUESTIONS = 10
NUM_OPTIONS = 5
LINE = "=" * 69


def ask(number, total, question):
    """Ask one question. Return True if right, False if wrong, None to quit."""
    topic, text, correct, wrong, why = question
    options = [correct] + list(wrong)
    random.shuffle(options)
    answer = options.index(correct) + 1

    print(f"\nQuestion {number} of {total}   [{topic}]")
    print(text)
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")

    while True:
        try:
            choice = input(f"Your answer (1-{NUM_OPTIONS}, q to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if choice.lower() == "q":
            return None
        if choice.isdigit() and 1 <= int(choice) <= NUM_OPTIONS:
            break
        print(f"Please type a number from 1 to {NUM_OPTIONS}.")

    if int(choice) == answer:
        print(f"Correct! {why}")
        return True
    print(f"Not quite. The answer was {answer}. {correct}")
    print(f"Why: {why}")
    return False


def main():
    for q in QUESTIONS:
        assert len(q[3]) == NUM_OPTIONS - 1, f"Question needs 4 wrong answers: {q[1]}"

    picked = random.sample(QUESTIONS, NUM_QUESTIONS)

    print(LINE)
    print("DATA ENGINEERING QUIZ")
    print(LINE)
    print(f"{NUM_QUESTIONS} questions, picked at random from {len(QUESTIONS)}.")

    score = 0
    asked = 0
    missed = set()
    for number, question in enumerate(picked, start=1):
        result = ask(number, NUM_QUESTIONS, question)
        if result is None:
            break
        asked += 1
        if result:
            score += 1
        else:
            missed.add(question[0])

    print(f"\n{LINE}")
    print(f"You scored {score} out of {asked}.")
    if asked and score == asked:
        print("Perfect score. Well done!")
    elif missed:
        print("Topics to review: " + ", ".join(sorted(missed)))
    print(LINE)


if __name__ == "__main__":
    sys.exit(main())

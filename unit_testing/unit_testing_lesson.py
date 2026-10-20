"""
Unit Testing Lesson: What it is, how to set it up, and how to use it.

Run this file to print the lesson:  python unit_testing_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS UNIT TESTING?
=====================================================================
A unit test is a small piece of code that checks that another small
piece of code (a "unit", usually one function) does what you expect.

Think of a car factory. Before the car is built, each part is tested
on its own: brakes, lights, horn. If a part is faulty you find out
straight away, not when the whole car crashes.

Why data engineers care:
  - Pipelines break quietly. Bad data can flow for weeks unnoticed.
  - Tests catch mistakes in your transform logic early.
  - You can change code with confidence: if tests pass, it still
    works.
  - Tests double as examples of how your code should behave.
  - CI/CD (see the cicd folder) runs your tests automatically.

=====================================================================
2. KEY WORDS
=====================================================================
UNIT         A small piece of code, like one function.
TEST         A function that runs the unit and checks the result.
ASSERT       A check: "this must be true or the test fails".
FIXTURE      Reusable setup for tests (e.g. sample data).
MOCK         A fake stand-in for something slow or external
             (a database, an API) so tests stay fast.
COVERAGE     The share of your code that tests actually run.
PARAMETRIZE  Run the same test with many inputs.

=====================================================================
3. INSTALL
=====================================================================
Python has a built-in tool (unittest), but most people use pytest. It
is simpler and more readable.

    pip install pytest

Check it works:
    pytest --version

=====================================================================
4. YOUR FIRST TEST
=====================================================================
Suppose you have a function in cleaning.py:

    def clean_name(name):
        return name.strip().title()

Create a file called test_cleaning.py:

    from cleaning import clean_name

    def test_clean_name_removes_spaces():
        assert clean_name("  alice  ") == "Alice"

    def test_clean_name_fixes_case():
        assert clean_name("BOB SMITH") == "Bob Smith"

Run it:
    pytest

Rules pytest follows:
  - Files are named test_*.py (or *_test.py).
  - Test functions start with test_.
  - A test passes if no assert fails and no error is raised.

Handy options:
    pytest -v               # show each test
    pytest -x               # stop at the first failure
    pytest -k "clean"       # only run tests with "clean" in the name
    pytest test_cleaning.py # run one file

=====================================================================
5. THE ARRANGE - ACT - ASSERT PATTERN
=====================================================================
Structure each test in three steps:

    def test_total_revenue():
        # Arrange: set up the input
        orders = [{"price": 10, "qty": 2}, {"price": 5, "qty": 1}]

        # Act: run the code
        result = total_revenue(orders)

        # Assert: check the result
        assert result == 25

Test ONE thing per test, and name it so a failure explains itself.

=====================================================================
6. TESTING MANY INPUTS WITH PARAMETRIZE
=====================================================================
    import pytest
    from cleaning import clean_name

    @pytest.mark.parametrize("raw, expected", [
        ("  alice ", "Alice"),
        ("BOB",      "Bob"),
        ("cara  ",   "Cara"),
        ("",         ""),
    ])
    def test_clean_name(raw, expected):
        assert clean_name(raw) == expected

=====================================================================
7. TESTING ERRORS
=====================================================================
Check that bad input raises the right error:

    import pytest

    def parse_age(value):
        age = int(value)
        if age < 0:
            raise ValueError("age cannot be negative")
        return age

    def test_negative_age_fails():
        with pytest.raises(ValueError):
            parse_age("-5")

=====================================================================
8. FIXTURES: SHARED SETUP
=====================================================================
    import pytest

    @pytest.fixture
    def sample_orders():
        return [
            {"id": 1, "price": 10, "qty": 2},
            {"id": 2, "price": 5,  "qty": 1},
        ]

    def test_total(sample_orders):          # pytest passes it in
        assert total_revenue(sample_orders) == 25

    def test_count(sample_orders):
        assert len(sample_orders) == 2

=====================================================================
9. MOCKING: AVOID REAL DATABASES AND APIs
=====================================================================
Unit tests should be fast and not need the internet. Replace the
outside world with a fake:

    from unittest.mock import patch

    def get_user_count():
        return fetch_from_api()["count"]       # slow, external

    def test_get_user_count():
        with patch("mymodule.fetch_from_api") as fake:
            fake.return_value = {"count": 42}
            assert get_user_count() == 42

=====================================================================
10. TESTING DATA PIPELINES
=====================================================================
  - Put transform logic in plain functions that take data in and
    return data out. These are easy to test.
  - Keep reading and writing (database, files) in separate thin
    functions, and mock those.
  - Test with tiny hand-made datasets: normal rows, empty input,
    nulls, duplicates, and odd values.
  - For Spark, build a small DataFrame in a fixture and compare the
    output to what you expect.

Example with pandas:

    import pandas as pd

    def drop_null_ids(df):
        return df.dropna(subset=["id"])

    def test_drop_null_ids():
        df = pd.DataFrame({"id": [1, None, 3], "v": ["a", "b", "c"]})
        result = drop_null_ids(df)
        assert list(result["id"]) == [1, 3]

=====================================================================
11. COVERAGE
=====================================================================
    pip install pytest-cov
    pytest --cov=.                  # show what code the tests run

High coverage does not guarantee good tests, but low coverage shows
you what is untested.

=====================================================================
12. GOOD HABITS
=====================================================================
  - Keep tests fast, so you run them all the time.
  - Each test should work alone and in any order.
  - Write a test when you find a bug, so it never returns.
  - Test behaviour (what goes in, what comes out), not internals.
  - Do not test the libraries themselves, only your own code.

=====================================================================
13. PRACTICE EXERCISE
=====================================================================
  1. pip install pytest.
  2. Write a function `remove_duplicates(rows)` that removes
     duplicate dicts by their "id".
  3. Write tests for: normal input, empty list, and duplicates.
  4. Use parametrize to cover 4 different inputs.
  5. Write a test that checks a bad input raises ValueError.
  6. Run `pytest --cov=.` and look for untested lines.

Next steps: learn CI/CD to run your tests automatically on every
push.
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()

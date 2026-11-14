"""
Data Structures and Algorithms (DSA) Lesson: What it is, how to practise it, and how to use it.

Run this file to print the lesson:  python dsa_lesson.py
"""

LESSON = """
=====================================================================
1. WHAT IS DSA?
=====================================================================
A DATA STRUCTURE is a way of storing data (a list, a dictionary).
An ALGORITHM is a set of steps that solves a problem (sorting,
searching, removing duplicates).

Think of a library. If books are in a random pile, finding one means
checking every book. If they are sorted by title on shelves, you find
one in seconds. Same books, better structure, much faster.

Why data engineers care:
  - Pipelines handle millions of rows. A slow approach that works on
    100 rows can take hours on 100 million.
  - Picking the right structure (e.g. a set for lookups) is often a
    one-line fix that makes a job 1000x faster.
  - Spark, SQL engines and databases use these ideas inside (hash
    joins, sorting, indexes, partitioning). Knowing them helps you
    understand why a query or job is slow.
  - Interviews for data engineers often include DSA questions.

=====================================================================
2. KEY WORDS
=====================================================================
BIG O        A way to describe how the work grows as the input
             grows. O(n) means "work grows in step with n items".
TIME         How long the code takes (in steps, not seconds).
SPACE        How much memory the code uses.
ARRAY/LIST   Items stored in order, found by position.
DICT (MAP)   Items stored as key -> value, found by key.
SET          A collection of unique items, fast to check "is x in?".
STACK        Last in, first out (a pile of plates).
QUEUE        First in, first out (a line at a shop).
HASH         A number made from a value, used to find it quickly.
RECURSION    A function that calls itself on a smaller problem.

=====================================================================
3. SETUP
=====================================================================
Nothing to install. Python has everything built in. Make a folder
dsa/ and a file for your practice, e.g. practice.py. Run with:

    python practice.py

To time code:
    import time
    start = time.perf_counter()
    ...your code...
    print(time.perf_counter() - start)

=====================================================================
4. BIG O: HOW FAST DOES IT GROW?
=====================================================================
Big O ignores small details and asks: if the input gets 10x bigger,
what happens to the work?

    O(1)        Constant. Same work always.      d["key"]
    O(log n)    Tiny growth. Halves each step.   binary search
    O(n)        Grows with the input.            loop over a list
    O(n log n)  A bit more than O(n).            good sorting
    O(n^2)      Grows very fast. Avoid.          loop inside a loop

Example for n = 1,000,000 items:
    O(n)        about 1 million steps
    O(n log n)  about 20 million steps
    O(n^2)      about 1,000,000,000,000 steps  (far too slow)

Rule of thumb: count the loops. One loop is O(n). A loop inside a
loop over the same data is O(n^2).

=====================================================================
5. THE BUILT-IN DATA STRUCTURES
=====================================================================
LIST: ordered, can change.
    nums = [3, 1, 2]
    nums.append(4)         # O(1)
    nums[0]                # O(1)
    3 in nums              # O(n)  must check each item

DICT: key -> value. The workhorse of data engineering.
    ages = {"alice": 30, "bob": 25}
    ages["alice"]          # O(1)
    "bob" in ages          # O(1)

SET: unique items only.
    ids = {1, 2, 3}
    2 in ids               # O(1)
    ids | {4}              # union
    ids & {2, 3, 9}        # intersection -> {2, 3}

TUPLE: ordered, cannot change. Good for fixed records and dict keys.
    point = (10, 20)

Useful extras from the standard library:
    from collections import Counter, defaultdict, deque
    Counter(["a", "b", "a"])        # {"a": 2, "b": 1}
    defaultdict(list)               # dict that starts missing keys as []
    deque()                         # fast queue (O(1) at both ends)

=====================================================================
6. THE BIGGEST EASY WIN: USE A SET OR DICT FOR LOOKUPS
=====================================================================
Task: find which orders have a customer in the customer list.

Slow, O(n * m): checks the whole list for every order.

    customer_ids = [1, 2, 3, ...]            # a list
    valid = [o for o in orders if o["customer_id"] in customer_ids]

Fast, O(n + m): turn the list into a set first.

    customer_ids = {1, 2, 3, ...}            # a set
    valid = [o for o in orders if o["customer_id"] in customer_ids]

Only one line changed. With 100,000 orders and 100,000 customers the
fast version is thousands of times quicker. This is exactly what a
HASH JOIN does in a database or Spark.

=====================================================================
7. COMMON PATTERNS WITH EXAMPLES
=====================================================================
a) Count things (group by)
    from collections import Counter
    events = ["click", "view", "click", "buy", "click"]
    Counter(events)                    # {"click": 3, "view": 1, "buy": 1}

b) Remove duplicates, keep order
    def dedupe(rows):
        seen = set()
        result = []
        for row in rows:
            if row["id"] not in seen:
                seen.add(row["id"])
                result.append(row)
        return result

c) Join two datasets (build a dict, then look up)
    users = {u["id"]: u for u in user_rows}
    joined = [
        {**o, "name": users[o["user_id"]]["name"]}
        for o in orders
        if o["user_id"] in users
    ]

d) Group rows by a key
    from collections import defaultdict
    by_user = defaultdict(list)
    for o in orders:
        by_user[o["user_id"]].append(o)

e) Find the top N
    import heapq
    heapq.nlargest(3, scores)          # faster than sorting everything

f) Two sums (find a pair that adds to a target) using a dict
    def two_sum(nums, target):
        seen = {}                      # value -> index
        for i, n in enumerate(nums):
            if target - n in seen:
                return [seen[target - n], i]
            seen[n] = i

=====================================================================
8. SORTING AND SEARCHING
=====================================================================
SORTING: Python's sorted() and list.sort() are O(n log n). Use them,
do not write your own.

    sorted(rows, key=lambda r: r["date"])
    sorted(rows, key=lambda r: r["amount"], reverse=True)

BINARY SEARCH: on SORTED data, find an item by halving the range
each time. O(log n).

    def binary_search(items, target):
        low, high = 0, len(items) - 1
        while low <= high:
            mid = (low + high) // 2
            if items[mid] == target:
                return mid
            if items[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

Python has this built in too: the bisect module.
Database indexes work in a similar way, which is why they make
lookups fast.

=====================================================================
9. STACKS, QUEUES AND LINKED IDEAS
=====================================================================
STACK (last in, first out): use a list.
    stack = []
    stack.append("a")
    stack.append("b")
    stack.pop()                        # "b"

QUEUE (first in, first out): use deque, not a list
    (list.pop(0) is O(n), deque.popleft() is O(1)).
    from collections import deque
    q = deque()
    q.append("job1")
    q.append("job2")
    q.popleft()                        # "job1"

Data engineering link: a Kafka topic is a queue of events, and
job schedulers use queues for tasks waiting to run.

=====================================================================
10. RECURSION
=====================================================================
A function that solves a problem by solving a smaller version of it.
It needs a base case (when to stop).

    def flatten(data):
        # turn nested lists into one flat list
        result = []
        for item in data:
            if isinstance(item, list):
                result.extend(flatten(item))   # smaller problem
            else:
                result.append(item)
        return result

    flatten([1, [2, [3, 4]], 5])       # [1, 2, 3, 4, 5]

Useful for nested JSON and folder trees. Python limits depth to
about 1000, so very deep data needs a loop and a stack instead.

=====================================================================
11. TREES AND GRAPHS
=====================================================================
TREE: items with parent -> children links (folders, org charts,
JSON documents).
GRAPH: items (nodes) joined by links (edges). A pipeline's DAG
(Airflow, dbt) is a graph: tasks are nodes, dependencies are edges.

A graph in Python is just a dict:
    graph = {
        "extract": ["clean"],
        "clean":   ["load", "report"],
        "load":    [],
        "report":  [],
    }

Walk it with BFS (breadth first, uses a queue):
    from collections import deque

    def bfs(graph, start):
        seen = {start}
        q = deque([start])
        order = []
        while q:
            node = q.popleft()
            order.append(node)
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        return order

    bfs(graph, "extract")   # ["extract", "clean", "load", "report"]

TOPOLOGICAL SORT: put tasks in an order where every task comes
after the ones it depends on. This is how Airflow and dbt decide
what to run first. Python has it built in:

    from graphlib import TopologicalSorter
    deps = {"load": {"clean"}, "clean": {"extract"}, "extract": set()}
    list(TopologicalSorter(deps).static_order())
    # ["extract", "clean", "load"]

=====================================================================
12. WHERE DSA SHOWS UP IN DATA ENGINEERING
=====================================================================
  - Joins: hash joins (dict), sort-merge joins (sorting).
  - Group by / counts: dicts and Counter.
  - Dedupe: sets.
  - Partitioning: hashing a key to pick a partition (Kafka, Spark).
  - Indexes: sorted structures for fast lookups.
  - DAGs: graphs and topological sort (Airflow, dbt).
  - Streaming windows: queues and deques.
  - Bloom filters: a compact set that may say "maybe", used to skip
    reading files.

=====================================================================
13. GOOD HABITS
=====================================================================
  - Get a correct answer first, then make it faster if needed.
  - Measure before you optimise. Time the code, do not guess.
  - Before writing a loop inside a loop, ask: can a dict or set
    replace the inner loop?
  - Use the standard library (Counter, deque, heapq, bisect).
  - Do not load huge data into a list if you can process it one row
    at a time (use generators).
  - Write unit tests for your solutions (see the unit_testing
    folder).
  - Practise little and often: one problem a day beats a weekend
    binge.

=====================================================================
14. PRACTICE EXERCISE
=====================================================================
  1. Write `has_duplicates(items)` two ways: with two loops, then
     with a set. Time both on 10,000 items.
  2. Write `top_n_users(events, n)` that returns the n users with
     the most events, using Counter.
  3. Write `join(orders, users)` using a dict and check it matches
     a slow nested-loop version.
  4. Write `flatten(data)` for nested lists using recursion.
  5. Using graphlib, put these tasks in a valid run order:
     report needs load, load needs clean, clean needs extract.
  6. Write a test for each function with pytest.
  7. Then try easy problems on LeetCode or NeetCode (arrays,
     hashing, stacks, binary search).

Next steps: keep practising, then see how these ideas appear inside
Spark (spark folder) and Airflow (airflow folder).
"""


def main():
    print(LESSON)


if __name__ == "__main__":
    main()

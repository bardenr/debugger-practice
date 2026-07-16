# Exercise 1: Inspecting a Crash
#
# A gradebook processor crashes with a KeyError. The traceback tells you
# which line failed, but not which student's record caused it or what the
# data looked like at the moment of failure.
#
# Instructions:
#   1. Run the file normally first:  python3 01_exception_crash.py
#      Read the traceback. Note what it tells you and what it doesn't.
#
#   2. Press <Leader>dc and select "file". No breakpoint needed —
#      when a program crashes with an unhandled exception, dap stops
#      there automatically before the process exits.
#
#   3. Inspect the Locals panel inside calculate_grade:
#      - Which record caused the crash?
#      - What key is missing from it?
#      - What does `record` look like compared to a valid entry?
#
#   4. Navigate up the call stack with <Leader>dk to see process_gradebook.
#      Check which iteration of the loop was running when it crashed.
#
# Compare what you can see here to what the traceback alone told you.
#
# Constraint: do not add print statements.


def calculate_grade(record):
    score = record["score"]
    max_score = record["max_score"]
    percentage = (score / max_score) * 100

    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"


def process_gradebook(records):
    results = []
    for record in records:
        grade = calculate_grade(record)
        results.append({"name": record["name"], "grade": grade})
    return results


gradebook = [
    {"name": "Alice",   "score": 92, "max_score": 100},
    {"name": "Bob",     "score": 78, "max_score": 100},
    {"name": "Charlie", "score": 85, "max_score": 100},
    {"name": "Diana",   "score": 71},
    {"name": "Eve",     "score": 88, "max_score": 100},
    {"name": "Frank",   "score": 95, "max_score": 100},
]

results = process_gradebook(gradebook)
for r in results:
    print(f"{r['name']}: {r['grade']}")

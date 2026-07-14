# Exercise 1: Exception Breakpoints
#
# A gradebook processor crashes with a KeyError. The traceback tells you
# which line failed, but with dozens of records you have no idea which
# student's data caused the problem or what was missing from it.
#
# Instructions:
#   1. Run the file once normally (python3 01_exception_breakpoints.py) to
#      see the traceback — note what it tells you and what it doesn't
#   2. Press <Leader>dc in Neovim to start the debugger
#   3. Before or after starting, press <Leader>dE and select "userUncaught"
#   4. The debugger will pause at the moment the exception is raised
#   5. Inspect the Locals panel — which record caused the crash?
#      What is missing from it?
#
# Notice how much more information you have compared to the traceback alone.
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

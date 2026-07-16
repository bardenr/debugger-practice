# Exercise 2: Exception Breakpoints
#
# A gradebook processor silently drops one student's result. The program
# runs without crashing and produces output — but Diana is missing.
# There is no traceback to read.
#
# Instructions:
#   1. Run the file normally first:  python3 01_exception_breakpoints.py
#      Notice that the output is missing one student. No error is shown.
#
#   2. Set a regular breakpoint on the `for record in records:` line below.
#      This gives you a place to pause before any processing happens.
#
#   3. Press <Leader>dc and select "file". The session starts and pauses
#      at your breakpoint.
#
#   4. While paused, press <Leader>dE and select "raised".
#      Exception breakpoints require an active session — this staging
#      breakpoint is what gives you time to set them.
#
#   5. Remove the staging breakpoint (<Leader>dp on that line), then
#      press <Leader>dc to continue. The debugger will now pause inside
#      calculate_grade at the exact moment the KeyError is raised, before
#      the except block silences it.
#
#   6. Inspect the Locals panel — which record caused it? What key is missing?
#
# The point: without <Leader>dE, a try/except that swallows exceptions gives
# you nothing — no crash, no traceback, just missing output. Exception
# breakpoints let you see inside the handler before it runs.
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
        try:
            grade = calculate_grade(record)
            results.append({"name": record["name"], "grade": grade})
        except Exception:
            pass
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

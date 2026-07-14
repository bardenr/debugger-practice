# Exercise 3: Generator Pipeline
#
# This pipeline computes running column sums from CSV data — after each row,
# it should yield the cumulative totals so far. Instead, every snapshot in
# the final output shows the same values.
#
# This exercise demonstrates how generators are lazy and what happens when
# you yield a mutable object.
#
# Instructions:
#   1. Set a breakpoint on the snapshots.append(snapshot) line in the
#      outer loop at the bottom of the file
#   2. Add watches for: snapshot    snapshots
#   3. Press <Leader>dc and step through each iteration of the loop
#   4. After the FIRST append: what does snapshots contain? Looks right.
#   5. After the SECOND append: what does snapshots contain now?
#      Both elements should be checked — are they what you expect?
#   6. When paused at the second or third iteration, open the REPL and run:
#      id(snapshots[0]) == id(snapshot)
#   7. What does that tell you about what column_sums is yielding?
#
# The bug is a single word in column_sums. The watches and REPL will
# show you exactly what's going wrong before you look for it.
#
# Constraint: do not add print statements.


def parse_rows(text):
    for line in text.strip().split("\n"):
        if line.startswith("#"):
            continue
        yield [float(v.strip()) for v in line.split(",")]


def column_sums(rows, num_cols):
    totals = [0.0] * num_cols
    for row in rows:
        for i, v in enumerate(row):
            totals[i] += v
        yield totals


csv = """
# Monthly sales by region: North, South, West
10, 20, 30
40, 50, 60
70, 80, 90
"""

snapshots = []
for snapshot in column_sums(parse_rows(csv), 3):
    snapshots.append(snapshot)

for i, s in enumerate(snapshots):
    print(f"After row {i + 1}: {s}")

# Expected:
#   After row 1: [10.0, 20.0, 30.0]
#   After row 2: [50.0, 70.0, 90.0]
#   After row 3: [120.0, 150.0, 180.0]

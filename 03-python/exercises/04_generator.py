# Exercise 4: Generator Pipeline
#
# This pipeline computes running column sums from CSV data — after each row,
# it should yield the cumulative totals so far. Instead, every snapshot in
# the final output shows the same values.
#
# This exercise demonstrates how generators are lazy and what happens when
# you yield a mutable object.
#
# Instructions:
#   1. Place your cursor anywhere inside test_column_sums and press
#      <Leader>dtm to run just this test under the debugger.
#      The test will fail — that's expected. This is how you'd debug a
#      failing pytest test in a real project.
#
#   2. Set a breakpoint on the snapshots.append(snapshot) line inside
#      test_column_sums, then run <Leader>dtm again.
#
#   3. Add watches for: snapshot    snapshots
#
#   4. Step through each iteration with <Leader>dc.
#      After the FIRST append: what does snapshots contain? Looks right.
#      After the SECOND append: check both elements — are they what you expect?
#
#   5. When paused at the second or third iteration, open the REPL and run:
#        id(snapshots[0]) == id(snapshot)
#      What does that tell you about what column_sums is yielding?
#
# The fix is one expression in column_sums: yield a copy of totals instead
# of the list itself. The watches and REPL will show you exactly what's
# going wrong before you look for it.
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


def test_column_sums():
    csv = """
# Monthly sales by region: North, South, West
10, 20, 30
40, 50, 60
70, 80, 90
"""
    snapshots = []
    for snapshot in column_sums(parse_rows(csv), 3):
        snapshots.append(snapshot)

    assert snapshots[0] == [10.0, 20.0, 30.0]
    assert snapshots[1] == [50.0, 70.0, 90.0]
    assert snapshots[2] == [120.0, 150.0, 180.0]

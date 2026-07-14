# Exercise 4: Watch Expressions
#
# find_duplicate() should return the first value that appears more than once.
# The output looks plausible at first glance — but it's wrong.
#
# Instructions:
#   1. Set a breakpoint on the `if n in seen:` line inside find_duplicate
#   2. In the Watch panel, add watches for: i    n    seen
#   3. Press <Leader>dc and step through the loop with <Leader>dn, watching all three
#      values update in the Watch panel with each step
#   4. When the function returns, compare what it returned to the values
#      of `i` and `n` at the moment it returned
#
# The bug is a single character. The watch expressions will show you
# exactly which variable is being used when the other one should be.
#
# Constraint: do not add print statements.


def find_duplicate(numbers):
    seen = set()
    for i, n in enumerate(numbers):
        if n in seen:
            return i
        seen.add(n)
    return None


data = [10, 30, 50, 30, 70, 10]
result = find_duplicate(data)
print(f"First duplicate value: {result}")

# Expected: 30   (the value that appears twice)
# Actual:   3    (looks like it could be right, but it's the index, not the value)

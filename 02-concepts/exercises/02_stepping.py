# Exercise 2: Stepping
#
# range_of() computes the difference between the largest and smallest
# values in a list. For the input below it should return 7, but it returns
# something else.
#
# Two helper functions are involved. One is correct; one is not.
#
# Instructions:
#   1. Set a breakpoint on the first line inside range_of (the `hi = ...` line)
#   2. Press <Leader>dc and select "file"
#   3. Step OVER each helper call with <Leader>dn. After each one, read the
#      value it assigned in the Locals panel. Does it look right?
#   4. When you find the wrong intermediate value, restart (<Leader>dr)
#      and this time step INTO that function with <Leader>ds to find the bug.
#
# Resist the urge to read the helper functions before you start — let
# the debugger show you which one is wrong first.
#
# Constraint: do not add print statements.


def find_max(numbers):
    max_val = 0
    for n in numbers:
        if n > max_val:
            max_val = n
    return max_val


def find_min(numbers):
    min_val = numbers[0]
    for n in numbers:
        if n < min_val:
            min_val = n
    return min_val


def range_of(numbers):
    hi = find_max(numbers)
    lo = find_min(numbers)
    return hi - lo


data = [-5, -3, -1, -8, -2]
result = range_of(data)
print(f"Range: {result}")

# Expected: 7   (-1 minus -8)
# Actual:   8

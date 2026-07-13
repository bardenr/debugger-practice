# Exercise 3: The Call Stack
#
# flatten() should return all non-list items from a nested list, in order.
# Instead it returns a mix of zeros and wrong values.
#
# Instructions:
#   1. Set a breakpoint on the `result.append(...)` line inside flatten
#   2. Press <F5> and select "Python: Current File"
#   3. The first pause will be at depth=0 (the outermost call). Note the
#      value of `depth` in the Locals panel, then continue with <F5>
#   4. Keep continuing until the call stack panel shows 3+ frames (you are
#      a few levels deep in the recursion)
#   5. Navigate UP the call stack frames. Look at `depth` at each level.
#   6. What is `depth` at the top level? What does that mean for items
#      processed there?
#
# Constraint: do not add print statements.


def flatten(lst, depth=0):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item, depth + 1))
        else:
            result.append(item * depth)
    return result


nested = [1, [2, 3], [4, [5, 6]], 7]
print(flatten(nested))

# Expected: [1, 2, 3, 4, 5, 6, 7]
# Actual:   [0, 2, 3, 4, 10, 12, 0]

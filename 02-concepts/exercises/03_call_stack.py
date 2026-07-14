# Exercise 3: The Call Stack
#
# flatten() should return all non-list items from a nested list, in order.
# Instead it returns a mix of zeros and wrong values.
#
# Instructions:
#
# STEP 1 — Start the session
#   Set a breakpoint on the `result.append(item * depth)` line inside flatten.
#   Press <Leader>dc and select "file".
#
# STEP 2 — Get deep enough in the recursion
#   The first pause is at depth=0. Keep pressing <Leader>dc to continue.
#   Watch the "Stacks" panel in nvim-dap-ui — it shows the active call chain.
#   Stop when you see 3 or more "flatten" frames listed (depth=2 or deeper).
#   You'll know you're there when the Locals panel shows depth=2.
#
# STEP 3 — Navigate frames with keymaps (no UI interaction needed)
#   Do NOT try to click or press Enter in the Stacks panel — nvim-dap-ui
#   doesn't support frame selection that way and will show an error.
#
#   Instead, stay in the source window and use:
#     <Leader>dk  — move up one frame (toward the outer/caller)
#     <Leader>dj  — move down one frame (toward the inner/callee)
#
#   Each press updates the Locals panel immediately. You can watch `depth`
#   change in the Locals panel as you move through the frames. The Stacks
#   panel shows which frame is currently active (marked with an arrow or
#   highlight) so you can use it as a visual reference, but you don't need
#   to interact with it directly.
#
# STEP 4 — Read depth at each frame
#   Press <Leader>dk repeatedly to move toward the outermost flatten call.
#   At each step, check `depth` in the Locals panel.
#
#   What is `depth` at the outermost flatten frame?
#   What does `item * depth` compute when depth is that value?
#   That is the bug.
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

# Exercise 3: Class State
#
# A shopping cart class produces wrong receipts. Alice's cart shows items
# that belong to Bob, and both totals are wrong.
#
# Instructions:
#   1. Set a breakpoint on the self.items.append(...) line inside add_item
#
#   2. Add watches for self.items and self.owner.
#      The Locals panel shows variables for the current frame, but its
#      contents change as you move between frames and steps. Watch expressions
#      persist across every pause and update in place — useful here because
#      you want to see self.items evolve across multiple calls to add_item,
#      including calls on different cart instances.
#
#      To add a watch:
#        a. Use <C-w>h/j/k/l to move focus into the Watches panel
#        b. Press 'e' to add a new expression
#        c. Type the expression (e.g. self.items) and press <Enter>
#        d. Repeat for self.owner
#        e. Press <C-w>p to jump back to the source window
#
#      To remove a watch later: move focus to the Watches panel and press 'd'
#      on the entry you want to remove.
#
#   3. Press <Leader>dc. When the session pauses, open the REPL (<Leader>d>)
#      and run:
#
#        import sys; sys.executable
#
#      This shows which Python the debug adapter is using. It won't affect
#      this bug, but it is the right tool to reach for when behavior in the
#      debugger doesn't match what you see running the file normally —
#      environment mismatch is a common cause.
#
#   4. Continue stepping through adding items to cart1, then cart2
#   5. Watch self.items carefully as you cross from cart1 to cart2 —
#      does anything about it surprise you?
#   6. When paused inside cart2's first add_item call, open the REPL
#      and run: id(cart1.items) == id(cart2.items)
#   7. What does that result tell you about where the bug is?
#
# Constraint: do not add print statements.


class ShoppingCart:
    items = []

    def __init__(self, owner):
        self.owner = owner

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})

    def total(self):
        return sum(item["price"] for item in self.items)

    def receipt(self):
        lines = [f"=== Cart for {self.owner} ==="]
        for item in self.items:
            lines.append(f"  {item['name']}: ${item['price']:.2f}")
        lines.append(f"  Total: ${self.total():.2f}")
        return "\n".join(lines)


cart1 = ShoppingCart("Alice")
cart1.add_item("Apple", 1.50)
cart1.add_item("Bread", 3.00)

cart2 = ShoppingCart("Bob")
cart2.add_item("Milk", 2.75)

print(cart1.receipt())
print()
print(cart2.receipt())

# Expected:
#   === Cart for Alice ===
#     Apple: $1.50
#     Bread: $3.00
#     Total: $4.50
#
#   === Cart for Bob ===
#     Milk: $2.75
#     Total: $2.75

# Exercise 2: Class State
#
# A shopping cart class produces wrong receipts. Alice's cart shows items
# that belong to Bob, and both totals are wrong.
#
# Instructions:
#   1. Set a breakpoint on the self.items.append(...) line inside add_item
#   2. Add watches for: self.items    self.owner
#   3. Press <F5> and step through adding items to cart1, then cart2
#   4. Watch self.items carefully as you cross from cart1 to cart2 —
#      does anything about it surprise you?
#   5. When paused inside cart2's first add_item call, open the REPL
#      and run: id(cart1.items) == id(cart2.items)
#   6. What does that result tell you about where the bug is?
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

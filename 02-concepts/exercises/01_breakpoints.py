# Exercise 1: Breakpoints
#
# This function claims to count the vowels in a word, but it returns
# wrong results for most inputs.
#
# Instructions:
#   1. Set a breakpoint on the `if char in "aeiou":` line
#   2. Press <F5> and select "Python: Current File"
#   3. When paused, look at the Locals panel — note the values of `char` and `count`
#   4. Press <F5> again. Does it pause a second time for the same word?
#   5. That observation is your clue. Figure out why execution doesn't
#      continue stepping through the word.
#
# Constraint: do not add print statements.


def count_vowels(text):
    count = 0
    for char in text.lower():
        if char in "aeiou":
            count += 1
        return count


words = ["hello", "world", "python", "debugger"]
for word in words:
    result = count_vowels(word)
    print(f"{word}: {result} vowels")


# Expected:
#   hello: 2 vowels
#   world: 1 vowel
#   python: 1 vowel
#   debugger: 3 vowels

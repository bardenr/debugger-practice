# Exercise 5: The REPL
#
# encode() and decode() should be inverses of each other — encoding then
# decoding should return the original message. The first word comes back
# correctly; every other word is garbled.
#
# Instructions:
#   1. Set a breakpoint inside decode on the `shift = ...` line
#   2. Press <F5> and select "Python: Current File"
#   3. Continue past the first word (i=0) until i=1
#   4. Open the REPL with <Leader>d>
#   5. In the REPL, inspect `shift`, `word`, and `key`
#   6. Look at how encode computed its shift for position i=1.
#      Try computing that same value in the REPL.
#   7. Call caesar_cipher(word, -<your_shift>) with your computed value.
#      Does it decode the word correctly?
#   8. Once you understand the fix, close the session and change the code.
#
# The REPL lets you test the corrected formula against the live encoded
# data before touching a single line of source.
#
# Constraint: do not add print statements.


def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return ''.join(result)


def encode(message, key):
    words = message.split()
    encoded = []
    for i, word in enumerate(words):
        shift = (key + i) % 26
        encoded.append(caesar_cipher(word, shift))
    return ' '.join(encoded)


def decode(message, key):
    words = message.split()
    decoded = []
    for i, word in enumerate(words):
        shift = (key - i) % 26
        decoded.append(caesar_cipher(word, -shift))
    return ' '.join(decoded)


original = "The quick brown fox jumps"
key = 5
encoded = encode(original, key)
decoded = decode(encoded, key)

print(f"Original: {original}")
print(f"Encoded:  {encoded}")
print(f"Decoded:  {decoded}")

# Expected decoded == original
# Actual: first word matches, rest are wrong

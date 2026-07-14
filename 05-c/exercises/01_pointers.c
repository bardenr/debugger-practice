/* Exercise 1: Pointer Inspection
 *
 * This program counts the total characters across an array of strings.
 * It crashes with a segfault before printing the result.
 *
 * Instructions:
 *   1. Run it first without the debugger to see the crash:
 *        ./exercises/01_pointers
 *   2. Set a breakpoint on the `return` line inside count_chars
 *   3. Press <Leader>dc and enter: exercises/01_pointers
 *   4. Each time it pauses, look at `str` in the Locals panel.
 *      The debugger shows both the pointer address and the string it points to.
 *   5. Continue with <Leader>dc until `str` looks different from the others.
 *      What address does it show? What string contents?
 *   6. Open the REPL and evaluate: str
 *      Then evaluate: str == 0
 *      What does that confirm?
 *
 * Constraint: no printf for debugging.
 */

#include <stdio.h>
#include <string.h>

int count_chars(const char *str) {
    return (int)strlen(str);
}

int main(void) {
    const char *words[] = {"hello", "world", NULL, "debug", "practice"};
    int n = 5;

    int total = 0;
    for (int i = 0; i < n; i++) {
        total += count_chars(words[i]);
    }

    printf("Total characters: %d\n", total);
    return 0;
}

/* Exercise 2: Array Bounds
 *
 * This program sums the elements of an array. The result is wrong —
 * it includes an extra value that doesn't belong to the array.
 *
 * C arrays don't know their own length. There is no bounds checking.
 * Reading past the end gives you whatever bytes happen to be in adjacent
 * memory — no crash, just a wrong answer.
 *
 * Instructions:
 *   1. Set a breakpoint on the `total += arr[i]` line inside sum_array
 *   2. Add watches for: i    arr[i]    total
 *   3. Press <F5> and enter: exercises/02_array_bounds
 *   4. Step through each iteration with <F10>, watching all three values
 *   5. The array has 5 elements (indices 0–4). Keep stepping past that.
 *      What is `i` when it stops being a valid index?
 *      What does `arr[i]` show at that point?
 *   6. Use the REPL to evaluate: i    and: arr[i]
 *      That extra value is what's corrupting the sum.
 *
 * Constraint: no printf for debugging.
 */

#include <stdio.h>

#define SIZE 5

int sum_array(int *arr, int n) {
    int total = 0;
    for (int i = 0; i <= n; i++) {
        total += arr[i];
    }
    return total;
}

int main(void) {
    int numbers[SIZE] = {10, 20, 30, 40, 50};
    int result = sum_array(numbers, SIZE);
    printf("Sum: %d\n", result);
    /* Expected: 150 */
    return 0;
}

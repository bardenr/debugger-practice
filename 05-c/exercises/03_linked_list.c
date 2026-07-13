/* Exercise 3: Uninitialized Pointer
 *
 * This program builds a linked list of three nodes and sums their values.
 * It either crashes or loops — depending on what garbage happened to be
 * in memory — because a pointer was never initialized.
 *
 * This exercise is about distinguishing a NULL pointer (safe end of list)
 * from an uninitialized pointer (garbage address that looks non-null).
 *
 * Instructions:
 *   1. Set a breakpoint on the `next_node = current->next` line inside sum_list
 *   2. Add watches for: current    next_node
 *   3. Press <F5> and enter: exercises/03_linked_list
 *   4. Step through with <F10>. Watch `next_node` after each assignment.
 *      For the first two nodes it should show a recognizable address pointing
 *      to the next node's struct contents.
 *   5. After the third node (value=30), step through the assignment again.
 *      What does `next_node` look like now? Is it 0x0?
 *   6. Open the REPL and evaluate: next_node == 0
 *      Then: current->value   (while current is still the third node)
 *   7. The while loop checks `current != NULL`. If next_node is not 0x0,
 *      what happens on the next iteration?
 *
 * Constraint: no printf for debugging.
 */

#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

Node *create_node(int value) {
    Node *node = (Node *)malloc(sizeof(Node));
    node->value = value;
    /* next is not initialized */
    return node;
}

void sum_list(Node *head) {
    int total = 0;
    int count = 0;
    Node *current = head;
    Node *next_node = NULL;

    while (current != NULL) {
        total += current->value;
        next_node = current->next;
        current = next_node;
        count++;
    }

    printf("Sum: %d, Count: %d\n", total, count);
}

int main(void) {
    Node *a = create_node(10);
    Node *b = create_node(20);
    Node *c = create_node(30);

    a->next = b;
    b->next = c;
    /* c->next is never set */

    sum_list(a);

    free(a);
    free(b);
    free(c);
    return 0;
}

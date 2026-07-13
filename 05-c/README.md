# C

This section assumes you've worked through [02-concepts](../02-concepts/concepts.md). C debugging uses the same tools, but the bugs you encounter are different in character — instead of logic errors and wrong values, you're often chasing memory you shouldn't be reading, pointers that don't point where you think, and state that was never initialized.

The debugger is especially valuable in C because these bugs leave no error messages, only crashes or silent wrong output.

---

## C-Specific Features

### Compilation Flags

Always compile with these flags when debugging:

```bash
gcc -g -O0 -Wall -o my_program my_program.c
```

| Flag | What it does |
|------|--------------|
| `-g` | Embed debug symbols (line numbers, variable names, types) |
| `-O0` | Disable optimizations — without this, the compiler can eliminate variables and reorder code, making the debugger lie to you |
| `-Wall` | Enable all warnings — the compiler often spots the bug before you do |

The Makefile in this section includes these flags automatically.

### Pointer Inspection

In the Locals panel, a pointer variable shows as an address (`0x00007ffd...`) and, when the debugger can determine the type, the value it points to. A null pointer shows as `0x0` or `<NULL>`.

When you have a pointer `p` in the REPL:
- `*p` — dereference (show the value it points to)
- `p->field` — dereference and access a struct field
- `p[3]` — treat as an array and read the 4th element
- `(int)p` — show the raw address as an integer (useful for comparing two pointers)

### Arrays

C arrays decay to pointers. The debugger sees a `int *arr` and doesn't know how many elements it has — it just shows the pointer address. To inspect the contents, use the REPL:

```
arr[0]   → first element
arr[4]   → fifth element
```

Or expand the pointer in the Locals panel if the debugger infers the count from context (it sometimes does for fixed-size local arrays).

### Uninitialized Memory

Memory from `malloc` is not zeroed. A pointer field that was never set contains whatever bytes happened to be in that heap allocation — often a non-zero, non-null garbage address. In the debugger, this looks like a valid-looking pointer (non-zero address) that leads nowhere useful.

Key distinction:
- **NULL pointer** → `0x0` in the Locals panel. Safe to detect with `== NULL`.
- **Uninitialized pointer** → some large hex address. Not null, but not valid either. Dereferencing it crashes.

### Core Dumps

When a program segfaults outside the debugger, the OS can save a memory snapshot called a **core dump**. You can load it later and inspect the exact state at the moment of the crash — which line, which variables, the full call stack.

On macOS:
```bash
ulimit -c unlimited   # enable core dumps for this shell session
./my_program          # if it segfaults, writes to /cores/core.<pid>
```

Loading a core dump in the debugger requires a different launch configuration (using `request = "attach"` with the core file path). For now, the more practical approach is to run the program under the debugger directly — the adapter catches segfaults and pauses at the crash, giving you the same information.

---

## Project Structure

```
05-c/
├── Makefile
└── exercises/
    ├── 01_pointers.c
    ├── 02_array_bounds.c
    └── 03_linked_list.c
```

Build all exercises:

```bash
cd 05-c
make
```

When the debugger prompts for a binary path, enter:
- `exercises/01_pointers`
- `exercises/02_array_bounds`
- `exercises/03_linked_list`

---

## Exercises

| File | What you're practicing | What you're finding |
|------|----------------------|---------------------|
| `exercises/01_pointers.c` | Pointer inspection in the Locals panel | Which pointer in a loop is NULL before the crash |
| `exercises/02_array_bounds.c` | Watching loop variables with the array | The off-by-one that reads past the end of the array |
| `exercises/03_linked_list.c` | Distinguishing NULL from garbage pointers | Which node has an uninitialized `next` and what it contains |

Constraint: no `printf` for debugging. Find the answer with the debugger only.

---

### A Note on Sanitizers

AddressSanitizer (`-fsanitize=address`) and Valgrind detect memory errors at runtime with precise messages. They're excellent complements to the debugger — sanitizers tell you *that* a memory error occurred and where; the debugger lets you inspect *why*. For real C work, use both. These exercises intentionally skip sanitizers so you build the habit of reading memory state directly.

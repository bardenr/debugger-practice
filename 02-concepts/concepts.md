# Core Debugger Concepts

These concepts apply regardless of language. The exercises use Python because it has the least syntax noise, but the mechanics — the keystrokes, the panels, the mental model — are identical when you get to Rust and C.

## How This Module Works

Each section explains one concept, then gives you a small Python program with a bug to find. The constraint is the same for every exercise: **no adding print statements**. Find the answer using only the tool described in that section.

To run an exercise:
1. Open the file in Neovim
2. Set a breakpoint where the instructions say
3. Press `<Leader>dc` → select "file"

---

## 1. Breakpoints

A breakpoint tells the debugger to pause execution at a specific line. When the program reaches that line, it freezes — the process is suspended but still alive — and you can inspect everything in scope.

Press `<Leader>dp` on any line to toggle a breakpoint. A `●` appears in the gutter (red if you've configured the sign highlights in your dap config, grey otherwise). Press `<Leader>dc` to start; the program runs at full speed until it hits the breakpoint, then stops.

When paused, the nvim-dap-ui panels show:
- **Locals** — every variable in the current function scope, with its current value
- **Arguments** — what was passed into this call
- **Globals** — module-level names (usually less useful)

### Conditional breakpoints

In a loop of 10,000 iterations, a regular breakpoint pauses 10,000 times. A **conditional breakpoint** (`<Leader>dw`) only pauses when an expression evaluates to true — `i == 500`, `name == "alice"`, `len(result) > expected`. This is one of the biggest practical speedups over print-debugging.

### Logpoints

A **logpoint** (`<Leader>dl`) is a breakpoint that doesn't stop — it prints a message to the Debug Console. Enter a format string using local variable names: `"i={i}, value={value}"`. Useful for tracing values across many iterations without interrupting execution.

### Exercise 1

Open `exercises/01_breakpoints.py`. A function counts vowels, but returns wrong results for most words.

**Instructions:**
1. Set a breakpoint on the `if char in "aeiou":` line inside `count_vowels`
2. Press `<Leader>dc`
3. When it pauses, look at the Locals panel — what are `char` and `count`?
4. Press `<Leader>dc` again to continue. Does it pause a second time for the same word?
5. That behavior is your clue. Figure out why `count` stops being tracked after so few steps.

---

## 2. Stepping

Once paused, you advance execution line by line. There are three movements:

| Key | Name | What it does |
|-----|------|--------------|
| `<Leader>dn` | Step over | Execute this line. If it calls a function, run the whole function without entering it. |
| `<Leader>ds` | Step into | If this line calls a function, jump inside that function and pause at its first line. |
| `<Leader>df` | Step out | Run until the current function returns, then pause in the caller. |

### The mental model: trust

Think of stepping in terms of how much you trust a function:

- **Step over** = "I trust this. Run it."
- **Step into** = "I don't trust this. Show me."
- **Step out** = "I've seen enough. Take me back."

In practice: step over everything until a value looks wrong, then go back to where it was computed and step into the suspicious call. You'll spend most of your time pressing `<Leader>dn`, occasionally switching to `<Leader>ds` when something seems off.

### Exercise 2

Open `exercises/02_stepping.py`. A calculation returns the wrong answer. Two helper functions are involved — one is correct and one is not.

**Instructions:**
1. Set a breakpoint on the first line inside `range_of`
2. Press `<Leader>dc`
3. Step over each helper call. After each one, check the value of the variable it assigned — does it look right?
4. When you find the wrong value, restart (`<Leader>dr`) and this time step *into* that function to find the bug

Do not read the helper functions before you start. Use step over to identify which is wrong, then step into to confirm.

---

## 3. The Call Stack

When your program pauses, you may be inside a chain of calls: `main` called `process`, which called `transform`, which called `validate`. Each active function call is a **frame**. The list of frames — from outermost to innermost — is the **call stack**.

The call stack panel in nvim-dap-ui shows every frame. Navigate to any frame with `<Leader>dk` (toward outer/caller) and `<Leader>dj` (toward inner/callee) — the Locals panel updates immediately. The program is still paused in the innermost frame; you're just looking around at a different level.

This matters most for recursive functions or deep call chains where the problem may be in what was *passed in*, not what the function does with it.

### Exercise 3

Open `exercises/03_call_stack.py`. A recursive flatten function returns wrong values.

**Instructions:**
1. Set a breakpoint on the `result.append(...)` line inside `flatten`
2. Press `<Leader>dc`. Continue a few times until you're several levels deep (watch the Stacks panel grow)
3. Press `<Leader>dk` to move up toward the outer call. Check `depth` in Locals after each press
4. What does `depth` equal at the outermost frame? What does that tell you about what's happening to top-level items?

---

## 4. Inspecting State

The Locals panel is passive — it shows what's there. These two tools let you actively query the program's state.

### Watch expressions

A watch expression is evaluated and displayed every time execution pauses. You add them in the Watch panel (part of the default nvim-dap-ui layout). Type any expression — a variable name, a calculation, a function call — and it updates with each step.

This is especially useful in loops where you want to track how multiple related values evolve together, side by side, across iterations.

### Evaluate expression

`<Leader>de` opens a prompt. Type any expression; the debugger evaluates it in the current frame and shows the result inline. Good for quick spot-checks without cluttering the Watch panel.

You can also hover your cursor over a variable name in the source buffer — nvim-dap-ui shows its value inline.

### Exercise 4

Open `exercises/04_watch_expressions.py`. A function that finds duplicate values returns an output that looks correct — but isn't, for a subtle reason.

**Instructions:**
1. Set a breakpoint inside the loop in `find_duplicate`
2. In the Watch panel, add watches for `i` and `n`
3. Press `<Leader>dc` and step through the loop, watching both values
4. When the function returns, compare what it actually returned to what `i` and `n` were at that moment

---

## 5. The REPL

`<Leader>d>` opens the Debug REPL — an interactive Python prompt that runs in the context of the paused program. You can:

- Evaluate expressions: `len(my_list)`, `my_dict.keys()`
- Call functions: `some_function(different_argument)`
- Reassign variables: `x = 42` then continue, to test what would happen with a different value
- Test a fix before writing it: confirm your hypothesis in the live process, then go change the code

This is the most powerful tool in the debugger. "I think the problem might be X" goes from a speculation requiring a re-run to something you can verify in ten seconds without leaving the paused session.

### Exercise 5

Open `exercises/05_repl.py`. An encode/decode pair should round-trip text back to the original. The first word comes back correctly; the rest are garbled.

**Instructions:**
1. Set a breakpoint inside `decode` on the `shift = ...` line
2. Press `<Leader>dc`. Continue past the first iteration (i=0) until i=1
3. Open the REPL (`<Leader>d>`)
4. Check what `shift` is currently. Then try computing what the shift *should* be to correctly undo the encoding — look at how `encode` computed its shift for the same word position
5. Use the REPL to call `caesar_cipher(word, -correct_shift)` with your hypothesis and see if it decodes the word properly
6. Confirm the fix before touching the source file

---

## Putting It Together

These five tools cover the large majority of real debugging:

1. **Breakpoint** — stop near the problem
2. **Step over/into** — narrow down where the wrong value is produced
3. **Call stack** — understand the context the bad value came from
4. **Watch / evaluate** — query state to form a hypothesis
5. **REPL** — verify the hypothesis without restarting

The workflow is almost always: pause → step toward the wrong value → inspect state → REPL to confirm → fix.

The language sections apply these tools to non-trivial programs with language-specific wrinkles. Refer back here when a concept comes up — the mechanics don't change between Python, Rust, and C.

**Next:**
- [03 — Python](../03-python/README.md)
- [04 — Rust](../04-rust/README.md)
- [05 — C](../05-c/README.md)

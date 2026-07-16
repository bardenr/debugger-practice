# Python

This section assumes you've worked through [02-concepts](../02-concepts/concepts.md). The exercises here use the same tools but with more realistic programs and three Python-specific features the concept exercises didn't cover.

---

## Python-Specific Features

### 1. Exception Breakpoints

When a Python program **crashes**, the debugger stops at the exception site automatically — no setup needed. But when an exception is **caught and silenced** by a `try/except`, the program keeps running and you get nothing: no crash, no traceback, just wrong or missing output.

That's what `<Leader>dE` is for. It tells debugpy to pause the moment an exception is raised, before any `except` block gets a chance to handle it.

**Add this keymap to your `after/plugin/dap.lua`:**

```lua
map("<Leader>dE", function() dap.set_exception_breakpoints() end, "Debug: Exception Breakpoints")
```

When you press `<Leader>dE`, nvim-dap shows a picker:

| Filter | Pauses on |
|--------|-----------|
| `raised` | Every exception, including caught ones — use this when a try/except is swallowing something |
| `uncaught` | Only exceptions that crash the program (redundant — the debugger already stops there) |
| `userUncaught` | Exceptions not caught in *your* code; skips library internals |

**`raised` is what you reach for when output is wrong or missing but nothing crashes.** `userUncaught` is useful when you want to catch errors from your code that a library is swallowing.

**`<Leader>dE` requires an active session** — it sends a request to the debug adapter, so you can't set it before starting. The pattern is: set a regular staging breakpoint somewhere early in the file, start the session, wait for it to pause, then call `<Leader>dE`, then remove the staging breakpoint and continue.

To clear exception breakpoints: press `<Leader>dE` again and deselect all filters, or call `dap.set_exception_breakpoints({})` from the REPL.

> **`uncaught` vs `userUncaught` in a framework context**
>
> It's tempting to think your code is always at the top of the call stack — but frameworks invert this. A Flask route, a pytest test, or an asyncio task runs *inside* the framework's own call stack. When your code raises an exception, Flask or pytest catches it before it propagates any further. The process doesn't crash; the framework handles it gracefully and moves on.
>
> In that situation `uncaught` never fires (the framework caught it), but `userUncaught` does — because your code didn't catch it. Use `userUncaught` any time you're debugging code that runs inside a framework with its own error handling. Use `raised` only when you've narrowed it down to a specific `try/except` you control and want to catch before it silences the exception.

---

### 2. Virtual Environments

Never install packages into the system site-packages. For any real project — including these exercises — create a virtual environment first:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
```

The debug adapter needs to use the same Python as your project, or it won't find your dependencies. Update your `after/plugin/dap.lua` to pick up the active environment:

```lua
-- Respects the activated venv if you launched Neovim from that shell
require("dap-python").setup(vim.fn.exepath("python3"))
```

`vim.fn.exepath("python3")` resolves to whichever `python3` is first on `$PATH` — when a venv is activated, that's `.venv/bin/python3`. If you prefer to be explicit, point directly at the venv's binary:

```lua
require("dap-python").setup(vim.fn.getcwd() .. "/.venv/bin/python3")
```

Either way, activate the venv in your shell *before* launching Neovim and the debugger will use the right Python automatically.

> **Note on Mason's debugpy:** the `setup()` call you added in section 01 pointed at Mason's own debugpy venv. That's fine for running files with no external dependencies. Once you start working on a project with a venv, switch the argument to the venv's Python — that Python needs access to debugpy too, so either install it in the venv (`pip install debugpy`) or keep pointing at Mason's copy and just ensure your dependencies are also accessible. The simplest habit: `pip install debugpy pytest` into every new project venv.

#### Verifying your environment during a session

If behavior in the debugger doesn't match what you see running the file normally — missing imports, wrong values, unexpected versions — the first thing to check is whether the adapter is using the Python you think it is.

During any active session, open the REPL (`<Leader>d>`) and run:

```python
import sys; sys.executable
```

The output is the full path to the Python the adapter is actually using. If you expected a venv but see a system Python path, your `dap-python` setup call is pointing at the wrong interpreter.

---

### 3. Debugging Pytest Tests

`nvim-dap-python` can launch a single test under the debugger. Place your cursor inside a test function or class and use these keymaps:

**Add to `after/plugin/dap.lua`:**

```lua
local dap_python = require("dap-python")
map("<Leader>dtm", dap_python.test_method, "Debug: Test Method")
map("<Leader>dtc", dap_python.test_class,  "Debug: Test Class")
```

This runs pytest with debugpy attached. Any breakpoints you've set in the code under test will fire normally. You can step through the test body and into the functions it calls.

Install pytest into your project venv (not system Python):

```bash
source .venv/bin/activate
pip install pytest debugpy
```

---

### Stepping Into Generators

Generators behave a bit differently under the debugger. When you step into a generator call, you jump into the generator body at the `yield` point. Stepping again resumes the generator until the next `yield`, then returns to the caller. The call stack will show both the generator frame and the caller frame simultaneously — you can navigate between them to see both sides of the lazy evaluation.

---

## Exercises

| File | Concept | What you're finding |
|------|---------|---------------------|
| [`exercises/01_exception_crash.py`](exercises/01_exception_crash.py) | Default crash behavior | Which record in a batch causes a crash, and what its data looks like |
| [`exercises/02_exception_breakpoints.py`](exercises/02_exception_breakpoints.py) | Exception breakpoints (`<Leader>dE`) | Why a student's grade is silently dropped with no error shown |
| [`exercises/03_class_state.py`](exercises/03_class_state.py) | Stepping + watch + REPL | Why two separate object instances share state they shouldn't |
| [`exercises/04_generator.py`](exercises/04_generator.py) | Stepping + watch + REPL | Why a generator pipeline produces the same output for every row |

The constraint is the same as section 2: **no print statements**.

---

Next: [04 — Rust](../04-rust/README.md)

# Python

This section assumes you've worked through [02-concepts](../02-concepts/concepts.md). The exercises here use the same tools but with more realistic programs and three Python-specific features the concept exercises didn't cover.

---

## Python-Specific Features

### 1. Exception Breakpoints

A regular breakpoint requires you to know in advance where to stop. An **exception breakpoint** tells the debugger to pause the moment an exception is raised — before the stack unwinds — so you can inspect the full program state at the crash site.

This is especially valuable in Python because exceptions are used for control flow everywhere, and a vague traceback often tells you *what* crashed but not *why*.

**Add this keymap to your `after/plugin/dap.lua`:**

```lua
map("<Leader>dE", function() dap.set_exception_breakpoints() end, "Debug: Exception Breakpoints")
```

When you press `<Leader>dE` during a session (or before starting one), nvim-dap shows a picker with the exception filter options:

| Filter | Pauses on |
|--------|-----------|
| `raised` | Every exception, including ones that are caught and handled — very noisy |
| `uncaught` | Only exceptions that reach the top level and crash the program |
| `userUncaught` | Exceptions not caught in *your* code (won't stop on library internals) |

**`userUncaught` is the most useful starting point.** It skips exceptions that are caught and handled normally, and stops on anything that bubbles up through your code uncaught.

To clear exception breakpoints, call `dap.set_exception_breakpoints({})` (empty table).

---

### 2. Debugging Pytest Tests

`nvim-dap-python` can launch a single test under the debugger. Place your cursor inside a test function or class and use these keymaps:

**Add to `after/plugin/dap.lua`:**

```lua
local dap_python = require("dap-python")
map("<Leader>dtm", dap_python.test_method, "Debug: Test Method")
map("<Leader>dtc", dap_python.test_class,  "Debug: Test Class")
```

This runs pytest with debugpy attached. Any breakpoints you've set in the code under test will fire normally. You can step through the test body and into the functions it calls.

Requires `pytest` in the same environment as your project (`pip install pytest`).

---

### 3. Virtual Environments

If your project uses a virtual environment, the debug adapter needs to use the same Python — otherwise it won't find your dependencies.

The `dap-python` setup call in `after/plugin/dap.lua` accepts a path:

```lua
-- Use whatever python is active in the shell (respects venv if activated)
require("dap-python").setup(vim.fn.exepath("python3"))

-- Or point directly at a venv's python
require("dap-python").setup("/path/to/your/venv/bin/python")
```

If you use a tool like `direnv` or activate venvs in your shell, the `vim.fn.exepath("python3")` form picks up the active environment automatically when you launch Neovim from that shell.

---

### Stepping Into Generators

Generators behave a bit differently under the debugger. When you step into a generator call, you jump into the generator body at the `yield` point. Stepping again resumes the generator until the next `yield`, then returns to the caller. The call stack will show both the generator frame and the caller frame simultaneously — you can navigate between them to see both sides of the lazy evaluation.

---

## Exercises

| File | Concept | What you're finding |
|------|---------|---------------------|
| [`exercises/01_exception_breakpoints.py`](exercises/01_exception_breakpoints.py) | Exception breakpoints | Which record in a batch causes a crash, and what its data looks like |
| [`exercises/02_class_state.py`](exercises/02_class_state.py) | Stepping + watch + REPL | Why two separate object instances share state they shouldn't |
| [`exercises/03_generator.py`](exercises/03_generator.py) | Stepping + watch + REPL | Why a generator pipeline produces the same output for every row |

The constraint is the same as section 2: **no print statements**.

---

Next: [04 — Rust](../04-rust/README.md)

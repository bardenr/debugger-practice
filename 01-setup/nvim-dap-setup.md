# Setting Up nvim-dap

nvim-dap implements the [Debug Adapter Protocol](https://microsoft.github.io/debug-adapter-protocol/) (DAP) in Neovim. DAP is the same protocol that powers VS Code's debugger — a language-agnostic JSON-RPC protocol between the editor and a language-specific **debug adapter** process. The adapters are the same ones VS Code uses; only the UI is different.

You need three things:
1. **nvim-dap** — the core plugin (protocol implementation + API)
2. **nvim-dap-ui** — a UI that renders the call stack, variables, breakpoints, etc.
3. **A debug adapter** for each language

---

## Plugin Installation

Neovim's built-in package manager (`:h packages`) loads any plugin placed under `~/.config/nvim/pack/*/start/` automatically at startup. No plugin manager binary needed — just git clone.

```bash
mkdir -p ~/.config/nvim/pack/plugins/start
cd ~/.config/nvim/pack/plugins/start

git clone https://github.com/mfussenegger/nvim-dap.git
git clone https://github.com/rcarriga/nvim-dap-ui.git
git clone https://github.com/nvim-neotest/nvim-nio.git        # required by nvim-dap-ui
git clone https://github.com/mfussenegger/nvim-dap-python.git
git clone https://github.com/williamboman/mason.nvim.git
git clone https://github.com/jay-babu/mason-nvim-dap.nvim.git
```

To update plugins later: `git pull` inside each directory, or loop it:

```bash
for d in ~/.config/nvim/pack/plugins/start/*/; do git -C "$d" pull; done
```

### Configuration

Put the configuration in `~/.config/nvim/after/plugin/dap.lua`. Files in `after/plugin/` are sourced after all `pack/*/start/` plugins are loaded, so every `require()` call will resolve correctly.

```lua
-- ~/.config/nvim/after/plugin/dap.lua

local dap = require("dap")
local dapui = require("dapui")

-- ── Mason: install debug adapters ────────────────────────────────────────────
-- Run :Mason after first launch to confirm these are installed.
require("mason").setup()
require("mason-nvim-dap").setup({
  ensure_installed = {
    "python",   -- installs debugpy
    "codelldb", -- installs codelldb (used for Rust and C)
  },
  automatic_installation = true,
})

-- ── UI ────────────────────────────────────────────────────────────────────────
dapui.setup()

-- Open the UI automatically when a session starts, close it when it ends.
dap.listeners.before.attach.dapui_config = function() dapui.open() end
dap.listeners.before.launch.dapui_config = function() dapui.open() end
dap.listeners.before.event_terminated.dapui_config = function() dapui.close() end
dap.listeners.before.event_exited.dapui_config = function() dapui.close() end

-- ── Python ────────────────────────────────────────────────────────────────────
-- Mason installs debugpy into its own virtual environment, not into your system
-- Python. We have to point dap-python at Mason's venv python explicitly,
-- otherwise it looks in the system Python and can't find debugpy.
require("dap-python").setup(vim.fn.stdpath("data") .. "/mason/packages/debugpy/venv/bin/python")

-- ── Rust ──────────────────────────────────────────────────────────────────────
-- codelldb is an LLDB-based adapter. Mason installs it and puts it on PATH.
dap.adapters.codelldb = {
  type = "server",
  port = "${port}",
  executable = {
    command = vim.fn.exepath("codelldb"),
    args = { "--port", "${port}" },
  },
}

dap.configurations.rust = {
  {
    name = "Launch",
    type = "codelldb",
    request = "launch",
    -- Prompts for the binary each time. For a cargo project this is
    -- typically target/debug/<project-name>.
    program = function()
      return vim.fn.input("Binary: ", vim.fn.getcwd() .. "/target/debug/", "file")
    end,
    cwd = "${workspaceFolder}",
    stopOnEntry = false,
  },
}

-- ── C (and C++) ───────────────────────────────────────────────────────────────
-- Reuses codelldb — same adapter, same configuration shape.
dap.configurations.c = {
  {
    name = "Launch",
    type = "codelldb",
    request = "launch",
    program = function()
      return vim.fn.input("Binary: ", vim.fn.getcwd() .. "/", "file")
    end,
    cwd = "${workspaceFolder}",
    stopOnEntry = false,
  },
}
dap.configurations.cpp = dap.configurations.c

-- ── Keymaps ───────────────────────────────────────────────────────────────────
local map = function(key, fn, desc)
  vim.keymap.set("n", key, fn, { desc = desc })
end

-- Session control
map("<F5>",       dap.continue,         "Debug: Continue / Start")
map("<F10>",      dap.step_over,        "Debug: Step Over")
map("<F11>",      dap.step_into,        "Debug: Step Into")
map("<F12>",      dap.step_out,         "Debug: Step Out")
map("<Leader>dq", dap.terminate,        "Debug: Terminate")
map("<Leader>dr", dap.restart,          "Debug: Restart")

-- Breakpoints
-- Note: <Leader>db is intentionally skipped — reserved for dadbod-ui.
map("<Leader>dp", dap.toggle_breakpoint, "Debug: Toggle Breakpoint")
map("<Leader>dw", function()             -- w = "when (this condition is true)"
  dap.set_breakpoint(vim.fn.input("Condition: "))
end, "Debug: Conditional Breakpoint")
map("<Leader>dl", function()
  dap.set_breakpoint(nil, nil, vim.fn.input("Log message: "))
end, "Debug: Logpoint")

-- UI
map("<Leader>du", dapui.toggle,         "Debug: Toggle UI")
map("<Leader>de", dapui.eval,           "Debug: Evaluate Expression")

-- Breakpoint list management
map("<Leader>dL", dap.list_breakpoints, "Debug: List Breakpoints")
map("<Leader>dC", dap.clear_breakpoints,"Debug: Clear All Breakpoints")

-- REPL
map("<Leader>d>", dap.repl.open,        "Debug: Open REPL")
```

---

## What Each Keymap Does

| Key | Action | When to use |
|-----|--------|-------------|
| `<F5>` | Continue | Start the session, or resume from a breakpoint |
| `<F10>` | Step over | Execute the current line; if it's a function call, run the whole function without entering it |
| `<F11>` | Step into | If the current line calls a function, jump into that function |
| `<F12>` | Step out | Run until the current function returns, then pause |
| `<Leader>dp` | Toggle breakpoint | Set or clear a breakpoint on the current line |
| `<Leader>dw` | Conditional breakpoint | Only pause when an expression is true (e.g. `i == 42`) |
| `<Leader>dl` | Logpoint | Print a message to the console without stopping |
| `<Leader>de` | Evaluate | Evaluate an expression in the current scope and show the result |
| `<Leader>du` | Toggle UI | Show/hide the dap-ui panels |
| `<Leader>d>` | Open REPL | Run arbitrary code in the paused context |

> **On key sequence collisions:** Neovim sequences like `<Leader>dB`, `<Leader>du`, `<Leader>dr` do not conflict with each other — they are distinct sequences. The only kind of conflict would be mapping `<Leader>d` to something *and* having `<Leader>d*` sequences, or two mappings that are byte-for-byte identical. `<Leader>db` (dadbod) and `<Leader>dB` (our toggle breakpoint) are different and coexist without issue.

---

## Verifying the Setup

### Python

Create a test file:

```python
# /tmp/test.py
def add(a, b):
    return a + b

result = add(2, 3)
print(result)
```

Open it in Neovim, set a breakpoint on the `return` line with `<Leader>dp`, then press `<F5>`. Choose "Python: Current File" from the picker. The UI should open and execution should pause on the breakpoint.

### C

```c
// /tmp/test.c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(2, 3);
    printf("%d\n", result);
    return 0;
}
```

Compile with debug symbols: `gcc -g -o /tmp/test /tmp/test.c`

Open `test.c` in Neovim, set a breakpoint with `<Leader>dp`, press `<F5>`, and enter `/tmp/test` when prompted for the binary path.

> **Important:** Always compile C and Rust with debug symbols (`-g` for C, the default `cargo build` for Rust). Without them, the adapter has no line/variable information to work with.

### Rust

```bash
cargo new /tmp/rust-test && cd /tmp/rust-test
```

Edit `src/main.rs`, set a breakpoint with `<Leader>dp`, press `<F5>`, and enter `target/debug/rust-test` when prompted. Run `cargo build` first.

---

## Adapter Reference for Future Languages

These are notes only — no tutorials are planned for these languages, but this is how you'd add them.

### Go

Install [delve](https://github.com/go-delve/delve):

```bash
go install github.com/go-delve/delve/cmd/dlv@latest
```

Clone [`leoluz/nvim-dap-go`](https://github.com/leoluz/nvim-dap-go) into your pack directory and call `require("dap-go").setup()` in your dap config. It handles adapter registration automatically.

### JavaScript / TypeScript

Add `"js"` to mason-nvim-dap's `ensure_installed`. This installs `vscode-js-debug`. Then clone [`mxsdev/nvim-dap-vscode-js`](https://github.com/mxsdev/nvim-dap-vscode-js) and configure it. You'll need separate `dap.configurations` entries for `javascript`, `typescript`, `javascriptreact`, and `typescriptreact`.

### C++

No additional setup — `dap.configurations.cpp = dap.configurations.c` (already in the config above) makes C++ share codelldb with C.

### Zig

Zig has no official DAP adapter. In practice, codelldb works for Zig binaries compiled in debug mode (`zig build` defaults to debug). Add a configuration block in your dap config:

```lua
dap.configurations.zig = {
  {
    name = "Launch",
    type = "codelldb",
    request = "launch",
    program = function()
      return vim.fn.input("Binary: ", vim.fn.getcwd() .. "/zig-out/bin/", "file")
    end,
    cwd = "${workspaceFolder}",
    stopOnEntry = false,
  },
}
```

---

## Troubleshooting

**The UI doesn't open:** Check that `nvim-nio` is installed — it's a required dependency of nvim-dap-ui that's easy to miss.

**"No configuration found for filetype":** You started a debug session in a file type that doesn't have a `dap.configurations` entry. Make sure the file you're in matches the language (e.g. a `.py` file for Python).

**Breakpoints show as unverified (grey, not red):** The adapter hasn't confirmed it can resolve the breakpoint. For C, this usually means the binary was compiled without `-g`. For Python, it can mean debugpy isn't installed in the Python the adapter is using.

**codelldb not found:** Run `:Mason` and check that codelldb is installed. If `vim.fn.exepath("codelldb")` returns empty, Mason may not have its bin directory on Neovim's PATH — confirm with `:echo $PATH` inside Neovim.

---

Next: [02 — Core Concepts](../02-concepts/concepts.md)

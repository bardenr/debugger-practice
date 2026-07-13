# Debugger Practice

A structured self-paced course for building real fluency with debuggers in Neovim.

## Learning Path

| Module | Language | What You'll Learn |
|--------|----------|-------------------|
| [01 — Setup](01-setup/nvim-dap-setup.md) | — | Install and configure nvim-dap, nvim-dap-ui, and adapters for all three languages |
| [02 — Core Concepts](02-concepts/concepts.md) | Python | Breakpoints, stepping, call stack, watch expressions, conditional breakpoints, the REPL |
| [03 — Python](03-python/README.md) | Python | Exercises that deepen the concepts from module 02 |
| [04 — Rust](04-rust/README.md) | Rust | Debugging with codelldb, inspecting enums and ownership |
| [05 — C](05-c/README.md) | C | Memory debugging, core dumps, pointer inspection |

Work through the modules in order. Each language section assumes you've done module 02 and references it rather than re-explaining concepts.

## Philosophy

The goal is to stop reaching for `print` statements. Every exercise has a specific bug to find and a constraint: **no adding print statements**. You must find the answer using only the debugger.

## Prerequisites

- Neovim 0.9+
- A plugin manager — examples use [lazy.nvim](https://github.com/folke/lazy.nvim)
- For Rust: `rustup` and a working Rust toolchain
- For C: `gcc` or `clang`, `make`
- For Python: Python 3.8+

Start with [01-setup](01-setup/nvim-dap-setup.md).

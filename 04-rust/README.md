# Rust

This section assumes you've worked through [02-concepts](../02-concepts/concepts.md). The core tools are the same — breakpoints, stepping, call stack, watch, REPL — but Rust has a few wrinkles worth knowing before you try to debug it.

---

## Rust-Specific Features

### Build Mode

Always build in debug mode when debugging. It's the default — just `cargo build`. Debug mode includes full symbol information and disables optimizations that cause variables to vanish from the locals panel.

```bash
cargo build            # debug mode — use this for debugging
cargo build --release  # strips symbols — debugger works poorly
```

When the debugger prompts for a binary path, it will be under `target/debug/`.

### Reading Rust Types

codelldb has built-in pretty-printers for Rust's standard types. In the Locals panel:

| Type | What it looks like |
|------|--------------------|
| `Vec<T>` | Expandable list of elements |
| `Option<T>` | `Some(value)` or `None` |
| `Result<T, E>` | `Ok(value)` or `Err(message)` |
| Custom enum | Variant name + any contained data |
| `String` / `&str` | The string contents directly |
| `HashMap<K, V>` | Expandable list of key-value pairs |

If you see garbled output or `<optimized out>` for variables, check that you built in debug mode.

### Stepping Into Closures

When a line contains a closure, `<Leader>ds` (step into) takes you inside the closure body. The closure's arguments and any captured variables are visible in the Locals panel. `<Leader>df` (step out) returns you to the caller.

In an iterator chain (`data.iter().filter(...).map(...).sum()`), each `.map()` and `.filter()` call is a separate closure. Step over the chain until the output is wrong, then restart and step into the specific closure that's misbehaving.

### Panics

When Rust panics, the stack unwinds and all local state is gone by the time you see the message. To inspect state at the moment of a panic:

1. Set a breakpoint just before the panicking line
2. Step up to it and inspect locals before it executes
3. Use the REPL to evaluate sub-expressions

Common panic sources: `.unwrap()` on `None` or `Err`, index out of bounds (`vec[i]` where `i >= len`), integer overflow (in debug mode), explicit `panic!()`.

Running with `RUST_BACKTRACE=1` outside the debugger gives a fuller stack trace — useful for finding where to set your first breakpoint before launching the debug session.

---

## Project Structure

The exercises share a single Cargo project with multiple binaries.

```
04-rust/
├── Cargo.toml
└── src/
    └── bin/
        ├── 01_iterators.rs
        ├── 02_enums.rs
        └── 03_panic.rs
```

Build everything at once:

```bash
cd 04-rust
cargo build
```

When prompted for the binary path, enter one of:
- `target/debug/01_iterators`
- `target/debug/02_enums`
- `target/debug/03_panic`

---

## Exercises

| File | What you're practicing | What you're finding |
|------|----------------------|---------------------|
| `src/bin/01_iterators.rs` | Stepping into closures | Which operation in an iterator chain computes the wrong value |
| `src/bin/02_enums.rs` | Reading `Result` variants in the locals panel | How an `Err` case is mishandled, corrupting the output |
| `src/bin/03_panic.rs` | Inspecting `Option` state before a panic | Which key is missing from config and why `.unwrap()` fails |

Constraint: no `println!` or `dbg!` macros.

---

Next: [05 — C](../05-c/README.md)

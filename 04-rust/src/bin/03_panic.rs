// Exercise 3: Inspecting State Before a Panic
//
// A config lookup panics at runtime. The panic message tells you the line,
// but not which key triggered it or what the data looked like at that moment.
//
// Instructions:
//   1. Run without the debugger first to see the panic message:
//      cargo run --bin 03_panic
//      Note what it tells you — and what it doesn't.
//   2. Set a breakpoint on the `value.unwrap()` line inside find_config_value
//   3. cargo build, then press <Leader>dc and enter: target/debug/03_panic
//   4. Continue past the successful lookups with <Leader>dc
//   5. When it pauses and the Locals panel shows something unexpected for
//      `value`, you've found the failing call
//   6. What is the Option variant shown for `value`?
//   7. Open the REPL and evaluate `key` — which key triggered the panic?
//
// Constraint: no println! or dbg! macros.

fn find_config_value(configs: &[(&str, &str)], key: &str) -> String {
    let found = configs.iter().find(|(k, _)| *k == key);
    let value = found.map(|(_, v)| v.to_string());
    value.unwrap()
}

fn main() {
    let config = vec![
        ("host", "localhost"),
        ("port", "8080"),
        ("timeout", "30"),
    ];

    let keys = ["host", "port", "debug_mode", "timeout"];

    for key in &keys {
        let value = find_config_value(&config, key);
        println!("{} = {}", key, value);
    }
}

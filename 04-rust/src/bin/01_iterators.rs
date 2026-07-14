// Exercise 1: Stepping Into Closures
//
// This program should compute the sum of squares of all positive numbers
// in a list. The result is wrong.
//
// Instructions:
//   1. cargo build (from the 04-rust directory)
//   2. Set a breakpoint on the .map() closure line (the |&x| line)
//   3. Press <Leader>dc and enter: target/debug/01_iterators
//   4. Each time the debugger pauses inside the closure, inspect `x` in
//      the Locals panel, then evaluate the expression on that line.
//      Does it produce a square?
//
// Tip: you can also set a breakpoint on the `let result` line, press <Leader>ds
// to step into the iterator chain, and navigate through it that way.
//
// Constraint: no println! or dbg! macros.

fn main() {
    let data: Vec<i32> = vec![3, -1, 4, -1, 5, -9, 2, 6, -5, 3];

    // Sum of squares of all positive numbers.
    // Positive values: 3, 4, 5, 2, 6, 3
    // Squares:         9, 16, 25, 4, 36, 9  → sum = 99
    let result: i32 = data
        .iter()
        .filter(|&&x| x > 0)
        .map(|&x| x + x)
        .sum();

    println!("Sum of squares of positives: {}", result);
    // Expected: 99
}

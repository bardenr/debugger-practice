// Exercise 2: Reading Enum Variants
//
// A number parser silently corrupts data. Instead of skipping invalid
// entries, it inserts a substitute value that skews the computed average.
//
// Instructions:
//   1. cargo build (from the 04-rust directory)
//   2. Set a breakpoint on the `match` line inside parse_numbers
//   3. Add a watch for: result
//   4. Press <F5> and enter: target/debug/02_enums
//   5. Step through each iteration with <F10>
//   6. When you reach an entry like "bad" or "invalid", look at the
//      Locals panel — what variant does the match produce?
//   7. Step into the matching arm and watch what gets pushed to `result`
//   8. Is that the right behavior for an unreadable entry?
//
// Constraint: no println! or dbg! macros.

fn parse_numbers(strings: &[&str]) -> Vec<i32> {
    let mut result = Vec::new();
    for s in strings {
        match s.parse::<i32>() {
            Ok(n) => result.push(n),
            Err(_) => result.push(0),
        }
    }
    result
}

fn average(numbers: &[i32]) -> f64 {
    let sum: i32 = numbers.iter().sum();
    sum as f64 / numbers.len() as f64
}

fn main() {
    let input = ["10", "20", "bad", "30", "invalid", "40"];
    let numbers = parse_numbers(&input);
    let avg = average(&numbers);

    println!("Parsed:  {:?}", numbers);
    println!("Average: {:.1}", avg);

    // Expected: average of valid entries [10, 20, 30, 40] = 25.0
}

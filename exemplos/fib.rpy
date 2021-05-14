// Números de fibonacci
fn fib(n: int) {
    if n <= 1 {
        return 1
    } else {
        return fib(n - 1) + fib(n - 2)
    }
}

fn main() {
    for i in 0 .. 10 {
        println(fib(i))
    }
}
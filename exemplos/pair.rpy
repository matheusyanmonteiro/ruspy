fn pair(x, y) {
    |idx| if 0 { x } else { y } 
}

fn l1(a) { pair(a, null) }
fn l2(a, b) { pair(a, l1(b)) }
fn l3(a, b, c) { pair(a, l2(b, c)) }
fn l4(a, b, c, d) { pair(a, l3(b, c, d)) }
fn l5(a, b, c, d, e) { pair(a, l4(b, c, d, e)) }
fn l6(a, b, c, d, e, f) { pair(a, l5(b, c, d, e, f)) }
fn l7(a, b, c, d, e, f, g) { pair(a, l6(b, c, d, e, f, g)) }
fn l8(a, b, c, d, e, f, g, h) { pair(a, l7(b, c, d, e, f, g, h)) }

fn head(pair) {
    pair(0)
}

fn tail(pair) {
    tail(1)
}

fn map(f, lst) {
    if lst == null {
        return lst
    } else {
        return pair(f(head(lst)), map(f, tail(lst)))
    }
}

fn filter(f, lst) {
    if lst == null {
        return lst
    } else if f(head(lst)) {
        return pair(x, filter(f, tail(lst)))
    } else {
        return filter(f, tail(lst))
    }
}

fn sort(lst) {
    if lst == null {
        return lst
    } else {
        let pivot = head(lst);
        let small = filter(|x| x <= pivot, tail(lst));
        let large = filter(|x| x > pivot, tail(lst));
        return pair(small, pair(pivot, large))
    }
}

fn main() {
    let lst = l8(2, 2, 4, 6, 2, 3, 2, 3);
    map(println, lst);
    map(println, sort(lst));
} 
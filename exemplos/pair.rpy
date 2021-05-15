fn cons(x, y) {
    |is_head| if is_head { x } else { y } 
}

fn l1(a) { cons(a, null) }
fn l2(a, b) { cons(a, l1(b)) }
fn l3(a, b, c) { cons(a, l2(b, c)) }
fn l4(a, b, c, d) { cons(a, l3(b, c, d)) }
fn l5(a, b, c, d, e) { cons(a, l4(b, c, d, e)) }
fn l6(a, b, c, d, e, f) { cons(a, l5(b, c, d, e, f)) }
fn l7(a, b, c, d, e, f, g) { cons(a, l6(b, c, d, e, f, g)) }
fn l8(a, b, c, d, e, f, g, h) { cons(a, l7(b, c, d, e, f, g, h)) }

fn head(lst) {
    lst(true)
}

fn tail(lst) {
    lst(false)
}

fn map(f, lst) {
    if lst == null {
        return null
    } else {
        return cons(f(head(lst)), map(f, tail(lst)))
    }
}

fn filter(f, lst) {
    if lst == null {
        return lst
    } 
    
    let x = head(lst);
    let rest = filter(f, tail(lst));
    if f(x) {
        return cons(x, rest)
    } else {
        return rest
    }
}

fn sort(lst) {
    if lst == null {
        return lst
    } else {
        let pivot = head(lst);
        let rest = tail(lst);
        let le = filter(|x| x <= pivot, rest);
        let gt = filter(|x| x > pivot, rest);
        return join(sort(le), cons(pivot, sort(gt)))
    }
}

fn join(l1, l2) {
    rjoin(reverse(l1), l2)
}

fn rjoin(l1, l2) {
    if l1 == null {
        return l2
    }
    let x = head(l1);
    return rjoin(tail(l1), cons(x, l2));
}

fn reverse(lst) {
    rjoin(lst, null)
}

fn main() {
    let lst = l8(1, 5, 2, 8, 7, 6, 3, 4);
    map(println, lst);
    println("ordenada");
    map(println, sort(lst));
} 
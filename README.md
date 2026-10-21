lambda-calculus-from-scratch

Alonzo Church didn't make Lambda Calculus for nothing. Rebuilding it from a single primitive — the function — in Python, because my crush wished me luck and that was somehow enough activation energy to spend a weekend reinventing computation.

No if. No for/while. No int, bool, or list as primitives. Just functions closing over functions, all the way down.

What's actually in here

Lambda calculus (Church, 1936) has exactly one building block: the function. Everything else — booleans, numbers, pairs, lists, recursion — gets encoded on top of it rather than borrowed from the host language. This repo builds that encoding in Python, then pushes it one step further into monadic IO.

1. Church encodings

    Booleans — TRUE/FALSE aren't values, they're functions that pick between two arguments: TRUE = λx.λy.x
    Numerals — a number is "apply this function n times": TWO = λf.λx.f(f(x))
    Logic — NOT/AND/OR built purely from boolean dispatch, no boolean type involved
    Pairs / lists — CONS/CAR/CDR/NIL built from closures, with a to_church_list helper to lift a normal Python list into one
    Recursion — the Y-combinator, for recursion without giving a lambda a name to call itself by
    Worked examples — summing a list and filtering even numbers, without +-as-primitive-control-flow, %, or a single if

2. Monadic IO

print() is impure — it reaches outside your program to touch the real world (stdout), and its return value tells you nothing about what it did. Two calls to print("hi") aren't interchangeable with one, which breaks referential transparency — the whole premise church.py is built to protect.

The fix isn't pretending print is pure. It's never actually running it inside your program: build a pure value that describes the effect, chain those descriptions together, and defer running the description to exactly one point at the very edge of the program.

    IO — wraps an unexecuted action (building one does nothing)
    bind — chains IO descriptions without running anything
    run() — the single impure line in the entire program

3. Monad design pattern (MonadDesignPattern.py)

A concrete, standalone illustration of the Maybe monad as a design pattern — the same abstraction the IO section leans on, stripped down to its essentials and made runnable in isolation.

The file wraps a value in a type (`Just` or `Nothing`) so that pipeline steps can be composed without a single `None` check in the calling code:

    Just — holds a value; bind runs the continuation, map lifts a pure function, or_else extracts with a fallback
    Nothing — short-circuits every bind/map, so downstream functions never run
    >> — the bind operator, letting you chain `Just(uid) >> find_user >> get_addr >> get_city`
    lift — turns a pure function into a Kleisli arrow (A -> M B)
    maybe — adapter from the None-returning world into the monad

The demo (`city_of`) resolves a user's city through three lookups that can each fail, with zero explicit null checks — the failure handling lives entirely in the type. The file also asserts the three monad laws (left identity, right identity, associativity) plus the Nothing short-circuit, so it doubles as a spec.

Why this is a bit unhinged

Python is eager: it evaluates every argument before a function call. Lambda calculus, in spirit, is lazy: it never touches a branch until one is chosen. Miss that distinction by a single un-thunked lambda and a "pure" church-encoded function recurses straight off the end of a list and blows the stack. Most of the bugs in this repo's history were exactly that — not wrong logic, wrong assumptions about which language's evaluation rules were actually running.

Usage

python3 madlad.py              # church encodings + monadic IO
python3 MonadDesignPattern.py  # Maybe monad demo + monad law checks

No dependencies — standard library only.

Sanity check

In Haskell, this pattern is production reality: the type system statically enforces that effectful code can't sneak into pure code. In Python, it's closer to theater — nothing stops you from cheating, since there's no compiler standing at the door. But building the theater by hand is the fastest way to actually feel the idea instead of just reading about it. The Maybe monad in MonadDesignPattern.py is the same story in miniature: the discipline of never unwrapping early is what buys you the clean, declarative pipeline — Python won't enforce it for you.

License

MIT. Do whatever you want with it — Church would've open-sourced it too.

Author: Stanislaw

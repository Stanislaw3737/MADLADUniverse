# Alonzo Church Didn't make LCalculus for nothing
# Remaking lambda Calculus from scratch
# (cause my crush wished me luck, and that got me fired up)

# Author - Stanislaw


# JUST WATCH ME CREATE THE UNIVERSE


#---- Church Booleans -----------------------------------------

TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y

def church_to_bool(church_bool):        # For display purposes for non-nerds
    return church_bool(True)(False)

#---- Church Numerals -----------------------------------------
# We are gonna create numbers: works something like this:
# 0 = λ f. λ x. x
# 1 = λ f. λ x. f(x)
# 2 = λ f. λ x. f(f(x))


ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
TWO = lambda f: lambda x: f(f(x))

def church_to_int(n):
    return n(lambda x: x + 1)(0)

def int_to_church(n):
    if n == 0:
        return ZERO
    return lambda f: lambda x: f(int_to_church(n - 1)(f)(x))

#---- Logical Operators (Pure functions) ---------------
# NOT = λ b. λ(FALSE)(TRUE)
# AND = λ a. λ b. a(b)(FALSE)
# OR = λ a. λ b. a(TRUE)(b)

NOT = lambda b: b(FALSE)(TRUE)
AND = lambda a: lambda b: a(b)(FALSE)
OR = lambda a: lambda b: a(TRUE)(b)

#---- Predicates (functions that return Church booleans -------------
# IS_ZERO = λ n. n(λ x. FALSE)(TRUE)

IS_ZERO = lambda n: n(lambda x: FALSE)(TRUE)

#---- Pairs / Cons Cells (For list operations)
# CONS = λ x. λ y. λ f. f(x)(y)
# CAR = λ p. p(TRUE)
# CDR = λ p. p(FALSE)

CONS = lambda x: lambda y: lambda f: f(x)(y)
CAR = lambda p: p(TRUE)
CDR = lambda p: p(FALSE)
NIL = lambda f: TRUE
IS_NIL = lambda l: l(lambda x: lambda y: FALSE)

# A thing to note: CONS/CAR/CDR/IS_NIL only understand Church-encoded lists
# (nested CONS cells), never plain Python lists. This helper builds
# a real Church list out of a Python one, so the functions below
# actually get the kind of value they expect.
def to_church_list(pylist):
    result = NIL
    for x in reversed(pylist):
        result = CONS(x)(result)
    return result

#---- And finally, The Y-Combinator (recursion mechanism, not the company)
# Don't wanna fry your brains, just basic Python recursion is fine
# Observe...

Y = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda x: f(lambda v: x(x)(v))))


#----- DONE --------- You have everything that you need to compute anything (yes, ANYTHING)
#----- Don't get surprised if you don't see if, or for/while anywhere------------



# EXAMPLE 1 - Sum of all elements in a list

# A thing to Note: Languages that simulate the Lambda Calculus are lazily evaluated
# Python is eager, not lazy. IS_NIL(lst)(branch_a)(branch_b) will
# evaluate BOTH branch_a and branch_b before picking one - so an un-thunked
# recursive call runs even in the base case and recurses off the end of the
# list. Wrapping each branch in `lambda: ...` and calling the result with
# `()` defers evaluation until after the Church boolean has chosen a branch.


def summ_pure(lst):
    # No if statements required
    return IS_NIL(lst)(
        lambda: 0
    )(
        lambda: CAR(lst) + summ_pure(CDR(lst))
    )()

print("Sum [1, 2, 3, 4, 5]: ", summ_pure(to_church_list([1, 2, 3, 4, 5])))

# EXAMPLE 2 - Filter even numbers (WITHOUT 'if' or % operator)
# If you do [x for x in lst if x%2 == 0], you are worthy for this religion
# but not enough

def mod_pure(a, b):
    # Modulus as repeated subtraction
    if a < b:
        return a
    return mod_pure(a - b, b)

# shit, I used if...not again

# same eager-evaluation trap as summ_pure above - both branches
# need to be thunks or this recurses forever once a < b.
def mod_church(a, b):
    # Modulus using Church booleans
    condition = TRUE if a < b else FALSE

    return condition(
        lambda: a
    )(
        lambda: mod_church(a - b, b)
    )()

print("mod_church(17, 5): ", mod_church(17, 5))

# Actually, go full Church Numerals for comparision
# Another note (here me out): This computed m <= n (via IS_ZERO of raw m - n), not m < n, and
# would crash (TypeError) if n > m, since IS_ZERO expects a Church numeral,
# not a plain negative int. True strict less-than needs the Church PRED /
# monus-based SUB.
def less_than_church(m, n):
    raise NotImplementedError("TODO: needs Church PRED/SUB, not raw int subtraction")

# EVEN Predicate (Pure function)

def is_even_church(n):
    def mod_two(x):
        if x < 2:
            return x
        return mod_two(x - 2)

    return TRUE if mod_two(n) == 0 else FALSE

# But we want Pure Church

def is_even_pure(n):
    # Church encoding throughout

    def mod_two_pure(x):
        return TRUE if x == 0 else (
            TRUE if x == 1 else mod_two_pure(x - 2)
        )

    result = mod_two_pure(n)
    return result

# FILTER with Church conditionals

def filter_pure(predicate, lst):
    # predicates return TRUE or FALSE (which are functions, dw)

    return IS_NIL(lst)(
        lambda: NIL
    )(
        # Recursive case
        lambda: predicate(CAR(lst))(
            # If true, include element
            lambda: CONS(CAR(lst))(filter_pure(predicate, CDR(lst)))
        )(
            # If false, skip element
            lambda: filter_pure(predicate, CDR(lst))
        )()
    )()

# Let's simplify that syntax

def filter_church(predicate, lst):
    # Clean version: predicate returns a Church boolean, which selects between two branches
    if not lst:
        return []

    head, tail = lst[0], lst[1:]

    # predicate(head) returns TRUE or FALSE
    return predicate(head)(
        [head] + filter_church(predicate, tail)
    )(
        filter_church(predicate, tail)
    )

# EVEN PREDICATE returning Church boolean

def even_predicate(x):
    return TRUE if x % 2 == 0 else FALSE

print("Filter even [1, 2, 3, 4, 5, 6]: ",
      filter_church(even_predicate, [1, 2, 3, 4, 5, 6]))

# MONADS by Stanislaw

# MONADS - are a design pattern in which pipeline implementations
# are abstracted away by wrapping the value to a type

# Below is an example of implementation of the Maybe MONAD
# As you can see in the main function, the code becomes far more simpler
# than if you had to manually check for Null values

# Also, you can also see that the code in the main function is declarative
# That is the essense of functional programming


from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, Union

A = TypeVar("A")
B = TypeVar("B")

@dataclass(frozen=True)
class Just(Generic[A]):
    value: A

    def bind(self, f: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        return f(self.value)            # run continuation on the value

    def map(self, f: Callable[[A], B]) -> "Maybe[B]":
        return Just(f(self.value))      # = bind (lambda a : Just(f(a)))

    def or_else(self, default: A) -> A:
        return self.value

    __rshift__ = bind                   # m >> f


@dataclass(frozen=True)
class Nothing:
    def bind(self, f) -> "Nothing":
        return self                     # short-circuits - f never runs

    def map(self, f) -> "Nothing":
        return self

    def or_else(self, default):
        return default

    __rshift__ = bind

Maybe = Union[Just[A], Nothing]

def lift(f: Callable[[A], B]) -> Callable[[A], Maybe[B]]:
    """ Pure function -> Kleisli arrow (A -> M B). """
    return lambda a: Just(f(a))

def maybe(value: A | None) -> Maybe[A]:
    """Adapter from None-returning world into the Monad. """
    return Nothing() if value is None else Just(value)

# ----- Demo: The pipeline has no None checks ----------------------

DB = {"u1":
      {"name": "ada",
       "addr": {"city": "london"}},
      "u2": {"name": "bob"}}

def find_user(uid: str) -> Maybe[dict]:
    return maybe(DB.get(uid))

def get_addr(user: dict) -> Maybe[dict]:
    return maybe(user.get("addr"))

def get_city(addr: dict) -> Maybe[dict]:
    return maybe(addr.get("city"))

def city_of(uid: str) -> str:
    return (
        Just(uid)
        >> find_user
        >> get_addr
        >> get_city
        >> lift(str.upper)
        ).or_else("Unknown")

if __name__ == "__main__":
    print(city_of("u1"))
    print(city_of("u2"))    # UNKNOWN (no addr)
    print(city_of("u3"))    # UNKNOWN (no user)

    # laws
    f = lambda x: Just(x + 1)
    g = lambda x: Just(x * 2)
    m = Just(3)
    assert Just(3).bind(f) == f(3)          # left identity
    assert m.bind(Just) == m                # right identity
    assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))
    assert Nothing().bind(f) == Nothing()
    print("laws okay")

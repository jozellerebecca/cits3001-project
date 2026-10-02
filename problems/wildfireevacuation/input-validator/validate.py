#!/usr/bin/env python3
import re
import sys

INTEGER = r"(0|[1-9]\d*)"          # a non-negative integer with no leading zeros
MAX_VALUE = 10**9


def read_ints(count):
    """Read one line that must contain exactly `count` integers separated by single spaces."""
    line = sys.stdin.readline()
    pattern = " ".join([INTEGER] * count) + "\n"
    assert re.fullmatch(pattern, line), f"bad line format: {line!r}"
    return list(map(int, line.split()))


# line 1: T S R
T, S, R = read_ints(3)
assert 1 <= T <= 200, f"T={T} out of range"
assert 1 <= S <= 200, f"S={S} out of range"
assert 1 <= R <= 2000, f"R={R} out of range"

# line 2: town populations
p = read_ints(T)
for x in p:
    assert 0 <= x <= MAX_VALUE, f"population {x} out of range"

# line 3: shelter capacities
c = read_ints(S)
for x in c:
    assert 0 <= x <= MAX_VALUE, f"shelter capacity {x} out of range"

# roads u v w
for _ in range(R):
    u, v, w = read_ints(3)
    assert 1 <= u <= T + S, f"road start {u} out of range"
    assert 1 <= v <= T + S, f"road end {v} out of range"
    assert 1 <= w <= MAX_VALUE, f"road capacity {w} out of range"

# nothing may come after the last road
assert sys.stdin.read() == "", "extra data after the last road"

# 42 tells problemtools the input is valid
sys.exit(42)
# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict
from pprint import pprint

aoc_data = get_data(day=13, year=2022)

# problem part is 1 or 2
# problem_part = 2

# test
test_data = \
"""[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


use_real_data = False

# un-comment below when ready to use real data
use_real_data = True

if use_real_data:
    print("Using AOC data")
    data = aoc_data
else:
    print("Using test data")
    data = test_data

lines = data.split('\n')

# --------------- part 1 ------------

index_of_pairs = 1

pairs_in_right_order = []


def in_order(left, right):
    def compare(l, r):
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return True
            elif l == r:
                return
            elif l > r:
                return False
        else:
            # coerce to lists, if necessary
            l = [l] if not isinstance(l, list) else l
            r = [r] if not isinstance(r, list) else r

            # iterate and compare
            for i in range(len(l)):
                if i > len(r) - 1:
                    return False

                res = compare(l[i], r[i])
                if res is not None:
                    return res

            if len(l) < len(r):
                return True

    return compare(left, right)


for i in range(0, len(lines), 3):
    left = eval(lines[i])
    right = eval(lines[i+1])
    if in_order(left, right):
        pairs_in_right_order.append(index_of_pairs)
        print('found a pair')

    index_of_pairs += 1

print(pairs_in_right_order)
ans = sum(pairs_in_right_order)

print(ans)

# --------------- part 2 ------------

packets = [[[2]], [[6]]]

for i in range(0, len(lines), 3):
    # print(index_of_packets, lines[i], lines[i+1])
    left = eval(lines[i])
    right = eval(lines[i+1])
    packets.append(left)
    packets.append(right)

from functools import cmp_to_key


def comp_func(left, right):
    return -1 if in_order(left, right) else 1


sorted_packets = sorted(packets, key=cmp_to_key(comp_func))

indices = []

two = [[2]]
six = [[6]]
for i in range(0, len(sorted_packets)):
    if sorted_packets[i] == two or sorted_packets[i] == six:
        indices.append(i + 1)

ans = indices[0] * indices[1]

print(ans)

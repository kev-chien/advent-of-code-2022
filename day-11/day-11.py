# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict
from pprint import pprint

aoc_data = get_data(day=11, year=2022)

# problem part is 1 or 2
problem_part = 2

# test
test_data = \
"""Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


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


@dataclass(init=False)
class Monkey:
    items: list[int]
    op_fn: T.Callable
    test_fn: T.Callable
    true_pass_to: int
    false_pass_to: int

    def set_op(self, lambda_right: str):
        self.op_fn = eval(f"lambda old: {lambda_right}")  # I know, but ... sometimes you gotta cut corners

    def set_test_fn(self, divisible_by_num: int):
        self.test_fn = lambda worry: worry % divisible_by_num == 0


monkeys = []

# for part 2 -> store the multiple of the divisible_by as our base
base = 1

for i in range(0, len(lines), 7):  # each "monkey config" takes 7 lines
    monkey = Monkey()
    monkey.items = [int(val) for val in lines[i + 1].split(': ')[1].split(', ')]
    monkey.set_op(lines[i + 2].split('= ')[1])

    divisible_by = int(lines[i + 3].split('by ')[1])
    base *= divisible_by

    monkey.set_test_fn(divisible_by)
    monkey.true_pass_to = int(lines[i + 4][-1])
    monkey.false_pass_to = int(lines[i + 5][-1])

    monkeys.append(monkey)


pprint(monkeys)

# run rounds, and count times each monkey inspected an item
monkey_inspected_count = [0 for _ in monkeys]

for round in range(10000):
    print(round)
    if (round % 1000 == 0):
        print(round, monkey_inspected_count)
        # pprint(monkeys)
    for i, monkey in enumerate(monkeys):
        # monkey inspects item with worry level
        for item in monkey.items:
            # increase inspected count
            monkey_inspected_count[i] += 1

            # worry level is modified by op_fn
            item = monkey.op_fn(item)

            if problem_part == 1:
                # monkey gets bored, worry level is floor divided by 3
                item //= 3
            else:
                # we can mod by the base (multiples of divisible bys that we actually care about)
                item = item % base

            # check test_fn
            if monkey.test_fn(item):
                monkeys[monkey.true_pass_to].items.append(item)
            else:
                monkeys[monkey.false_pass_to].items.append(item)

        # monkey has no more items
        monkey.items = []

counts_sorted = sorted(monkey_inspected_count)
ans = counts_sorted[-1] * counts_sorted[-2]

print(ans)


# -------------- part 2 -------------

# how do we manage these worry levels?!!!!

# okay, so the divisible by numbers are prime numbers
# so we don't actually need to store the worry levels
# we just need to store if it's divisible!!!! (or, the prime factors)
# ORRRR... let's always //= a number by the multiple of the prime factors that we actually care about.

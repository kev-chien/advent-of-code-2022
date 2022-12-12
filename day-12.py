# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict
from pprint import pprint

aoc_data = get_data(day=12, year=2022)

# problem part is 1 or 2
problem_part = 2

# test
test_data = \
"""Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


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
# credit goes to: https://www.redblobgames.com/pathfinding/a-star/implementation.html
import heapq


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


for y in range(len(lines)):
    for x in range(len(lines[0])):
        if 'S' == lines[y][x]:
            start = (x, y)
        elif 'E' == lines[y][x]:
            end = (x, y)


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def height(x, y):
    value = lines[y][x]
    if value == 'S':
        return ord('a')
    elif value == 'E':
        return ord('z')
    else:
        return ord(value)


def neighbors(a):
    (x, y) = a
    options = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]

    def is_in_grid(x_2, y_2):
        return 0 <= x_2 < len(lines[0]) and 0 <= y_2 < len(lines)

    def is_accessible(x_2, y_2):
        return height(x_2, y_2) <= height(x, y) + 1

    result = list(filter(
        lambda option: is_in_grid(option[0], option[1]) and is_accessible(option[0], option[1]),
        options
    ))
    return result


def a_star_search():
    queue = PriorityQueue()
    queue.put(start, 0)

    cost_so_far = {start: 0}

    while not queue.empty():
        current = queue.get()

        if current == end:
            break

        for neighbor in neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                queue.put(neighbor, priority)

    return cost_so_far


cost_so_far = a_star_search()

pprint(cost_so_far)

ans = cost_so_far[end]

print(ans)

# --------------- part 2 ------------
# reverse reverse
def heuristic_2(a, b):
    return 0  # no good heuristic anymore


def neighbors_2(a):
    (x, y) = a
    options = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]

    def is_in_grid(x_2, y_2):
        return 0 <= x_2 < len(lines[0]) and 0 <= y_2 < len(lines)

    def is_accessible(x_2, y_2):
        return height(x_2, y_2) + 1 >= height(x, y)

    result = list(filter(
        lambda option: is_in_grid(option[0], option[1]) and is_accessible(option[0], option[1]),
        options
    ))
    return result


def a_star_search_2():
    queue = PriorityQueue()
    queue.put(end, 0)

    cost_so_far = {end: 0}

    while not queue.empty():
        current = queue.get()
        x, y = current

        if lines[y][x] == 'a' or lines[y][x] == 'S':
            start = (x, y)
            break

        for neighbor in neighbors_2(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic_2(neighbor, end)
                queue.put(neighbor, priority)

    return cost_so_far, start


cost_so_far, start = a_star_search_2()

pprint(cost_so_far)

ans = cost_so_far[start]

print(ans)

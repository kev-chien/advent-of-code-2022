# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict

data = get_data(day=9, year=2022)


####### part 1

# test
test_data = \
"""R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

# un-comment below when ready to use real data
# data = test_data

lines = data.split('\n')


def find_diff(h, t):
    return (h[0] - t[0], h[1] - t[1])


visited = set()
t = (0, 0)
h = (0, 0)
for line in lines:
    d, moves = line.split(' ')
    moves = int(moves)
    # print(line)

    for i in range(moves):
        # print("h", h, "t", t)
        # do a thing
        if d == 'U':
            h = (h[0], h[1] + 1)
        if d == 'D':
            h = (h[0], h[1] - 1)
        if d == 'L':
            h = (h[0] - 1, h[1])
        if d == 'R':
            h = (h[0] + 1, h[1])

        diff = find_diff(h, t)

        """
          x x x
        x       x
        x   o   x
        x       x
          x x x
        """

        if diff == (2, 0):
            t = (t[0] + 1, t[1])
        elif diff == (2, 1):
            t = (t[0] + 1, t[1] + 1)
        elif diff == (1, 2):
            t = (t[0] + 1, t[1] + 1)
        elif diff == (0, 2):
            t = (t[0], t[1] + 1)
        elif diff == (-1, 2):
            t = (t[0] - 1, t[1] + 1)
        elif diff == (-2, 1):
            t = (t[0] - 1, t[1] + 1)
        elif diff == (-2, 0):
            t = (t[0] - 1, t[1])
        elif diff == (-2, -1):
            t = (t[0] - 1, t[1] - 1)
        elif diff == (-1, -2):
            t = (t[0] - 1, t[1] - 1)
        elif diff == (0, -2):
            t = (t[0], t[1] - 1)
        elif diff == (1, -2):
            t = (t[0] + 1, t[1] - 1)
        elif diff == (2, -1):
            t = (t[0] + 1, t[1] - 1)

        visited.add(t)

count = len(list(visited))

ans = count
print(ans)


# part 2

test_data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

# un-comment below when ready to use real data
# data = test_data

lines = data.split('\n')

visited = set()
rope = [(0, 0)] * 10
for line in lines:
    d, moves = line.split(' ')
    moves = int(moves)
    # print(line)

    for i in range(moves):
        # move head
        h = rope[0]
        if d == 'U':
            rope[0] = (h[0], h[1] + 1)
        if d == 'D':
            rope[0] = (h[0], h[1] - 1)
        if d == 'L':
            rope[0] = (h[0] - 1, h[1])
        if d == 'R':
            rope[0] = (h[0] + 1, h[1])
        # print(i, rope[0])

        """
        x x x x x
        x       x
        x   o   x
        x       x
        x x x x x
        """

        # move the rest
        for i in range(1, 10):
            h = rope[i - 1]
            t = rope[i]
            diff = find_diff(h, t)

            if diff == (2, 0):
                t = (t[0] + 1, t[1])
            elif diff == (2, 1):
                t = (t[0] + 1, t[1] + 1)
            elif diff == (1, 2):
                t = (t[0] + 1, t[1] + 1)
            elif diff == (0, 2):
                t = (t[0], t[1] + 1)
            elif diff == (-1, 2):
                t = (t[0] - 1, t[1] + 1)
            elif diff == (-2, 1):
                t = (t[0] - 1, t[1] + 1)
            elif diff == (-2, 0):
                t = (t[0] - 1, t[1])
            elif diff == (-2, -1):
                t = (t[0] - 1, t[1] - 1)
            elif diff == (-1, -2):
                t = (t[0] - 1, t[1] - 1)
            elif diff == (0, -2):
                t = (t[0], t[1] - 1)
            elif diff == (1, -2):
                t = (t[0] + 1, t[1] - 1)
            elif diff == (2, -1):
                t = (t[0] + 1, t[1] - 1)
            elif diff == (-2, -2):
                t = (t[0] - 1, t[1] - 1)
            elif diff == (-2, 2):
                t = (t[0] - 1, t[1] + 1)
            elif diff == (2, 2):
                t = (t[0] + 1, t[1] + 1)
            elif diff == (2, -2):
                t = (t[0] + 1, t[1] - 1)

            rope[i] = t

            if i == 9:
                visited.add(t)

    # print(rope)

count = len(list(visited))
# print(rope)

ans = count
print(ans)

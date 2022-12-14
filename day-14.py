# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict
from pprint import pprint


# pairwise, available in python 3.10
def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    return zip(iterable[:-1], iterable[1:])


aoc_data = get_data(day=14, year=2022)

# problem part is 1 or 2
problem_part = 2

# test
test_data = \
"""498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


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
max_x = 550 if problem_part == 1 else 550 + 350
grid = [['.' for _ in range(max_x)] for _ in range(175)]


left_most_x = 500
right_most_x = 500
bottom_most_y = 0

for line in lines:
    line = re.sub(r'(->\s)', '', line)
    # print(line)
    rock_points = line.split(' ')
    # print(rock_points)
    left_most_x = min(left_most_x, int(rock_points[0][0]))
    right_most_x = max(right_most_x, int(rock_points[0][0]))
    bottom_most_y = max(bottom_most_y, int(rock_points[0][1]))
    for point_1, point_2 in pairwise(rock_points):
        x1, y1 = list(map(int, point_1.split(',')))
        x2, y2 = list(map(int, point_2.split(',')))
        # print('line: ', (x1, y1), (x2, y2))
        left_most_x = min(left_most_x, x2)
        right_most_x = max(right_most_x, x2)
        bottom_most_y = max(bottom_most_y, y2)
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                print(f'drawing {y}, {x1}')
                grid[y][x1] = '#'
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                print(f'drawing {y1}, {x}')
                grid[y1][x] = '#'


if problem_part == 2:
    print('problem 2')
    for x in range(0, max_x):
        grid[bottom_most_y + 2][x] = '#'

    bottom_most_y += 2
    left_most_x = 0
    right_most_x = max_x


x_clipped_left, x_clipped_right = 400, 550
y_clipped_bottom = 100


def draw_image():
    image_pretty = '\n'.join([''.join(line[x_clipped_left:x_clipped_right]) for line in grid[:y_clipped_bottom]])
    print(image_pretty)


unit = 0
free_falling = False
while not free_falling:
    unit += 1
    sand_x, sand_y = (500, 0)
    if grid[sand_y][sand_x] == 'o':
        print("I'm blocked")
        break
    while True:
        options = [(sand_x, sand_y + 1), (sand_x - 1, sand_y + 1), (sand_x + 1, sand_y + 1)]
        moved = False
        for option_x, option_y in options:
            if grid[option_y][option_x] == '.':
                sand_x, sand_y = option_x, option_y
                moved = True
                break
        if not moved:
            grid[sand_y][sand_x] = 'o'
            break
        if sand_x < left_most_x or sand_x > right_most_x or sand_y > bottom_most_y:
            print("I'm falling to pieces")
            free_falling = True
            break

# print(unit)
# draw_image()
ans = unit - 1
print(ans)
# --------------- part 2 ------------
# code mixed with above

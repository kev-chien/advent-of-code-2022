# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict

aoc_data = get_data(day=10, year=2022)


# ----------- part 1 --------

# test
test_data = \
"""addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

# test_data = """noop
# addx 3
# addx -5"""

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

x = 1
cycle = 1
ans = 0

cycle_thing = set(list(range(20, 221, 40)))


def start_cycle():
    global ans
    # print(f'cycle={cycle}, line={line}, x={x}')
    # print(cycle)
    if cycle in cycle_thing:
        ans += cycle * x
        # print(f'added to ans - cycle={cycle}, line={line}, ans={ans}, x={x}')


for line in lines:
    # during cycle
    start_cycle()

    # after cycle
    cycle += 1
    if line == "noop":
        continue

    # addx: 2nd cycle
    start_cycle()

    cycle += 1

    _, arg = line.split(' ')
    arg = int(arg)
    x += arg
    # after 2nd cycle


print(ans)

# ------- part 2 --------

x = 1
cycle = 0

image = [['.'] * 40 for _ in range(6)]


def draw_image():
    image_pretty = '\n'.join([''.join(line) for line in image])
    print(image_pretty)


def start_cycle():
    print(f'cycle={cycle}, line={line}, x={x}')
    # print(cycle)
    crt_x_pos = cycle % 40
    crt_y_pos = cycle // 40
    if crt_x_pos in [x - 1, x, x + 1]:
        print('drawing', crt_x_pos, crt_y_pos, x)
        image[crt_y_pos][crt_x_pos] = '#'
        draw_image()


for line in lines:
    # during cycle
    start_cycle()

    # after cycle
    cycle += 1
    if line == "noop":
        continue

    # addx: 2nd cycle
    start_cycle()

    cycle += 1

    _, arg = line.split(' ')
    arg = int(arg)
    x += arg
    # after 2nd cycle




draw_image()

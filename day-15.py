# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict
from pprint import pprint
import math
import itertools


aoc_data = get_data(day=15, year=2022)

# problem part is 1 or 2
problem_part = 2

# test
test_data = \
"""Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


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

"""
thought process:
    - build list of sensors, and beacons
    - get min_x, and max_x from sensors
    - get max(m_d...) for sensor to beacon
    - for row y=row, from left to right,
     - check if beacon exists there
     - for sensor in sensors, check if m_d(sensor, beacon) is higher than m_d(sensor, point)
     - if beacon is close than current point, current point still possible
"""
# --------------- part 1 ------------
def m_d(a, b):
    return sum(abs(a_c - b_c) for a_c, b_c in zip(a, b))


sensors = []
beacons = []
beacons_set = set()
s_b_m_d = []
min_x = None
max_x = None
max_radius = 0
for line in lines:
    s_x, s_y, b_x, b_y = map(
        int,
        re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line).groups()
    )

    s = (s_x, s_y)
    b = (b_x, b_y)

    sensors.append(s)
    beacons.append(b)
    beacons_set.add(b)
    dist = m_d(s, b)
    s_b_m_d.append(dist)
    if min_x is None:
        min_x = s_x
    else:
        min_x = min(min_x, s_x)

    if max_x is None:
        max_x = s_x
    else:
        max_x = max(max_x, s_x)

    max_radius = max(max_radius, dist)

min_x -= max_radius
max_x += max_radius

print("sensors and beacons parsed")


def count_no_beacons(row):
    no_beacons = 0
    print(f"scanning min_x={min_x}, max_x={max_x}")
    for x in range(min_x, max_x + 1):
        if x % 100_000 == 0:
            print(x)
        no_beacon = (x, row) not in beacons_set and any(
            m_d((x, row), s) <= s_b_m_d[i]
            for i, s in enumerate(sensors)
        )
        if no_beacon:
            no_beacons += 1
    return no_beacons

# ans = count_no_beacons(10)
# ans = count_no_beacons(2000000)
# print(ans)
# --------------- part 2 ------------

# test data
# min_x = 0
# max_x = 20
# min_y = 0
# max_y = 20
# real data
min_x = 0
max_x = 4000000
min_y = 0
max_y = 4000000

# super inefficient method
# def find_beacon(row):
#     print(f"scanning min_x={min_x}, max_x={max_x}")
#     for x in range(min_x, max_x + 1):
#         if x % 100_000 == 0:
#             print(f'x={x}')
#         found_beacon = (x, row) not in beacons_set and all(
#             m_d((x, row), s) > s_b_m_d[i]
#             for i, s in enumerate(sensors)
#         )
#         if found_beacon:
#             return (x, row)

# for y in range(min_y, max_y + 1):
#     print(f"scanning min_y={min_y}, min_y={max_y}")
#     if y % 100_000 == 0:
#         print(f'y={y}')
#     beacon = find_beacon(y)
#     if beacon:
#         break

# print(beacon)
# x, y = beacon
# ans = x * 4000000 + y
# print(ans)

# I think I have to re-write my code

"""
idea:
for every sensor
check only the fringe (border) around it.
"""
candidates = set()

def check_has_beacon(c):
    x, y = c
    return (x, y) not in beacons_set and all(
        m_d((x, y), s) > s_b_m_d[i]
        for i, s in enumerate(sensors)
    )


def in_range(c):
    x, y = c
    return min_x <= x <= max_x and min_y <= y <= max_y


checked = set()
beacon = None
for i, s in enumerate(sensors):
    s_x, s_y = s
    radius = s_b_m_d[i] + 1
    # create a circle
    candidates = itertools.chain(
        zip(range(s_x - radius, s_x), range(s_y, s_y + radius)),
        zip(range(s_x, s_x + radius), range(s_y + radius, s_y, -1)),
        zip(range(s_x + radius, s_x, -1), range(s_y, s_y - radius, -1)),
        zip(range(s_x, s_x - radius, -1), range(s_y - radius, s_y, 1))
    )
    print(f'i={i}, sensor={s}, radius={radius}')
    for c in candidates:
        # print(f'candidate={c}')
        if c in checked:
            continue
        checked.add(c)
        if in_range(c) and check_has_beacon(c):
            beacon = c
            print("found beacon:", beacon)
            break
    if beacon:
        break

print(beacon)

x, y = beacon
ans = x * 4000000 + y
print(ans)

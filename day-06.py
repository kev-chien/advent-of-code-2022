from aocd import get_data
from aocd import submit
import re

data = get_data(day=6, year=2022)

# part 1 or part 2?
problem_part = 2


# test
test_data = \
"""mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

# un-comment below when ready to use real data
# data = test_data


def find_marker(data, num_chars):
    for i in range(len(data)):
        packet = set(data[i:i+num_chars])
        if len(list(packet)) == num_chars:
            return i + num_chars


ans = find_marker(data, 4)

print(ans)

ans = find_marker(data, 14)

print(ans)

from aocd import get_data
import re

data = get_data(day=5, year=2022)

# part 1 or part 2?
problem_part = 2


# test
test_data = \
"""    [D]    \n[N] [C]    \n[Z] [M] [P] \n 1   2   3 \n
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

# un-comment below when ready to use real data
# data = test_data

crates_data, moves_data = data.split('\n\n')

crates_lines = list(reversed(crates_data.split('\n')))

# part 1
"""
In [8]: crates_lines
Out[8]:
[' 1   2   3   4   5   6   7   8   9 ',
 '[M] [Z] [H] [P] [N] [W] [P] [L] [C]',
 '[J] [C] [J] [J] [C] [L] [Z] [V] [B]',
 '[C] [D] [F] [D] [D] [D] [T] [M] [G]',
 '[B]     [C] [M] [R] [Q] [F] [G] [P]',
 '[F]     [N] [T] [J] [P] [R]     [F]',
 '[R]     [G] [S]     [J] [H]     [Q]',
 '[L]     [W] [B]     [G]         [R]',
 '[H]                 [Z]         [J]']

In [9]: len(crates_lines[0])
Out[9]: 35

In [11]: list(range(1,len(crates_lines[0]),4))
Out[11]: [1, 5, 9, 13, 17, 21, 25, 29, 33]
"""

# build N lists to represent crates
crate_indices = list(range(1,len(crates_lines[0]),4))
crates = [[] for _ in range(len(crate_indices))]
for i in range(1, len(crates_lines)):
    for crate_number, crate_index in enumerate(crate_indices):
        if crates_lines[i][crate_index] != ' ':
            crates[crate_number].append(crates_lines[i][crate_index])

# print(crates)

# parse moves...
moves_lines = moves_data.split('\n')


"""
"move 1 from 2 to 1"
write regex that parses the above...
"""

pattern = re.compile('move (\d+) from (\d+) to (\d+)')

for move_line in moves_lines:
    match = re.search(pattern, move_line)
    crates_to_move, start_stack, end_stack = list(map(int, match.groups()))
    start_ind, end_ind = start_stack - 1, end_stack - 1
    # move the crates over
    if problem_part == 1:
        crates[end_ind].extend(reversed(crates[start_ind][-crates_to_move:]))
    elif problem_part == 2:
        crates[end_ind].extend(crates[start_ind][-crates_to_move:])

    crates[start_ind] = crates[start_ind][:-crates_to_move]
    # print(crates)

answer = ''.join(crate_stack[-1] for crate_stack in crates)
print(answer)

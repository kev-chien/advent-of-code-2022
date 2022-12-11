# import all the utils I might use
from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T
from collections import defaultdict

data = get_data(day=8, year=2022)


####### part 1

# test
test_data = \
"""30373
25512
65332
33549
35390"""

# un-comment below when ready to use real data
# data = test_data

lines = data.split('\n')
lines = [
    [int(t) for t in line]
    for line in lines
]

# width is X
# height is Y
Y = len(lines)
X = len(lines[0])

visible_on_edges = 2 * (Y + X) - 4

# visible, inside the edges
visible = set()

# scan in 4 directions
# scanning to the right, from top-left
for y in range(1, Y - 1):
    tallest = lines[y][0]
    for x in range(1, X - 1):
        tree = lines[y][x]
        if tree > tallest:
            visible.add((x, y))
        tallest = max(tree, tallest)

# scanning to the left, from top-right
for y in range(1, Y - 1):
    tallest = lines[y][X - 1]
    for x in range(X - 2, 0, -1):
        tree = lines[y][x]
        if tree > tallest:
            visible.add((x, y))
        tallest = max(tree, tallest)

# scanning to the bottom, from top-left
for x in range(1, X - 1):
    tallest = lines[0][x]
    for y in range(1, Y - 1):
        tree = lines[y][x]
        if tree > tallest:
            visible.add((x, y))
        tallest = max(tree, tallest)

# scanning to the top, from bottom-left
for x in range(1, X - 1):
    tallest = lines[Y - 1][x]
    for y in range(Y - 2, 0, -1):
        tree = lines[y][x]
        if tree > tallest:
            visible.add((x, y))
        tallest = max(tree, tallest)

visible_inside = len(list(visible))

print(visible_on_edges)
print(visible_inside)
ans = visible_inside + visible_on_edges
print(ans)


####### part 2
best_score = 1
# scan in 4 directions
# outer loop: iterate through all the trees
for y_t in range(1, Y - 1):
    for x_t in range(1, X - 1):
        # scanning to the right
        tree_score = 1
        score = 0
        for x in range(x_t + 1, X):
            score += 1
            tree = lines[y_t][x]
            if tree >= lines[y_t][x_t]:
                break
        tree_score *= score
        if not tree_score:
            break

        # scanning to the left
        score = 0
        for x in range(x_t - 1, -1, -1):
            score += 1
            tree = lines[y_t][x]
            if tree >= lines[y_t][x_t]:
                break
        tree_score *= score
        if not tree_score:
            break

        # scanning to the bottom
        score = 0
        for y in range(y_t + 1, Y):
            score += 1
            tree = lines[y][x_t]
            if tree >= lines[y_t][x_t]:
                break
        tree_score *= score
        if not tree_score:
            break

        # scanning to the top
        score = 0
        for y in range(y_t - 1, -1, -1):
            score += 1
            tree = lines[y][x_t]
            if tree >= lines[y_t][x_t]:
                break
        tree_score *= score
        if not tree_score:
            break

        best_score = max(best_score, tree_score)

print(best_score)
ans = best_score

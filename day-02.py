"""
1 col - Opponent:
A - Rock 1
B - Paper 2
C - Scissors 3

2 col - Me:
X - Rock 1
Y - Paper 2
Z - Scissors 3
"""

from aocd import data

lines = data.split('\n')


def determine_scores(op, me):
    op_score, me_score = 0, 0

    # map A, B, C to 1, 2, 3
    op_int = ord(op) - ord('A') + 1

    # map X, Y, Z to 1, 2, 3
    me_int = ord(me) - ord('X') + 1

    if op_int == me_int:
        # draw
        op_score = op_int + 3
        me_score = me_int + 3
    elif (op_int, me_int) == (2, 1) or \
         (op_int, me_int) == (3, 2) or \
         (op_int, me_int) == (1, 3):
        # opponent wins if they are (2, 1), or (3, 2), or (1, 3)
        op_score = op_int + 6
        me_score = me_int
    else:
        # i win
        op_score = op_int
        me_score = me_int + 6

    return op_score, me_score


op_scores, me_scores = [], []

for line in lines:
    op, me = line[0], line[2]
    op_score, me_score = determine_scores(op, me)
    op_scores.append(op_score)
    me_scores.append(me_score)

print(f'op_scores sum: {sum(op_scores)}')
print(f'me_scores sum: {sum(me_scores)}')


# part 2
print('part 2')


def determine_my_move(op, outcome):
    if outcome == 'X':  # lose
        lose_map = {
            'A': 'Z',  # rock - scissors
            'B': 'X',  # paper - rock
            'C': 'Y',  # scissors - paper
        }
        me = lose_map[op]
    elif outcome == 'Y':  # draw
        draw_map = {
            'A': 'X',
            'B': 'Y',
            'C': 'Z',
        }
        me = draw_map[op]
    else:  # win
        win_map = {
            'A': 'Y',  # rock - paper
            'B': 'Z',  # paper - scissors
            'C': 'X',  # scissors - rock
        }
        me = win_map[op]

    return me


me_scores, op_scores = [], []
for line in lines:
    op, outcome = line[0], line[2]
    me = determine_my_move(op, outcome)
    op_score, me_score = determine_scores(op, me)
    op_scores.append(op_score)
    me_scores.append(me_score)

print(f'op_scores sum: {sum(op_scores)}')
print(f'me_scores sum: {sum(me_scores)}')

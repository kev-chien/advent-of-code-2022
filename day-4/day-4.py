from aocd import data

# test
test_data = \
"""2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

# un-comment below when ready to use real data
# data = test_data

lines = data.split('\n')

# part 1


def left_contains_right(left_1, left_2, right_1, right_2):
    return left_1 <= right_1 <= right_2 <= left_2


count = 0
for line in lines:
    sections = line.split(',')
    a_1, a_2 = list(map(int, sections[0].split('-')))
    b_1, b_2 = list(map(int, sections[1].split('-')))
    fully_contained = left_contains_right(a_1, a_2, b_1, b_2) or left_contains_right(b_1, b_2, a_1, a_2)

    if fully_contained:
        count += 1

print(count)


# part 2

def overlaps(a_1, a_2, b_1, b_2):
    """
    case_1:
    aaaaa
       bbbbbbb

    case_2:
    bbbbb
       aaaaaa

    case_3:
      bb
    aaaaaa

    case_4:
      aa
    bbbbbb
    """
    case_1 = a_1 < b_1 <= a_2 < b_2
    case_2 = b_1 < a_1 <= b_2 < a_2
    case_3 = a_1 <= b_1 <= b_2 <= a_2
    case_4 = b_1 <= a_1 <= a_2 <= b_2

    return case_1 or case_2 or case_3 or case_4


count = 0
for line in lines:
    sections = line.split(',')
    a_1, a_2 = list(map(int, sections[0].split('-')))
    b_1, b_2 = list(map(int, sections[1].split('-')))
    fully_contained = overlaps(a_1, a_2, b_1, b_2)

    if fully_contained:
        count += 1

print(count)

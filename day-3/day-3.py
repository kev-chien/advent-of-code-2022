from aocd import get_data

data = get_data(day=3, year=2022)

test_data = \
"""vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

# comment this out when ready
# data = test_data

"""
Notes:
    each rucksack has 2 compartments of equal lengths
    probably, put comp 1 in a set, check if 2 has anything in 1
    or, put everything in a set, do an intersection
"""

# part 1


def priority(char):
    """
    In python, 'a' > 'A'
    >>> 'a' > 'A'
    True
    >>> ord('A')
    65
    >>> ord('a')
    97
    """
    if char >= 'A' and char < 'a':
        return ord(char) - ord('A') + 27
    elif char >= 'a':
        return ord(char) - ord('a') + 1
    else:
        raise Exception('impossibru')


assert priority('p') == 16
assert priority('L') == 38


def get_priority_of_item_in_both_compartments(rucksack: str):
    """time to do a lot of string stuff"""
    # split into compartments
    half_index = int(len(rucksack)/2)
    comp_1, comp_2 = rucksack[:half_index], rucksack[half_index:]
    print(comp_1, comp_2)

    # find duplicate item
    duplicate = set(comp_1) & set(comp_2)
    assert len(duplicate) == 1
    duplicate_item = list(duplicate)[0]

    # find priority
    return priority(duplicate_item)


assert get_priority_of_item_in_both_compartments('vJrwpWtwJgWrhcsFMMfFFhFp') == 16


lines = data.split('\n')
sum_priorities = 0
for line in lines:
    sum_priorities += get_priority_of_item_in_both_compartments(line)

print(sum_priorities)


# part 2


def get_priority_of_item_in_three_elf_group(rucksacks: list[str]):
    """finds the priority of the shared item, in the rucksacks of a three-elf group"""
    assert len(rucksacks) == 3

    # find shared item
    shared = set(rucksacks[0]) & set(rucksacks[1]) & set(rucksacks[2])
    assert len(shared) == 1
    shared_item = list(shared)[0]

    # find priority
    return priority(shared_item)


sum_priorities = 0
for index in range(0, len(lines), 3):
    three_elf_group = lines[index:index+3]
    sum_priorities += get_priority_of_item_in_three_elf_group(three_elf_group)

print(sum_priorities)

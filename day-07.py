from __future__ import annotations
from aocd import get_data
from aocd import submit
import re
from dataclasses import dataclass, field
import typing as T

data = get_data(day=7, year=2022)

# part 1 or part 2?
problem_part = 2


# test
test_data = \
"""$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

# un-comment below when ready to use real data
# data = test_data

# part 1


@dataclass
class TreeNode:
    name: str
    parent: T.Optional[TreeNode] = None
    size: int = 0


@dataclass
class Dir(TreeNode):
    children: dict[str, TreeNode] = field(default_factory=dict)

    def __repr__(self):
        return f'{self.name} (dir), children={[repr(child) for child in self.children.values()]}'


@dataclass
class File(TreeNode):
    def __repr__(self):
        return f'{self.name} (file, size={self.size})'


lines = data.split('\n')

cd_pattern = re.compile(r'\$ cd (\S+)')
file_pattern = re.compile(r'(\d+) (\S+)')
dir_pattern = re.compile(r'dir (\S+)')
ls_pattern = re.compile(r'\$ ls')


# create root
root = Dir(name='/')
cur_node = root

for line in lines:
    cd_match = re.search(cd_pattern, line)
    file_match = re.search(file_pattern, line)
    dir_match = re.search(dir_pattern, line)
    ls_match = re.search(ls_pattern, line)

    if cd_match:
        cd_into = cd_match.group(1)
        if cd_into == '/':
            # root node, no-op
            cur_node = root
        elif cd_into == '..':
            # go up
            cur_node = cur_node.parent
        else:
            # assumption: we never cd, before we ls
            cur_node = cur_node.children[cd_into]
    elif file_match:
        # assumption: we only see a file name after an `ls`
        file_size = int(file_match.group(1))
        file_name = file_match.group(2)
        cur_node.children[file_name] = File(name=file_name, parent=cur_node, size=file_size)
    elif dir_match:
        # assumption: we only see a dir name after an `ls`
        dir_name = dir_match.group(1)
        cur_node.children[dir_name] = Dir(name=dir_name, parent=cur_node)
    elif ls_match:
        # no-op
        pass
    else:
        raise Exception("should not happen")


def count_size(cur_node: TreeNode):
    """Updates all the Dir's with a size"""
    if isinstance(cur_node, Dir):
        cur_node.size = sum(node.size or count_size(node) for node in cur_node.children.values()) or 0
        return cur_node.size
    elif isinstance(cur_node, File):
        # this should also not really happen
        return cur_node.size
    else:
        raise Exception("should not happen")


count_size(root)


def find_dirs_at_most(cur_node: TreeNode, at_most: int, result: list[Dir] = []) -> list[Dir]:
    if isinstance(cur_node, Dir):
        if cur_node.size <= at_most:
            result.append(cur_node)
        for child in cur_node.children.values():
            find_dirs_at_most(child, at_most, result)
        return result
    elif isinstance(cur_node, File):
        # this should also not really happen
        return result
    else:
        raise Exception("should not happen")


result = find_dirs_at_most(root, 100000)

ans = sum(thing.size for thing in result)

print(ans)


# part 2
unused_space = 70_000_000 - root.size


def find_dir_at_least(cur_node: TreeNode, at_least: int) -> Dir:
    """Pass in the root node as the best_candidate
    Every dir, attempt to update best_candidate if the dir is better"""
    best_candidate = cur_node
    def inner(cur_node, at_least: int):
        nonlocal best_candidate
        if isinstance(cur_node, Dir):
            if best_candidate.size > cur_node.size >= at_least:
                best_candidate = cur_node
            for child in cur_node.children.values():
                inner(child, at_least)
        elif isinstance(cur_node, File):
            # no-op
            pass
        else:
            raise Exception("should not happen")

    inner(cur_node, at_least)
    return best_candidate


space_to_delete = 30_000_000 - unused_space
best_candidate = find_dir_at_least(root, space_to_delete)

print(best_candidate.name, best_candidate.size)

ans = best_candidate.size

print(ans)

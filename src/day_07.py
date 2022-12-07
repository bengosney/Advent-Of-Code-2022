# Standard Library
from collections import defaultdict
from functools import lru_cache
from os import path

# First Party
from utils import read_input


class dir:
    def __init__(self, tree) -> None:
        self.files = {}
        self.children = []
        self.dir_tree = tree

    @lru_cache
    def sum(self) -> int:
        return sum([v for v in self.files.values()])

    @lru_cache
    def total_size(self) -> int:
        total = self.sum()

        for c in self.children:
            total += self.dir_tree[c].total_size()

        return total

    @staticmethod
    def parse(input: str) -> dict[str, "dir"]:
        dir_tree = defaultdict(lambda: dir(dir_tree))
        cwd = ""

        @lru_cache
        def abspath(*args):
            return path.abspath(path.join(*args))

        for line in input.split("\n"):
            match line.split(" "):
                case ("$", *args):
                    match args:
                        case ("cd", d):
                            cwd = abspath(cwd, d)
                case ("dir", d):
                    dir_tree[cwd].children.append(abspath(cwd, d))
                case (size, name):
                    dir_tree[cwd].files[name] = int(size)
                case _:
                    raise Exception(f"Unknow line: {line}")

        return dir_tree


def part_1(input: str) -> int:
    MAX_SIZE = 100000

    dir_tree = dir.parse(input)

    totals = 0
    for folder in dir_tree.values():
        if (total := folder.total_size()) <= MAX_SIZE:
            totals += total

    return totals


def part_2(input: str) -> int:
    MAX_SIZE = 70000000
    MIN_FREE = 30000000

    dir_tree = dir.parse(input)

    needed_space = MIN_FREE - (MAX_SIZE - dir_tree["/"].total_size())

    totals = []
    for folder in dir_tree.values():
        if (total := folder.total_size()) >= needed_space:
            totals.append(total)

    return min(totals)


# -- Tests


def get_example_input() -> str:
    return """$ cd /
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


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 95437


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 24933642


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1334506


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 7421137


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

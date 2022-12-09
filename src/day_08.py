# Standard Library
from collections.abc import Callable, Iterable
from math import prod

# First Party
from utils import read_input


def map_trees(input: str) -> tuple[dict[tuple[int, int], int], int, int]:
    tree_map = {}

    for y, line in enumerate(input.split("\n")):
        for x, tree in enumerate(line):
            tree_map[(x, y)] = int(tree)

    max_x = max(map(lambda p: p[0], tree_map)) + 1
    max_y = max(map(lambda p: p[1], tree_map)) + 1

    return tree_map, max_x, max_y


def part_1(input: str) -> int:
    tree_map, max_x, max_y = map_trees(input)

    visible = max_x + max_y - 1
    for x, y in tree_map:
        if x in [0, max_x] or y in [0, max_y]:
            continue

        visible += int(
            any(
                [
                    all(tree_map[(x, y)] > tree_map[(tx, y)] for tx in range(x)),
                    all(tree_map[(x, y)] > tree_map[(tx, y)] for tx in range(x + 1, max_x)),
                    all(tree_map[(x, y)] > tree_map[(x, ty)] for ty in range(y)),
                    all(tree_map[(x, y)] > tree_map[(x, ty)] for ty in range(y + 1, max_y)),
                ]
            )
        )

    return visible


def one_until(predicate: Callable, iterable: Iterable):
    for x in iterable:
        yield 1
        if predicate(x):
            break


def part_2(input: str) -> int:
    tree_map, max_x, max_y = map_trees(input)

    scores = [
        prod(
            [
                sum(one_until(lambda tx: tree_map[(x, y)] <= tree_map[(tx, y)], reversed(range(x)))),
                sum(one_until(lambda tx: tree_map[(x, y)] <= tree_map[(tx, y)], range(x + 1, max_x))),
                sum(one_until(lambda ty: tree_map[(x, y)] <= tree_map[(x, ty)], reversed(range(y)))),
                sum(one_until(lambda ty: tree_map[(x, y)] <= tree_map[(x, ty)], range(y + 1, max_y))),
            ],
        )
        for x, y in tree_map
    ]
    return max(scores)


# -- Tests


def get_example_input() -> str:
    return """30373
25512
65332
33549
35390"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 21


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 8


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1779


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 172224


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

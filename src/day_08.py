# First Party
from utils import read_input


def part_1(input: str) -> int:
    tree_map = {}
    positions = []

    max_x = 0
    max_y = 0

    for y, line in enumerate(input.split("\n")):
        max_y = max(max_y, y)
        for x, tree in enumerate(line):
            max_x = max(max_x, x)
            tree_map[(x, y)] = int(tree)
            positions.append((x, y))

    visible = []
    for x, y in positions:
        if x in [0, max_x] or y in [0, max_y]:
            visible.append((x, y))
            continue

        tree = tree_map[(x, y)]

        if any(
            [
                all(tree > tree_map[(tx, y)] for tx in range(x)),
                all(tree > tree_map[(tx, y)] for tx in range(x + 1, max_x + 1)),
                all(tree > tree_map[(x, ty)] for ty in range(y)),
                all(tree > tree_map[(x, ty)] for ty in range(y + 1, max_y + 1)),
            ]
        ):
            visible.append((x, y))

    return len(visible)


def part_2(input: str) -> int:
    tree_map = {}
    positions = []

    max_x = 0
    max_y = 0

    for y, line in enumerate(input.split("\n")):
        max_y = max(max_y, y)
        for x, tree in enumerate(line):
            max_x = max(max_x, x)
            tree_map[(x, y)] = int(tree)
            positions.append((x, y))

    scores = []
    for x, y in positions:
        tree = tree_map[(x, y)]

        x1 = 0
        for tx in reversed(range(x)):
            x1 += 1
            if tree <= tree_map[(tx, y)]:
                break

        x2 = 0
        for tx in range(x + 1, max_x + 1):
            x2 += 1
            if tree <= tree_map[(tx, y)]:
                break

        y1 = 0
        for ty in reversed(range(y)):
            y1 += 1
            if tree <= tree_map[(x, ty)]:
                break

        y2 = 0
        for ty in range(y + 1, max_y + 1):
            y2 += 1
            if tree <= tree_map[(x, ty)]:
                break

        scores.append(x1 * x2 * y1 * y2)

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

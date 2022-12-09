# Standard Library
from collections import defaultdict
from itertools import repeat

# First Party
from utils import read_input

X = 0
Y = 1


def draw(head: tuple[int, int], tail: tuple[int, int]):
    height = 5
    width = 6
    for y in range(height):
        for x in range(width):
            pos = (x, (height - y) - 1)
            p = "."
            if pos == tail:
                p = "T"
            if pos == head:
                p = "H"
            print(p, end="")
        print()


def part_1(input: str) -> int:
    head = [0, 0]
    tail = [0, 0]

    visited = defaultdict(lambda: 0)

    commands = []
    for line in input.split("\n"):
        direction, amount = line.split()
        commands.extend(repeat(direction, int(amount)))

    for cmd in commands:
        match cmd:
            case "R":
                head[X] += 1
            case "L":
                head[X] -= 1
            case "U":
                head[Y] += 1
            case "D":
                head[Y] -= 1

        x_diff = head[X] - tail[X]
        y_diff = head[Y] - tail[Y]

        if (abs(x_diff) + abs(y_diff)) == 3:
            tail[X] += 1 if x_diff > 0 else -1
            tail[Y] += 1 if y_diff > 0 else -1

        while abs(head[X] - tail[X]) >= 2:
            tail[X] += 1 if (head[X] - tail[X]) > 0 else -1

        while abs(head[Y] - tail[Y]) >= 2:
            tail[Y] += 1 if (head[Y] - tail[Y]) > 0 else -1

        visited[tuple(tail)] = 1

    return sum(visited.values())


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 13


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


# def test_part_1_real():
#     real_input = read_input(__file__)
#     assert part_1(real_input) is not None


# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

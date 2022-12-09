# Standard Library
from collections import defaultdict
from itertools import repeat

# First Party
from utils import read_input

X = 0
Y = 1


def get_move(x: int) -> int:
    return (x > 0) - (x < 0)


def follow(leader, follower):
    if abs(leader[X] - follower[X]) > 1 or abs(leader[Y] - follower[Y]) > 1:
        follower[X] += get_move(leader[X] - follower[X])
        follower[Y] += get_move(leader[Y] - follower[Y])

    return follower


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

        tail = follow(head, tail)

        visited[tuple(tail)] = 1

    return sum(visited.values())


def part_2(input: str) -> int:
    rope = list(repeat([0, 0], 10))
    visited = defaultdict(lambda: 0)

    commands = []
    for line in input.split("\n"):
        direction, amount = line.split()
        commands.extend(repeat(direction, int(amount)))

    for cmd in commands:
        match cmd:
            case "R":
                rope[0][X] += 1
            case "L":
                rope[0][X] -= 1
            case "U":
                rope[0][Y] += 1
            case "D":
                rope[0][Y] -= 1

        for i in range(1, len(rope)):
            rope[i] = follow(rope[i - 1].copy(), rope[i].copy())

        visited[tuple(rope[-1])] = 1

    return sum(visited.values())


# -- Tests


def get_example_input_1() -> str:
    return """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def test_part_1():
    test_input = get_example_input_1()
    assert part_1(test_input) == 13


def get_example_input_2() -> str:
    return """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def test_part_2():
    test_input = get_example_input_2()
    assert part_2(test_input) == 36


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 6087


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 2493


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

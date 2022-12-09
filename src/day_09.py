# Standard Library
from collections import defaultdict
from itertools import repeat
from typing import cast

# First Party
from utils import read_input

MOVES = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}

Point = tuple[int, int]


def move(x: int) -> int:
    return (x > 0) - (x < 0)


def add(a: Point, b: Point) -> Point:
    return cast(Point, tuple([x + y for x, y in list(zip(a, b))]))


def follow(leader: Point, follower: Point) -> Point:
    diff_x, diff_y = (x - y for x, y in zip(leader, follower))
    if abs(diff_x) > 1 or abs(diff_y) > 1:
        return add(follower, (move(diff_x), move(diff_y)))

    return follower


def simulate(input: str, length) -> int:
    rope: list[Point] = list(repeat((0, 0), length))
    visited = defaultdict(lambda: 0)

    for line in input.split("\n"):
        direction, amount = line.split(" ")
        for _ in range(int(amount)):
            rope[0] = add(rope[0], MOVES[direction])
            for i in range(1, len(rope)):
                rope[i] = follow(rope[i - 1], rope[i])

            visited[rope[-1]] = 1

    return sum(visited.values())


def part_1(input: str) -> int:
    return simulate(input, 2)


def part_2(input: str) -> int:
    return simulate(input, 10)


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

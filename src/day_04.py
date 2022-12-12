# First Party
from utils import no_input_skip, read_input


def expand(group: str) -> list[int]:
    start, end = map(int, group.split("-"))
    return list(range(start, end + 1))


def contains(one: list[int], two: list[int]) -> int:
    return int(all(i in two for i in one) or all(i in one for i in two))


def overlaps(one: list[int], two: list[int]) -> int:
    return int(any(i in two for i in one))


def part_1(input: str) -> int:
    return sum(map(lambda line: contains(*map(expand, line.split(","))), input.split("\n")))


def part_2(input: str) -> int:
    return sum(map(lambda line: overlaps(*map(expand, line.split(","))), input.split("\n")))


# -- Tests


def get_example_input() -> str:
    return """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 2


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 4


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 464


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 770


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

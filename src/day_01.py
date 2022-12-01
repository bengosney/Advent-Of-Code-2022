# First Party
from utils import read_input


def part_1(input: str) -> int:
    elves = input.split("\n\n")

    max_cals = 0
    for elve in elves:
        cals = sum(map(int, elve.split("\n")))
        max_cals = max(max_cals, cals)

    return max_cals


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 24000


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

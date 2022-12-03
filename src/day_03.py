# First Party
from utils import read_input

priorities = {
    **{chr(i + 96): i for i in range(1, 27)},
    **{chr(i + 38): i for i in range(26, 53)},
}


def part_1(input: str) -> int:
    priority = 0
    for line in input.split("\n"):
        in_both = set(line[: len(line) // 2]).intersection(line[len(line) // 2 :])
        for item in in_both:
            priority += priorities[item]

    return priority


def part_2(input: str) -> int:
    priority = 0
    lines = input.split("\n")
    for i in range(0, len(lines), 3):
        in_group = set(lines[i]).intersection(lines[i + 1]).intersection(lines[i + 2])
        for c in in_group:
            priority += priorities[c]

    return priority


# -- Tests


def get_example_input() -> str:
    return """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 157


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 70


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 7597


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 2607


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

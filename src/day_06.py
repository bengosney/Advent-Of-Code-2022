# First Party
from utils import no_input_skip, read_input


def find_uniq_position(input: str, length: int) -> int:
    for i in range(len(input) - length):
        if len(set(input[i : i + length])) == length:
            return i + length

    raise Exception("No solution found")


def part_1(input: str) -> int:
    return find_uniq_position(input, 4)


def part_2(input: str) -> int:
    return find_uniq_position(input, 14)


# -- Tests


def get_example_input() -> str:
    return """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 7


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 19


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1953


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 2301


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

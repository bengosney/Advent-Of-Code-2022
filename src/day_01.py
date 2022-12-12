# First Party
from utils import no_input_skip, read_input


def get_calorie_list(input: str) -> list[int]:
    return sorted(map(lambda e: sum(map(int, e.split("\n"))), input.split("\n\n")), reverse=True)


def part_1(input: str) -> int:
    return get_calorie_list(input)[0]


def part_2(input: str) -> int:
    return sum(get_calorie_list(input)[:3])


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


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 45000


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 70720


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 207148


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

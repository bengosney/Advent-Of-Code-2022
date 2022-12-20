# Standard Library
from collections import deque

# First Party
from utils import no_input_skip, read_input


def mix(input_numbers: list[int]) -> list[int]:
    numbers = deque(input_numbers)

    for n in input_numbers:
        rot = numbers.index(n)
        numbers.rotate(-rot)
        numbers.popleft()
        numbers.rotate(-n)
        numbers.insert(0, n)
        numbers.rotate(rot + n)

    numbers.rotate(-1)
    return list(numbers)


def grove_numbers(numbers: list[int]) -> list[int]:
    idx = numbers.index(0)
    return [
        numbers[(1000 + idx) % len(numbers)],
        numbers[(2000 + idx) % len(numbers)],
        numbers[(3000 + idx) % len(numbers)],
    ]


def part_1(input: str) -> int:
    input_numbers = list(map(int, input.split("\n")))
    numbers = mix(input_numbers)
    ans = grove_numbers(numbers)

    return sum(ans)


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """1
2
-3
3
-2
0
4"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) is not None


def test_mix():
    test_input = get_example_input()
    mixed = mix(list(map(int, test_input.split("\n"))))
    answer = [1, 2, -3, 4, 0, 3, -2]
    print(mixed)
    print(answer)

    assert mixed == answer


def test_grove():
    test_input = get_example_input()
    mixed = mix(list(map(int, test_input.split("\n"))))
    grove = grove_numbers(mixed)
    answer = [4, -3, 2]
    print(grove)
    print(answer)

    assert grove == answer


@no_input_skip
def test_real_grove():
    test_input = read_input(__file__)
    mixed = mix(list(map(int, test_input.split("\n"))))
    grove = grove_numbers(mixed)
    answer = [1608, -2852, 8469]
    print(grove)
    print(answer)

    assert grove == answer


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 7225


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) == 548634267428


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

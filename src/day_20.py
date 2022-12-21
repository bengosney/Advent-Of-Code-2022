# Standard Library
from collections import deque
from collections.abc import Iterable

# First Party
from utils import no_input_skip, read_input


def mix(numbers: deque[tuple[int, int]]) -> list[int]:
    for n in list(numbers):
        v, _ = n
        numbers.rotate(-numbers.index(n, 0))
        numbers.popleft()
        numbers.rotate(-v)
        numbers.appendleft(n)

    return [n[0] for n in numbers]


def grove_numbers(numbers: list[int]) -> list[int]:
    idx = numbers.index(0)
    return [
        numbers[(1000 + idx) % len(numbers)],
        numbers[(2000 + idx) % len(numbers)],
        numbers[(3000 + idx) % len(numbers)],
    ]


def intput_to_pairs(input: str) -> Iterable[tuple[int, int]]:
    for i, n in enumerate(map(int, input.split("\n"))):
        yield (n, n * i)


def part_1(input: str) -> int:
    numbers = deque(intput_to_pairs(input))

    numbers = mix(numbers)
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
    assert part_1(test_input) == 3


def test_grove():
    test_input = get_example_input()
    numbers = deque(intput_to_pairs(test_input))
    mixed = mix(numbers)
    grove = grove_numbers(mixed)
    answer = [4, -3, 2]

    assert grove == answer


@no_input_skip
def test_real_grove():
    test_input = read_input(__file__)
    numbers = deque(intput_to_pairs(test_input))
    mixed = mix(numbers)
    grove = grove_numbers(mixed)
    answer = [1608, -2852, 8469]

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

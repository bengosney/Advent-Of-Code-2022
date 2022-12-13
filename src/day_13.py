# First Party
from utils import no_input_skip, read_input


def compare(packet_1, packet_2) -> bool | None:
    for i in range(min(len(packet_1), len(packet_2))):
        if isinstance(packet_1[i], list) and not isinstance(packet_2[i], list):
            packet_2[i] = [packet_2[i]]

        if isinstance(packet_2[i], list) and not isinstance(packet_1[i], list):
            packet_1[i] = [packet_1[i]]

        if isinstance(packet_1[i], list) and isinstance(packet_2[i], list):
            if (res := compare(packet_1[i], packet_2[i])) is not None:
                return res

        if packet_1[i] < packet_2[i]:
            return True

        if packet_1[i] > packet_2[i]:
            return False

    if len(packet_1) == len(packet_2):
        return None

    return len(packet_1) < len(packet_2)


def part_1(input: str) -> int:
    correct = []
    for i, packet_pair in enumerate(input.split("\n\n")):
        packet_1, packet_2 = list(map(eval, packet_pair.split("\n")))
        res = compare(packet_1, packet_2)
        if res or res is None:
            correct.append(i + 1)

    return sum(correct)


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 13


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 5208


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

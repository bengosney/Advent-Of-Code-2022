# Standard Library
from functools import cmp_to_key
from typing import Literal

# First Party
from utils import no_input_skip, read_input


def parse(packet_row: str):
    def p(packet: list):
        _packet = []

        while len(packet):
            c = packet.pop(0)
            match c:
                case "[":
                    _packet.append(p(packet))
                case "]":
                    return _packet
                case ",":
                    num = ""
                case n:
                    num = n
                    while len(packet) and packet[0].isnumeric():
                        num += packet.pop(0)
                    _packet.append(int(num))

        return _packet

    return p(list(packet_row)[1:-1])


def compare(packet_1, packet_2) -> Literal[-1] | Literal[0] | Literal[1]:
    _packet_1 = list(packet_1)
    _packet_2 = list(packet_2)
    for i in range(min(len(_packet_1), len(_packet_2))):
        if isinstance(_packet_1[i], list) and not isinstance(_packet_2[i], list):
            _packet_2[i] = [_packet_2[i]]

        if isinstance(_packet_2[i], list) and not isinstance(_packet_1[i], list):
            _packet_1[i] = [_packet_1[i]]

        if isinstance(_packet_1[i], list) or isinstance(_packet_2[i], list):
            if (res := compare(_packet_1[i], _packet_2[i])) != 0:
                return res
            continue

        if _packet_1[i] < _packet_2[i]:
            return 1

        if _packet_1[i] > _packet_2[i]:
            return -1

    if len(_packet_1) == len(_packet_2):
        return 0

    return 1 if len(_packet_1) < len(_packet_2) else -1


def part_1(input: str) -> int:
    correct = []
    for i, packet_pair in enumerate(input.split("\n\n")):
        packet_1, packet_2 = list(map(parse, packet_pair.split("\n")))
        if compare(packet_1, packet_2) >= 0:
            correct.append(i + 1)

    return sum(correct)


def part_2(input: str) -> int:
    packets = list(map(parse, filter(lambda x: x != "", input.split("\n"))))
    packets.extend(([[2]], [[6]]))

    packets.sort(key=cmp_to_key(compare), reverse=True)

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


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


def test_parser():
    test_input = get_example_input()
    for row in filter(lambda x: x != "", test_input.split("\n")):
        assert parse(row) == eval(row)


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 13


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 140


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 5208


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 25792


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

# Standard Library
import re
from collections import defaultdict

# First Party
from utils import read_input


def parse_input(input: str) -> tuple[dict[int, list[str]], list[dict[str, int]]]:
    inital, moves = input.split("\n\n")
    inital = inital.split("\n")
    inital.pop()
    inital.reverse()

    stacks = defaultdict(lambda: [])

    for row in inital:
        for i in range(1, len(row), 4):
            if row[i] != " ":
                stacks[i // 4].append(row[i])

    moves = moves.split("\n")
    regex = r"^move\s(?P<count>\d+)\sfrom\s(?P<from>\d+)\sto\s(?P<to>\d+)$"
    parsed_moves = []
    for move in moves:
        parsed = re.search(regex, move, re.MULTILINE)
        if parsed is not None:
            parsed_moves.append({k: int(v) for k, v in parsed.groupdict().items()})

    return dict(stacks), parsed_moves


def get_ans(stacks):
    ans = ""
    for i in range(len(stacks)):
        ans += f"{stacks[i][-1]}"

    return ans


def part_1(input: str) -> str:
    stacks, moves = parse_input(input)

    for move in moves:
        for _ in range(move["count"]):
            stacks[move["to"] - 1].append(stacks[move["from"] - 1].pop())

    return get_ans(stacks)


def part_2(input: str) -> str:
    stacks, moves = parse_input(input)

    for move in moves:
        hold = []
        for _ in range(move["count"]):
            hold.append(stacks[move["from"] - 1].pop())

        hold.reverse()
        for c in hold:
            stacks[move["to"] - 1].append(c)

    return get_ans(stacks)


# -- Tests


def get_example_input() -> str:
    return """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == "CMZ"


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == "MCD"


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == "BSDMQFLSP"


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == "PGSQBFLDP"


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

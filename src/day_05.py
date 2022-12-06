# Standard Library
import re
from collections import defaultdict

# First Party
from utils import read_input


def parse_input(input: str) -> tuple[dict[int, list[str]], list[dict[str, int]]]:
    inital, raw_moves = map(lambda i: i.split("\n"), input.split("\n\n"))

    stacks = defaultdict(lambda: [])
    for row in reversed(inital[:-1]):
        for i in range(1, len(row), 4):
            if row[i] != " ":
                stacks[(i // 4) + 1].append(row[i])

    moves = []
    for move in raw_moves:
        parsed = re.search(r"^move\s(?P<count>\d+)\sfrom\s(?P<from>\d+)\sto\s(?P<to>\d+)$", move, re.MULTILINE)
        if parsed is not None:
            moves.append({k: int(v) for k, v in parsed.groupdict().items()})

    return dict(stacks), moves


def part_1(input: str) -> str:
    stacks, moves = parse_input(input)

    for move in moves:
        stacks[move["to"]].extend([stacks[move["from"]].pop() for _ in range(move["count"])])

    return "".join(f"{stack[-1]}" for stack in stacks.values())


def part_2(input: str) -> str:
    stacks, moves = parse_input(input)

    for move in moves:
        stacks[move["to"]].extend(reversed([stacks[move["from"]].pop() for _ in range(move["count"])]))

    return "".join(f"{stack[-1]}" for stack in stacks.values())


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

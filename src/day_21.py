# Standard Library
import operator
from collections.abc import Callable
from typing import Literal

# First Party
from utils import no_input_skip, read_input

Ops = Literal["+"] | Literal["-"] | Literal["*"] | Literal["/"] | Literal["=="]

Monkeys = dict[str, tuple[str, Callable[[int, int], int | bool], str] | int]
ops: dict[Ops, Callable[[int, int], int | bool]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "==": operator.eq,
}


def resolve(monkey: str, monkeys: Monkeys) -> tuple[int, bool]:
    monk = monkeys[monkey]

    if isinstance(monk, int):
        return monk, False

    left, lefthuman = resolve(monk[0], monkeys)
    right, righthuman = resolve(monk[2], monkeys)

    return int(ops[monk[1]](left, right)), lefthuman or righthuman or monk[0] == "humn" or monk[1] == "humn"


def parse(input: str) -> Monkeys:
    monkeys: Monkeys = {}
    for line in input.split("\n"):
        monkey, job = line.split(": ")
        if job.isnumeric():
            monkeys[monkey] = int(job)
        else:
            left, op, right = job.split(" ")
            monkeys[monkey] = (left, op, right)

    return monkeys


def part_1(input: str) -> int:
    monkeys = parse(input)

    ans, _ = resolve("root", monkeys)
    return ans


def part_2(input: str) -> int:
    monkeys = parse(input)
    root = monkeys["root"]
    if isinstance(root, int):
        raise ValueError("root is int?")

    left, lefthumn = resolve(root[0], monkeys)
    right, _ = resolve(root[2], monkeys)

    if lefthumn:
        correct = right
        to_check = root[0]
    else:
        correct = left
        to_check = root[2]

    def diff() -> int:
        ans, _ = resolve(to_check, monkeys)
        return abs(ans - correct)

    while (d := diff()) != 0:
        monkeys["humn"] += (d // 100) + 1

    return monkeys["humn"]


# -- Tests


def get_example_input() -> str:
    return """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 152


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 301


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 70674280581468


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 3243420789721


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

# Standard Library
import operator

# First Party
from utils import no_input_skip, read_input  # noqa

Monkeys = dict[str, tuple[str, str, str] | int]
Ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def resolve(monkey: str, monkeys: Monkeys) -> int:
    monk = monkeys[monkey]

    if isinstance(monk, int):
        return monk

    left = resolve(monk[0], monkeys)
    right = resolve(monk[2], monkeys)

    return int(Ops[monk[1]](left, right))


def part_1(input: str) -> int:
    monkeys: Monkeys = {}
    for line in input.split("\n"):
        monkey, job = line.split(": ")
        if job.isnumeric():
            monkeys[monkey] = int(job)
        else:
            left, op, right = job.split(" ")
            monkeys[monkey] = (left, op, right)

    return resolve("root", monkeys)


def part_2(input: str) -> int:
    pass


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


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


# @no_input_skip
# def test_part_1_real():
#     real_input = read_input(__file__)
#     assert part_1(real_input) is not None


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

# Standard Library
import operator
from collections import defaultdict
from collections.abc import Callable
from functools import partial
from math import lcm
from typing import Self

# First Party
from utils import read_input


def int_or_zero(s: str) -> int:
    return int(s) if s.isnumeric() else 0


class Monkey:
    def __init__(self, monkey_list: dict[int, Self]) -> None:
        self.monkey_list = monkey_list
        self.items: list[int] = []
        self.op: Callable[[int], int]
        self.test: int = 0
        self.true: int = 0
        self.false: int = 0

        self.inspected: int = 0

    def add(self, item: int):
        self.items.append(item)

    def process_items(self, worry_reducer: Callable[[int], int]):
        while len(self.items):
            self.inspected += 1
            item = worry_reducer(self.op(self.items.pop(0)))
            if item % self.test == 0:
                self.monkey_list[self.true].add(item)
            else:
                self.monkey_list[self.false].add(item)

    @classmethod
    def parse(cls: type[Self], input: str) -> dict[int, Self]:
        def get_op(op_str: str) -> Callable[[int], int]:
            match op_str.split(" = ")[-1].split()[1:]:
                case "*", "old":
                    return lambda x: x * x
                case "*", val:
                    return partial(operator.mul, int(val))
                case "+", val:
                    return partial(operator.add, int(val))
                case _:
                    raise Exception(f"Unknown op: {op_str}")

        monkeys: dict[int, Monkey] = defaultdict(lambda: cls(monkeys))

        for monk in input.split("\n\n"):
            definition = list(map(lambda s: s.strip(), monk.split("\n")))
            _, monk_num = map(int_or_zero, map(lambda s: s.strip(":"), definition.pop(0).split()))

            for line in definition:
                match line.split(":"):
                    case "Starting items", item_string:
                        monkeys[monk_num].items = list(map(int, item_string.split(",")))
                    case "Operation", op:
                        monkeys[monk_num].op = get_op(op.strip())
                    case attr, value:
                        setattr(
                            monkeys[monk_num],
                            attr.lower().split()[-1],
                            int(value.split()[-1]),
                        )
                    case _:
                        raise Exception(f"Unmatched definition line: {line.split(':')}")

        return dict(monkeys)


def round(monkeys: dict[int, Monkey], worry_reducer: Callable[[int], int]):
    for monkey in monkeys.values():
        monkey.process_items(worry_reducer)


def get_monkey_business(monkeys: dict[int, Monkey]) -> int:
    business: list[int] = []
    for monkey in monkeys.values():
        business.append(monkey.inspected)

    business.sort()

    return business.pop() * business.pop()


def part_1(input: str) -> int:
    monkeys = Monkey.parse(input)
    for _ in range(20):
        round(monkeys, lambda x: x // 3)

    return get_monkey_business(monkeys)


def part_2(input: str) -> int:
    monkeys = Monkey.parse(input)
    base = lcm(*[monkey.test for monkey in monkeys.values()])

    for i in range(10000):
        round(monkeys, lambda x: x % base)

    return get_monkey_business(monkeys)


# -- Tests


def get_example_input() -> str:
    return """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 10605


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 2713310158


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 67830


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 15305381442


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

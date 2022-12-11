# Standard Library
from collections import defaultdict
from typing import Self

# First Party
from utils import read_input


def int_or_zero(s: str) -> int:
    return int(s) if s.isnumeric() else 0


class Monkey:
    def __init__(self, monkey_list: dict[int, Self]) -> None:
        self.monkey_list = monkey_list
        self.items: list[int] = []
        self.op: str = ""
        self.test: int = 0
        self.true: int = 0
        self.false: int = 0

        self.inspected: int = 0

    def __str__(self) -> str:
        return "\n====\n" + "\n".join(
            [
                f"items: {self.items}",
                f"op: {self.op}",
                f"test: {self.test}",
                f"  True: {self.true}",
                f"  False: {self.false}",
            ]
        )

    def __repr__(self) -> str:
        return f"{self}"

    def add(self, item: int):
        self.items.append(item)

    def process_items(self, worry_divisor: int):
        def op(old: int) -> int:
            return int(eval(self.op))

        while len(self.items):
            self.inspected += 1
            item = op(self.items.pop(0))
            if worry_divisor > 1:
                item = item // worry_divisor
            if item % self.test == 0:
                self.monkey_list[self.true].add(item)
            else:
                self.monkey_list[self.false].add(item)

    @classmethod
    def parse(cls: type[Self], input: str) -> dict[int, Self]:
        monkeys: dict[int, Monkey] = defaultdict(lambda: cls(monkeys))

        for monk in input.split("\n\n"):
            definition = list(map(lambda s: s.strip(), monk.split("\n")))
            _, monk_num = map(int_or_zero, map(lambda s: s.strip(":"), definition.pop(0).split()))

            for line in definition:
                match line.split(":"):
                    case "Starting items", item_string:
                        monkeys[monk_num].items = list(map(int, item_string.split(",")))
                    case "Operation", op:
                        _, op = op.strip().split(" = ")
                        monkeys[monk_num].op = op
                    case "Test", test:
                        monkeys[monk_num].test = sum(map(int_or_zero, test.split()))
                    case "If true", true:
                        monkeys[monk_num].true = sum(map(int_or_zero, true.split()))
                    case "If false", false:
                        monkeys[monk_num].false = sum(map(int_or_zero, false.split()))
                    case _:
                        raise Exception(f"Unmatched definition line: {line.split(':')}")

        return dict(monkeys)


def round(monkeys: dict[int, Monkey], worry_divisor: int):
    for monkey in monkeys.values():
        monkey.process_items(worry_divisor)


def part_1(input: str) -> int:
    monkeys = Monkey.parse(input)
    for _ in range(20):
        round(monkeys, 3)

    business: list[int] = []
    for monkey in monkeys.values():
        business.append(monkey.inspected)

    business.sort()

    return business.pop() * business.pop()


def part_2(input: str) -> int:
    monkeys = Monkey.parse(input)
    for i in range(1000):
        if (i % 100) == 0:
            print(i)
        round(monkeys, 1)

    business: list[int] = []
    for monkey in monkeys.values():
        business.append(monkey.inspected)

    business.sort()

    return business.pop() * business.pop()


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


# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

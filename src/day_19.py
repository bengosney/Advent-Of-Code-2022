# Standard Library
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Self

# First Party
from utils import no_input_skip, read_input  # noqa

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"


@dataclass(frozen=True)
class Robot:
    cost: dict[str, int]
    type: str

    def can_build(self, resources: dict[str, int]) -> bool:
        return all(c <= resources[t] for t, c in self.cost.items())


@dataclass(frozen=True)
class resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def __add__(self, other: Self):
        return resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )


@dataclass
class Sim:
    blueprints: dict[str, Robot]
    resources: dict[str, int]
    robots: dict[str, int]

    rounds: int = 24
    minute: int = 0

    debug: bool = True

    def print(self, *args, **kwargs) -> None:
        if self.debug is not False:
            print(*args, **kwargs)

    @cached_property
    def sum(self) -> dict[str, int]:
        maxes = defaultdict(lambda: 0)
        for blueprint in self.blueprints.values():
            for k, v in blueprint.cost.items():
                maxes[k] += v

        return dict(maxes)

    def round(self):
        new = defaultdict(lambda: 0)
        to_try = [GEODE]

        to_try.extend(_type for _type in [ORE, CLAY, OBSIDIAN] if self.robots[_type] < self.sum[_type])
        for _type in to_try:
            blueprint = self.blueprints[_type]
            if blueprint.can_build(self.resources):
                new[blueprint.type] += 1
                spent: list[str] = []
                for t, c in blueprint.cost.items():
                    self.resources[t] -= c
                    spent.append(f"{c} {t}")
                break

        for t, c in self.robots.items():
            if c > 0:
                self.resources[t] += c

        for _type, count in new.items():
            self.robots[_type] += count

    def play(self) -> int:
        for i in range(self.rounds):
            self.minute = i
            self.round()

        return self.resources[GEODE]


def parse(line: str):
    type_regex = r"Each (\w+)"
    cost_regex = r"(costs|and) (\d+) (\w+)"

    robot_defs: dict[str, Robot] = {}

    _, robots = line.split(": ")
    for raw_robot in robots.split(". "):
        type_res = re.findall(type_regex, raw_robot, re.MULTILINE)[0]
        cost_res = re.findall(cost_regex, raw_robot, re.MULTILINE)

        costs: dict[str, int] = {}
        for cost in cost_res:
            _, c, t = cost
            costs[t] = int(c)

        robot_defs[type_res] = Robot(costs, type_res)

    sim = cls(robot_defs, defaultdict(lambda: 0), defaultdict(lambda: 0))
    sim.robots[ORE] = 1

    return sim


def part_1(input: str) -> int:
    sims: list[Sim] = []

    for line in input.split("\n"):
        sims.append(parse(line))
        break

    return sum(s.play() for s in sims)


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""  # noqa


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 33


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

    real_input = get_example_input()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

# Standard Library
import re
from dataclasses import dataclass
from functools import cache

# First Party
from utils import no_input_skip, read_input


@dataclass(frozen=True)
class Valve:
    name: str
    flow: int
    connected: list[str]


def parse(input: str) -> dict[str, Valve]:
    valves: dict[str, Valve] = {}
    regex = r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z\s,]+)$"

    for row in input.split("\n"):
        name, flow, joined = re.findall(regex, row, re.MULTILINE)[0]
        valves[name] = Valve(name, int(flow), joined.split(", "))

    return valves


@cache
def add_to(opened: frozenset, new: str) -> frozenset:
    _opened = set(opened)
    _opened.add(new)

    return frozenset(_opened)


def part_1(input: str) -> int:
    valves = parse(input)

    @cache
    def tick(mins: int, opened: frozenset, curr: str) -> int:
        if mins <= 0:
            return 0

        max_release = 0
        for valve in valves[curr].connected:
            max_release = max(max_release, tick(mins - 1, opened, valve))

        if curr not in opened and valves[curr].flow > 0:
            mins -= 1
            valve_released = mins * valves[curr].flow
            for valve in valves[curr].connected:
                max_release = max(max_release, valve_released + tick(mins - 1, add_to(opened, curr), valve))

        return max_release

    return tick(30, frozenset(), "AA")


def part_2(input: str) -> int:
    valves = parse(input)

    @cache
    def tick(mins: int, opened: frozenset[str], curr: str, elephant: bool) -> int:
        if mins <= 0:
            return tick(26, opened, "AA", False) if elephant else 0

        best = 0
        for valve in valves[curr].connected:
            best = max(best, tick(mins - 1, opened, valve, elephant))

        if curr not in opened and valves[curr].flow > 0:
            mins -= 1
            released = mins * valves[curr].flow
            for valve in valves[curr].connected:
                best = max(best, released + tick(mins - 1, add_to(opened, curr), valve, elephant))

        return best

    return tick(26, frozenset(), "AA", True)


# -- Tests


def get_example_input() -> str:
    return """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 1651


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 1707


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 1923


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 2594


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

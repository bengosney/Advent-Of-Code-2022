# Standard Library
import contextlib
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

# First Party
from utils import no_input_skip, read_input


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, delta: Self) -> Self:
        return Vec(self.x + delta.x, self.y + delta.y)

    def dist_to(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(frozen=True)
class Sensor:
    pos: Vec
    beacon: Vec

    def dist(self) -> int:
        return self.pos.dist_to(self.beacon)

    def covers(self, row: int) -> set[int]:
        cover_x = self.dist() - abs(self.pos.y - row)
        thing = set()
        if cover_x > 0:
            for x in range(-cover_x, cover_x + 1):
                thing.add(self.pos.x + x)
        return thing

    def walk(self) -> Iterable[Vec]:
        dist = self.dist()
        for x in range(-dist, dist + 1):
            y_dist = dist - abs(x)
            for y in range(-y_dist, y_dist + 1):
                yield self.pos + Vec(x, y)


def part_1(input: str, test_row: int) -> int:
    regex = r"x=(-?\d+),\s+y=(-?\d+)"

    sensors: list[Sensor] = []
    for row in input.split("\n"):
        matches = re.findall(regex, row, re.MULTILINE)
        _sensor = Vec(*map(int, matches[0]))
        _beacon = Vec(*map(int, matches[1]))

        sensor = Sensor(_sensor, _beacon)
        sensors.append(sensor)

    covers = set()
    for sensor in sensors:
        covers |= sensor.covers(test_row)

    for sensor in sensors:
        if sensor.beacon.y == test_row:
            with contextlib.suppress(KeyError):
                covers.remove(sensor.beacon.x)

    return len(covers)


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input, 10) == 26


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input, 2000000) == 5176944


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":

    part_1(get_example_input(), 10)

    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input, 2000000)}")
    print(f"Part2: {part_2(real_input)}")

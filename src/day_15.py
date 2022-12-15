# Standard Library
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

    def is_in_range(self, max_pos: int, min_pos: int = 0) -> bool:
        return min_pos < self.x < max_pos and min_pos < self.y < max_pos


@dataclass(frozen=True)
class Sensor:
    pos: Vec
    beacon: Vec

    def __int__(self) -> int:
        return self.pos.dist_to(self.beacon)

    def covers(self, row: int) -> set[int]:
        cover_x = int(self) - abs(self.pos.y - row)
        covered = set()
        if cover_x > 0:
            for x in range(-cover_x, cover_x + 1):
                covered.add(self.pos.x + x)
        return covered

    def contains(self, point: Vec) -> bool:
        return int(self) >= self.pos.dist_to(point)

    def walk_edges(self) -> Iterable[Vec]:
        sx = self.pos.x
        sy = self.pos.y

        for x in range(-1, int(self) + 1):
            y = (int(self) - 1) - x

            yield Vec((sx + x) + 1, (sy + y) + 1)
            yield Vec((sx - x) - 2, (sy - y) - 1)
            yield Vec((sx + x) + 1, (sy - y) - 1)
            yield Vec((sx - x) - 1, (sy + y) + 1)


def get_sensors(input: str) -> Iterable[Sensor]:
    regex = r"x=(-?\d+),\s+y=(-?\d+)"

    for row in input.split("\n"):
        matches = re.findall(regex, row, re.MULTILINE)
        yield Sensor(Vec(*map(int, matches[0])), Vec(*map(int, matches[1])))


def part_1(input: str, test_row: int) -> int:
    sensors = get_sensors(input)

    covers = set()
    beacons = set()
    for sensor in sensors:
        covers |= sensor.covers(test_row)
        if sensor.beacon.y == test_row:
            beacons.add(sensor.beacon.x)

    return len(covers - beacons)


def part_2(input: str, max_pos: int) -> int:
    sensors = list(get_sensors(input))

    for i in range(len(sensors)):
        for e in sensors[i].walk_edges():
            if e.is_in_range(max_pos) and all(not sensors[j].contains(e) for j in range(i - 1, len(sensors))):
                return (e.x * 4000000) + e.y

    raise Exception("Nothing found")


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


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input, 20) == 56000011


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input, 2000000) == 5176944


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input, 4000000) == 13350458933732


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input, 2000000)}")
    print(f"Part2: {part_2(real_input, 4000000)}")

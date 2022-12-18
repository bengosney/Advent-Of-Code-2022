# Standard Library
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cached_property, partial
from typing import Self

# First Party
from utils import no_input_skip, read_input


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    def __add__(self, delta: Self) -> Self:
        return Cube(
            self.x + delta.x,
            self.y + delta.y,
            self.z + delta.z,
        )

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

    def sum(self) -> int:
        return self.x + self.y + self.z

    def adj(self) -> Iterable[Self]:
        yield Cube(self.x + 1, self.y + 0, self.z + 0)
        yield Cube(self.x - 1, self.y + 0, self.z + 0)

        yield Cube(self.x + 0, self.y + 1, self.z + 0)
        yield Cube(self.x + 0, self.y - 1, self.z + 0)

        yield Cube(self.x + 0, self.y + 0, self.z + 1)
        yield Cube(self.x + 0, self.y + 0, self.z - 1)


@dataclass(frozen=True)
class Bounds:
    x: list[int]
    y: list[int]
    z: list[int]

    def __contains__(self, other: Cube):
        return all(
            [
                self.min_x < other.x < self.max_x,
                self.min_y < other.y < self.max_y,
                self.min_z < other.z < self.max_z,
            ]
        )

    @cached_property
    def volume(self) -> int:
        return (self.max_x - self.min_x) * (self.max_y - self.min_y) * (self.max_z - self.min_z)

    @classmethod
    def from_cubes(cls: type[Self], cubes: list[Cube]) -> Self:
        xs = []
        ys = []
        zs = []

        for cube in cubes:
            xs.append(cube.x)
            ys.append(cube.y)
            zs.append(cube.z)

        return cls(xs, ys, zs)

    @cached_property
    def min_x(self) -> int:
        return min(self.x)

    @cached_property
    def max_x(self) -> int:
        return max(self.x)

    @cached_property
    def min_y(self) -> int:
        return min(self.y)

    @cached_property
    def max_y(self) -> int:
        return max(self.y)

    @cached_property
    def min_z(self) -> int:
        return min(self.z)

    @cached_property
    def max_z(self) -> int:
        return max(self.z)


def get_cubes(input: str) -> list[Cube]:
    cubes: list[Cube] = []
    for line in input.split("\n"):
        cube = Cube(*map(int, line.split(",")))
        cubes.append(cube)
    return cubes


def part_1(input: str) -> int:
    cubes = get_cubes(input)

    faces = 0
    for cube in cubes:
        faces += 6

        for adj in cube.adj():
            if adj in cubes:
                faces -= 1

    return faces


enclosed_cache: dict[Cube, bool] = {}


def is_enclosed(cube: Cube, cubes: list[Cube], bounds: Bounds) -> bool:
    to_check: list[Cube] = [cube]
    checked: set[Cube] = set()

    while len(to_check):
        checking = to_check.pop(0)

        if checking in enclosed_cache:
            return enclosed_cache[checking]

        checked.add(checking)

        if checking not in bounds:
            for c in checked:
                enclosed_cache[c] = False
            return False

        for adj in checking.adj():
            if adj not in checked and adj not in cubes and adj not in to_check:
                to_check.append(adj)

    for c in checked:
        enclosed_cache[c] = True

    return True


def part_2(input: str) -> int:
    cubes = get_cubes(input)
    bounds = Bounds.from_cubes(cubes)

    enclosed = partial(is_enclosed, cubes=cubes, bounds=bounds)

    faces = 0
    for cube in cubes:
        faces += 6

        for adj in cube.adj():
            if adj in cubes or enclosed(adj):
                faces -= 1

    return faces


# -- Tests


def get_example_input() -> str:
    return """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 64


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 58


def test_bounds():
    cubes = get_cubes(get_example_input())
    bounds = Bounds.from_cubes(cubes)

    enclosed = partial(is_enclosed, cubes=cubes, bounds=bounds)

    cube = Cube(50, 50, 50)
    assert enclosed(cube) is False


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 4604


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 2604


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

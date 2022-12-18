# Standard Library
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

# First Party
from utils import no_input_skip, read_input  # noqa


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    def adj(self) -> Iterable[Self]:
        yield Cube(self.x + 1, self.y + 0, self.z + 0)
        yield Cube(self.x - 1, self.y + 0, self.z + 0)

        yield Cube(self.x + 0, self.y + 1, self.z + 0)
        yield Cube(self.x + 0, self.y - 1, self.z + 0)

        yield Cube(self.x + 0, self.y + 0, self.z + 1)
        yield Cube(self.x + 0, self.y + 0, self.z - 1)


def part_1(input: str) -> int:
    cubes: list[Cube] = []
    for line in input.split("\n"):
        cube = Cube(*map(int, line.split(",")))
        cubes.append(cube)

    faces = 0
    for cube in cubes:
        faces += 6

        for adj in cube.adj():
            if adj in cubes:
                faces -= 1

    return faces


def part_2(input: str) -> int:
    pass


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

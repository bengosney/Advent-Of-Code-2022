# Standard Library
from dataclasses import dataclass
from typing import Self

# First Party
from utils import read_input

# Third Party
from icecream import ic


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, delta: Self) -> Self:
        return Vec(self.x + delta.x, self.y + delta.y)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __repr__(self) -> str:
        return str(self)


@dataclass(frozen=True)
class Node:
    pos: Vec
    connected: list[Vec]


UP = Vec(0, -1)
DOWN = Vec(0, 1)
LEFT = Vec(-1, 0)
RIGHT = Vec(1, 0)

MOVES = [UP, DOWN, LEFT, RIGHT]


def draw(grid: dict[Vec, int], data: dict[Vec, str] = {}):
    width = 0
    height = 0
    for v in grid:
        width = max(width, v.x)
        height = max(height, v.y)

    width += 1
    height += 1
    print("=" * width)
    for y in range(height):
        row = "".join(data.get(Vec(x, y), ".") for x in range(width))
        print(row)
    print("=" * width)


def part_1(input: str) -> int:
    grid: dict[Vec, int] = {}
    start: Vec = Vec(-1, -1)
    end: Vec = Vec(-1, -1)

    vals = {}

    for y, line in enumerate(input.split("\n")):
        for x, col in enumerate(line):
            vals[Vec(x, y)] = col
            match col:
                case "S":
                    start = Vec(x, y)
                    grid[Vec(x, y)] = 0
                case "E":
                    end = Vec(x, y)
                    grid[Vec(x, y)] = 26
                case height:
                    grid[Vec(x, y)] = ord(height) - 96

    nodes: dict[Vec, Node] = {}
    for p in grid:
        connected = []
        for m in MOVES:
            n = p + m
            if n in grid and abs(grid[n] - grid[p]) <= 1:
                connected.append(n)

        nodes[p] = Node(pos=p, connected=connected)

    # ic(start)
    # ic(end)
    # ic(nodes)
    def pathfind():
        paths = [[start]]
        visited = []
        while len(paths):
            path = paths.pop(0)
            for curr in nodes[path[-1]].connected:
                if curr not in path and curr not in visited:
                    newpath = list(path)
                    newpath.append(curr)
                    if curr == end:
                        return newpath

                    paths.append(newpath)
                    visited.append(curr)
        raise Exception("no path found")

    path = pathfind()

    ic(path)
    g = {}
    for thing in path:
        g[thing] = vals[thing]
    draw(grid, vals)
    draw(grid, g)

    return len(path) - 1


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 31


# def test_part_2():
#     test_input = get_example_input()
#     assert part_2(test_input) is not None


# def test_part_1_real():
#     real_input = read_input(__file__)
#     assert part_1(real_input) is not None


# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

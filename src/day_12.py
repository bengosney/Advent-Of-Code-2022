# Standard Library
import contextlib
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


def draw(grid: dict[Vec, int], data: dict[Vec, str] = {}, colour: dict[Vec, str] = {}):
    width = 0
    height = 0
    for v in grid:
        width = max(width, v.x)
        height = max(height, v.y)

    width += 1
    height += 1
    print("=" * width)
    for y in range(height):
        row = ""
        for x in range(width):
            row += colour.get(Vec(x, y), "") + data.get(Vec(x, y), ".") + "\033[0m"
        print(row)
    print("=" * width)


def get_moves(grid, curr):
    for move in MOVES:
        new = move + curr
        with contextlib.suppress(KeyError):
            if abs(grid[new] - grid[curr]) <= 1:
                yield new


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
                    grid[Vec(x, y)] = ord("a")
                case "E":
                    end = Vec(x, y)
                    grid[Vec(x, y)] = ord("z")
                case height:
                    grid[Vec(x, y)] = ord(height)

    nodes: dict[Vec, Node] = {}
    for pos in grid:
        connected = []
        for move in MOVES:
            new = pos + move
            with contextlib.suppress(KeyError):
                if (grid[pos] + 1) >= grid[new]:
                    connected.append(new)

        # if len(connected) == 1:
        #    ic(p)
        nodes[pos] = Node(pos=pos, connected=connected)

    ic(start)
    ic(end)

    visited: list[Vec] = []

    def pathfind(start_point: Vec, end_point: Vec):
        paths = [[start_point]]
        while len(paths):
            path = paths.pop(0)
            for curr in nodes[path[-1]].connected:
                if curr not in path and curr not in visited:
                    newpath = list(path)
                    newpath.append(curr)
                    if curr == end_point:
                        return newpath

                    paths.append(newpath)
                    visited.append(curr)

                get_moves(grid, curr)
                # ic(f"dead end: {vals[curr]} {','.join([vals[c] for c in adj])}")
        raise Exception(f"no path found: {len(visited)}")

    try:
        path = pathfind(start, end)
    except Exception as e:
        draw(grid, vals, {k: "\033[92m" for k in visited})
        print("".join([chr(i) for i in range(ord("a"), ord("z") + 1)]))
        raise e

    ic(path)
    g = {}
    for thing in path:
        g[thing] = vals[thing]
    draw(grid, vals)
    draw(grid, g)

    return len(path) - 1


def part_2(input: str) -> int:
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
                    grid[Vec(x, y)] = ord("a")
                case "E":
                    end = Vec(x, y)
                    grid[Vec(x, y)] = ord("z")
                case height:
                    grid[Vec(x, y)] = ord(height)

    nodes: dict[Vec, Node] = {}
    for pos in grid:
        connected = []
        for move in MOVES:
            new = pos + move
            with contextlib.suppress(KeyError):
                if grid[pos] == grid[new]:
                    connected.append(new)

                if (grid[pos] - 1) == grid[new]:
                    connected.append(new)

                if grid[pos] < grid[new]:
                    connected.append(new)

        # if len(connected) == 1:
        #    ic(p)
        nodes[pos] = Node(pos=pos, connected=connected)

    ic(start)
    ic(end)

    visited: list[Vec] = []

    def pathfind(start_point: Vec):
        paths = [[start_point]]
        while len(paths):
            path = paths.pop(0)
            for curr in nodes[path[-1]].connected:
                if curr not in path and curr not in visited:
                    newpath = list(path)
                    newpath.append(curr)
                    if grid[curr] == ord("a"):
                        return newpath

                    paths.append(newpath)
                    visited.append(curr)

                get_moves(grid, curr)
                # ic(f"dead end: {vals[curr]} {','.join([vals[c] for c in adj])}")
        raise Exception(f"no path found: {len(visited)}")

    try:
        path = pathfind(end)
    except Exception as e:
        draw(grid, vals, {k: "\033[92m" for k in visited})
        print("".join([chr(i) for i in range(ord("a"), ord("z") + 1)]))
        raise e

    ic(path)
    g = {}
    for thing in path:
        g[thing] = vals[thing]
    draw(grid, vals)
    draw(grid, g)

    return len(path) - 1


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


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) is not None


# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

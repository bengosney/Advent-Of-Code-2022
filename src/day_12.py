# Standard Library
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Self

# First Party
from utils import read_input


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, delta: Self) -> Self:
        return Vec(self.x + delta.x, self.y + delta.y)


@dataclass(frozen=True)
class Node:
    pos: Vec
    connected: list[Vec]


def moves(curr: Vec) -> Iterable[Vec]:
    for move in [Vec(0, -1), Vec(0, 1), Vec(-1, 0), Vec(1, 0)]:
        yield move + curr


def build_grid(input: str) -> tuple[Vec, Vec, dict[Vec, int]]:
    grid: dict[Vec, int] = {}
    start: Vec = Vec(-1, -1)
    end: Vec = Vec(-1, -1)

    for y, line in enumerate(input.split("\n")):
        for x, col in enumerate(line):
            match col:
                case "S":
                    start = Vec(x, y)
                    grid[Vec(x, y)] = ord("a")
                case "E":
                    end = Vec(x, y)
                    grid[Vec(x, y)] = ord("z")
                case height:
                    grid[Vec(x, y)] = ord(height)

    return start, end, grid


def path_find(nodes: dict[Vec, Node], start_point: Vec, end_condition: Callable[[Vec], bool]):
    paths: list[list[Vec]] = [[start_point]]
    visited: set[Vec] = set()
    while len(paths):
        path = paths.pop(0)
        for curr in nodes[path[-1]].connected:
            if end_condition(curr):
                return path

            if curr not in visited:
                new_path = list(path)
                new_path.append(curr)
                paths.append(new_path)
                visited.add(curr)

    raise Exception(f"no path found: {len(visited)}")


def part_1(input: str) -> int:
    start, end, grid = build_grid(input)

    nodes: dict[Vec, Node] = {}
    for pos in grid:
        connected = [new for new in moves(pos) if new in grid and (grid[pos] + 1) >= grid[new]]
        nodes[pos] = Node(pos=pos, connected=connected)

    path = path_find(nodes, start, lambda c: c == end)

    return len(path)


def part_2(input: str) -> int:
    _, end, grid = build_grid(input)

    nodes: dict[Vec, Node] = {}
    for pos in grid:
        connected = [new for new in moves(pos) if new in grid and (grid[pos] - 1) <= grid[new]]
        nodes[pos] = Node(pos=pos, connected=connected)

    path = path_find(nodes, end, lambda c: grid[c] == ord("a"))

    return len(path)


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


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 29


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 468


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 459


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

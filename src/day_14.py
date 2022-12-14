# Standard Library
from collections import defaultdict
from itertools import pairwise

# First Party
from utils import no_input_skip, read_input

Point = tuple[int, int]
Sim = dict[Point, str]


def draw(sim: Sim) -> None:
    x = list(map(lambda k: k[0], sim))
    y = list(map(lambda k: k[1], sim))

    def _range(i: list[int], padding: int = 2):
        return range(min(i) - padding, (max(i) + padding))

    print("---")
    for _y in _range(y):
        for _x in _range(x):
            print("+" if (_x, _y) == START else sim[(_x, _y)], end="")
        print()
    print("---")


def step(sim: Sim, x: int, y: int, floor: int = 0) -> tuple[int, int]:
    if y + 1 != floor:
        if sim[(x, y + 1)] == ".":
            return x, y + 1
        elif sim[(x - 1, y + 1)] == ".":
            return x - 1, y + 1
        elif sim[(x + 1, y + 1)] == ".":
            return x + 1, y + 1

    return x, y


START: Point = 500, 0


def init_sim(input: str) -> tuple[Sim, int]:
    sim: Sim = defaultdict(lambda: ".")

    for row in input.split("\n"):
        points = row.split(" -> ")

        for p1, p2 in pairwise(points):
            x1, y1 = map(int, p1.split(","))
            x2, y2 = map(int, p2.split(","))

            for i in range(min(x1, x2), max(x1, x2) + 1):
                sim[(i, y1)] = "#"

            for i in range(min(y1, y2), max(y1, y2) + 1):
                sim[(x1, i)] = "#"

    return sim, max(map(lambda k: k[1], sim.keys()))


def part_1(input: str) -> int:
    sim, max_y = init_sim(input)

    sand = 0
    px, py = START

    while True:
        cx, cy = step(sim, px, py)

        if cy > max_y:
            return sand

        if cx == px and cy == py:
            px, py = START
            sand += 1
            sim[(cx, cy)] = "o"
        else:
            px = cx
            py = cy


def part_2(input: str) -> int:
    sim, max_y = init_sim(input)

    sand = 1
    px, py = START
    floor = max_y + 2

    while True:
        cx, cy = step(sim, px, py, floor)

        if (cx, cy) == START:
            return sand

        if cx == px and cy == py:
            px, py = START
            sand += 1
            sim[(cx, cy)] = "o"
        else:
            px = cx
            py = cy


# -- Tests


def get_example_input() -> str:
    return """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 24


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 93


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 674


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 24958


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    # real_input = get_example_input()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

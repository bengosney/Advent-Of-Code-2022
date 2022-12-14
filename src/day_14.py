# Standard Library
from collections import defaultdict

# First Party
from utils import no_input_skip, read_input


def draw(sim, x: tuple[int, int], y: tuple[int, int]):
    pad = 5
    print()
    for _y in range(y[0] - pad, (y[1] + pad)):
        row = ""
        for _x in range(x[0] - pad, x[1] + pad):
            row += sim[(_x, _y)]
        print(row)
    print(f"{x}, {y}")


def step(sim, x: int, y: int, floor: int = 0) -> tuple[int, int]:
    if y + 1 == floor:
        return x, y

    if sim[(x, y + 1)] == ".":
        return x, y + 1

    if sim[(x - 1, y + 1)] == ".":
        return x - 1, y + 1

    if sim[(x + 1, y + 1)] == ".":
        return x + 1, y + 1

    return x, y


Point = tuple[int, int]
Sim = dict[Point, str]

START: Point = 500, 0


def init_sim(input: str) -> tuple[Sim, int]:
    max_y: int = 0
    sim: Sim = defaultdict(lambda: ".")

    for row in input.split("\n"):
        points = row.split(" -> ")
        point = points.pop(0)
        x1, y1 = map(int, point.split(","))
        while len(points):
            point = points.pop(0)
            x2, y2 = map(int, point.split(","))

            sim[(x1, y1)] = "#"

            for i in range(min(x1, x2), max(x1, x2) + 1):
                sim[(i, y1)] = "#"

            for i in range(min(y1, y2), max(y1, y2) + 1):
                sim[(x1, i)] = "#"

            max_y = max(max_y, y2, y1)

            x1 = x2
            y1 = y2

    return sim, max_y


def part_1(input: str) -> int:
    sim, max_y = init_sim(input)

    sand = 0
    px, py = START
    sim[(500, 0)] = "+"
    for _ in range(500000):
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
    raise Exception("Sim over time")


def part_2(input: str) -> int:
    sim, max_y = init_sim(input)

    sand = 1
    px, py = START
    sim[(500, 0)] = "+"
    for _ in range(10000000):
        cx, cy = step(sim, px, py, max_y + 2)

        if (cx, cy) == START:
            return sand
        if cx == px and cy == py:
            px, py = START
            sand += 1
            sim[(cx, cy)] = "o"
        else:
            px = cx
            py = cy
    raise Exception("Sim over time")


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

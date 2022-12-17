# Standard Library
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import cycle
from typing import DefaultDict, Self

# First Party
from utils import no_input_skip, read_input  # noqa

# Third Party
from icecream import ic


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, delta: Self) -> Self:
        return Vec(self.x + delta.x, self.y + delta.y)

    def __sub__(self, delta: Self) -> Self:
        return Vec(self.x - delta.x, self.y - delta.y)


@dataclass(frozen=True)
class Shape:
    points: list[Vec]

    def __add__(self, delta: Vec) -> Self:
        return Shape([vec + delta for vec in self.points])

    def __contains__(self, pos: Vec) -> bool:
        return pos in self.points

    @property
    def left(self) -> int:
        return min(p.x for p in self.points)

    @property
    def right(self) -> int:
        return max(p.x for p in self.points)

    @property
    def bottom(self) -> int:
        return min(p.y for p in self.points)

    @property
    def top(self) -> int:
        return max(p.y for p in self.points)


SPAWN_GAP = 4

DOWN = Vec(0, -1)
LEFT = Vec(-1, 0)
RIGHT = Vec(1, 0)

SHAPES = [
    Shape([Vec(0, 0), Vec(1, 0), Vec(2, 0), Vec(3, 0)]),
    Shape([Vec(1, 0), Vec(0, 1), Vec(1, 1), Vec(2, 1), Vec(1, 2)]),
    Shape([Vec(0, 0), Vec(1, 0), Vec(2, 0), Vec(2, 1), Vec(2, 2)]),
    Shape([Vec(0, 0), Vec(0, 1), Vec(0, 2), Vec(0, 3)]),
    Shape([Vec(0, 0), Vec(0, 1), Vec(1, 0), Vec(1, 1)]),
]


class Game:
    def __init__(self, jets: list[Vec], shapes: list[Shape]) -> None:
        self.board: DefaultDict[Vec, str] = defaultdict(lambda: ".")
        for x in range(7):
            self.board[Vec(x, 0)] = "="
        self.jets: Iterable[Vec] = cycle(jets)
        self.shapes: Iterable[Shape] = cycle(shapes)
        self.rock: Shape | None = None
        self.rock_count: int = 0
        self.jet_count: int = 0
        self.spawn: int = SPAWN_GAP
        self.last_jet: str = ""

        self.draw_step = 0
        self.pause: bool = False

    @property
    def height(self):
        return self.spawn - SPAWN_GAP

    def init_rock(self) -> bool:
        if self.rock is None:
            self.rock = next(self.shapes) + Vec(2, self.spawn)
            self.rock_count += 1
            return True
        return False

    def move(self):
        if self.rock is None:
            raise Exception("No rock to move down")

        m = next(self.jets)
        self.jet_count += 1
        rock = self.rock + m

        self.last_jet = "left" if m == LEFT else "right"

        if any(self.board[r] != "." for r in rock.points):
            return

        if rock.left >= 0 and rock.right <= 6:
            self.rock = rock

    def down(self):
        if self.rock is None:
            raise Exception("No rock to move down")

        rock = self.rock + DOWN
        if any(self.board[r] != "." for r in rock.points):
            for r in self.rock.points:
                self.board[r] = str(self.rock_count % len(SHAPES))
            self.spawn = max(self.spawn, self.rock.top + SPAWN_GAP)
            self.rock = None
        else:
            self.rock += DOWN

    def round(self, input: str = ""):
        if self.init_rock():
            self.draw(f"Spawn Rock {self.spawn}")
        self.move()
        # print(f"{self.jet_count} : {self.last_jet}")
        self.draw(f"Jet {self.last_jet}")
        self.down()
        self.draw("Down")

    def draw(self, txt: str = "", pause: bool = True):
        return
        self.draw_step += 1

        print(f"\n=== {self.draw_step} {txt}")

        for y in range(self.spawn + 5, 0, -1):
            print(f"{y:4} |", end="")
            for x in range(7):
                pos = Vec(x, y)
                if self.rock and pos in self.rock:
                    print("@", end="")
                else:
                    print(self.board[pos], end="")
            print("|")
        print("     +-------+")
        print(f"height: {self.height} rocks: {self.rock_count} jet count: {self.jet_count}")
        input()


def part_1(input_string: str) -> int:
    ic(len(input_string))
    jets = [LEFT if d == "<" else RIGHT for d in input_string]
    game = Game(jets, SHAPES)

    while game.rock_count < 2023:
        # while game.height < 3068:
        game.round()
    game.draw()

    ic(game.rock_count)

    return game.height


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 3068


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

    # real_input = get_example_input()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

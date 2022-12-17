# Standard Library
from dataclasses import dataclass
from typing import Self

# First Party
from utils import no_input_skip, read_input  # noqa


@dataclass(frozen=True)
class Shape:
    points: list[complex]

    def __add__(self, delta: complex) -> Self:
        return Shape([p + delta for p in self.points])

    def __contains__(self, pos: complex) -> bool:
        return pos in self.points

    @property
    def left(self) -> int:
        return min(int(p.real) for p in self.points)

    @property
    def right(self) -> int:
        return max(int(p.real) for p in self.points)

    @property
    def bottom(self) -> int:
        return min(int(p.imag) for p in self.points)

    @property
    def top(self) -> int:
        return max(int(p.imag) for p in self.points)


SPAWN_GAP = 4

DOWN = complex(0, -1)
LEFT = complex(-1, 0)
RIGHT = complex(1, 0)

SHAPES = [
    Shape([complex(0, 0), complex(1, 0), complex(2, 0), complex(3, 0)]),
    Shape([complex(1, 0), complex(0, 1), complex(1, 1), complex(2, 1), complex(1, 2)]),
    Shape([complex(0, 0), complex(1, 0), complex(2, 0), complex(2, 1), complex(2, 2)]),
    Shape([complex(0, 0), complex(0, 1), complex(0, 2), complex(0, 3)]),
    Shape([complex(0, 0), complex(0, 1), complex(1, 0), complex(1, 1)]),
]


class Game:
    def __init__(self, jets: list[complex], shapes: list[Shape]) -> None:
        self.board: dict[complex, str] = {}
        for x in range(7):
            self.board[complex(x, 0)] = "="
        self.jets: list[complex] = jets
        self.shapes: list[Shape] = shapes
        self.rock: Shape | None = None
        self.rock_idx: int = 0
        self.jet_idx: int = 0
        self.spawn: int = SPAWN_GAP
        self.last_jet: str = ""

        self.draw_step = 0
        self.pause: bool = False

        self.cache = {}

    @property
    def height(self):
        return self.spawn - SPAWN_GAP

    def init_rock(self) -> bool:
        if self.rock is None:
            self.rock = self.shapes[self.rock_idx % len(self.shapes)] + complex(2, self.spawn)
            self.rock_idx += 1
            return True
        return False

    def move(self):
        if self.rock is None:
            raise Exception("No rock to move down")

        m = self.jets[self.jet_idx % len(self.jets)]
        self.jet_idx += 1
        rock = self.rock + m

        self.last_jet = "left" if m == LEFT else "right"

        if any(r in self.board for r in rock.points):
            return

        if rock.left >= 0 and rock.right <= 6:
            self.rock = rock

    def down(self):
        if self.rock is None:
            raise Exception("No rock to move down")

        rock = self.rock + DOWN
        if any(r in self.board for r in rock.points):
            for r in self.rock.points:
                self.board[r] = str(self.rock_idx % len(SHAPES))
            self.spawn = max(self.spawn, self.rock.top + SPAWN_GAP)
            self.rock = None
        else:
            self.rock += DOWN

    def round(self):
        self.init_rock()
        self.move()
        self.down()


def part_1(input_string: str) -> int:
    jets = [LEFT if d == "<" else RIGHT for d in input_string]
    game = Game(jets, SHAPES)

    while game.rock_idx < 2023:
        game.round()

    return game.height


def part_2(input_string: str) -> int:
    jets = [LEFT if d == "<" else RIGHT for d in input_string]
    game = Game(jets, SHAPES)

    while game.rock_idx < 1000000000000:
        game.round()

    return game.height


# -- Tests


def get_example_input() -> str:
    return ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 3068


# def test_part_2():
#   test_input = get_example_input()
#   assert part_2(test_input) == 1514285714288


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

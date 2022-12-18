# Standard Library
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Self

# First Party
from utils import no_input_skip, read_input


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
        self.board: DefaultDict[complex, str] = defaultdict(lambda: ".")
        self.jets: list[complex] = jets
        self.shapes: list[Shape] = shapes
        self.rock: Shape | None = None
        self.rock_idx: int = 0
        self.jet_idx: int = 0
        self.spawn: int = SPAWN_GAP

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
        if any(r in self.board for r in rock.points) or rock.bottom == 0:
            for r in self.rock.points:
                self.board[r] = "#"
            self.spawn = max(self.spawn, self.rock.top + SPAWN_GAP)
            self.rock = None
        else:
            self.rock += DOWN

    def round(self):

        self.init_rock()
        while self.rock is not None:
            self.move()
            self.down()

    def play(self, rock_count: int) -> int:
        rocks = rock_count
        cache = {}
        additional = 0
        while rocks:
            self.round()
            rocks -= 1

            key = (
                self.rock_idx % len(self.shapes),
                self.jet_idx % len(self.jets),
                "".join([self.board.get(complex(i, self.height), " ") for i in range(7)]),
            )

            if key in cache and rocks > 5022:
                cached_height, cached_rocks = cache[key]
                additional += (self.height - cached_height) * (rocks // (cached_rocks - rocks))
                rocks %= cached_rocks - rocks
            cache[key] = (self.height + additional, rocks)

        return self.height + additional


def part_1(input_string: str) -> int:
    jets = [LEFT if d == "<" else RIGHT for d in input_string]
    game = Game(jets, SHAPES)
    return game.play(2022)


def part_2(input_string: str) -> int:
    jets = [LEFT if d == "<" else RIGHT for d in input_string]
    game = Game(jets, SHAPES)

    return game.play(1000000000000)


# -- Tests


def get_example_input() -> str:
    return ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 3068


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 1514285714288


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 3083


# @no_input_skip
# def test_part_2_real():
#    real_input = read_input(__file__)
#
#    ans = part_2(real_input)
#    print(ans)
#    print(1532183908048)
#    print(1532183908048 - ans)
#    assert ans == 1532183908048


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

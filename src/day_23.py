# Standard Library
from collections import defaultdict, deque
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import DefaultDict, Deque, Literal, Self

# First Party
from utils import no_input_skip, read_input  # noqa

DIRECTIONS = (
    Literal["N"] | Literal["S"] | Literal["E"] | Literal["W"] | Literal["NE"] | Literal["NW"] | Literal["SE"] | Literal["SW"]
)


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, delta: Self) -> Self:
        return Vec(self.x + delta.x, self.y + delta.y)

    def __str__(self) -> str:
        return f"x:{self.x}, y:{self.y}"


dirs: dict[DIRECTIONS, Vec] = {
    "N": Vec(0, -1),
    "S": Vec(0, 1),
    "E": Vec(1, 0),
    "W": Vec(-1, 0),
}

dirs["NE"] = dirs["N"] + dirs["E"]
dirs["NW"] = dirs["N"] + dirs["W"]
dirs["SE"] = dirs["S"] + dirs["E"]
dirs["SW"] = dirs["S"] + dirs["W"]


def get_moves() -> Deque[Callable[[Vec, "Board"], Vec | None]]:
    return deque(
        [
            lambda pos, board: pos + dirs["N"]
            if all(board[pos + d] is None for d in [dirs["NW"], dirs["N"], dirs["NE"]])
            else None,
            lambda pos, board: pos + dirs["S"]
            if all(board[pos + d] is None for d in [dirs["SW"], dirs["S"], dirs["SE"]])
            else None,
            lambda pos, board: pos + dirs["W"]
            if all(board[pos + d] is None for d in [dirs["W"], dirs["NW"], dirs["SW"]])
            else None,
            lambda pos, board: pos + dirs["E"]
            if all(board[pos + d] is None for d in [dirs["NE"], dirs["E"], dirs["SE"]])
            else None,
        ]
    )


@dataclass()
class Elf:
    pos: Vec
    moves: Deque[Callable[[Vec, "Board"], Vec | None]]

    def __str__(self) -> str:
        return f"Elf at {self.pos}"


class Board(DefaultDict):
    @property
    def min_x(self) -> int:
        return min(vec.x for vec, c in self.items() if c is not None)

    @property
    def min_y(self) -> int:
        return min(vec.y for vec, c in self.items() if c is not None)

    @property
    def max_x(self) -> int:
        return max(vec.x for vec, c in self.items() if c is not None)

    @property
    def max_y(self) -> int:
        return max(vec.y for vec, c in self.items() if c is not None)

    @property
    def area(self) -> int:
        return (self.max_x - self.min_x) * (self.max_y - self.min_y)

    def x_range(self, padding: int = 0) -> Iterator[int]:
        yield from range(self.min_x - padding, self.max_x + 1 + padding)

    def y_range(self, padding: int = 0) -> Iterator[int]:
        yield from range(self.min_y - padding, self.max_y + 1 + padding)


def get_board(elfs: list[Elf]) -> Board[Vec, Elf | None]:
    board: DefaultDict[Vec, Elf | None] = Board(lambda: None)

    for elf in elfs:
        board[elf.pos] = elf

    return board


def draw(elfs: list[Elf], padding: int = 0, extra: str = "") -> str:
    board = get_board(elfs)
    print(f"=== {extra}")
    to_print = ""
    for y in board.y_range(padding):
        for x in board.x_range(padding):
            to_print += "#" if board[Vec(x, y)] else "."
        to_print += "\n"
    print(to_print)
    print("===")

    return to_print


def parse(input: str) -> Iterator[Elf]:
    for y, line in enumerate(input.split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                yield Elf(Vec(x, y), get_moves())


def move_elfs(elfs: list[Elf]) -> list[Elf]:
    board = get_board(elfs)
    next_elfs: list[tuple[Vec, Elf]] = []
    moves: DefaultDict[Vec, int] = defaultdict(lambda: 0)
    for elf in elfs:
        new_move = None
        for move in elf.moves:
            if new_move is None:
                new_move = move(elf.pos, board)

        elf.moves.rotate(1)
        if new_move is not None:
            moves[new_move] += 1
            next_elfs.append((new_move, elf))

    for new_move, elf in next_elfs:
        if moves[new_move] == 1:
            elf.pos = new_move

    return elfs


def part_1(input: str) -> int:
    elfs: list[Elf] = list(parse(input))

    draw(elfs)

    for i in range(10):
        elfs = move_elfs(elfs)
        draw(elfs, extra=str(i + 1))

    return get_board(elfs).area - len(elfs)


def part_2(input: str) -> int:
    pass


# -- Tests


def get_example_input() -> str:
    return """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 110


def test_parse_and_draw():
    start = """....
.##.
.#..
....
.##.
...."""

    elfs = parse(start)
    drawn = draw(list(elfs), 1)
    for left, right in zip(drawn.split("\n"), start.split("\n")):
        assert left == right


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

    real_input = """.....
..##.
..#..
.....
..##.
....."""

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

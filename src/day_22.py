# Standard Library
import re
from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from functools import partial
from typing import Literal, Self

# First Party
from utils import no_input_skip, read_input

# Third Party
from icecream import ic


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, delta: Self) -> Self:
        return Vec(self.x + delta.x, self.y + delta.y)


Move = Literal["R"] | Literal["L"]


@dataclass(frozen=True)
class Tile:
    c: Literal["."] | Literal["#"] | Literal[">"] | Literal["v"] | Literal["<"] | Literal["^"]
    vec: Vec

    def __eq__(self, __o: Self) -> bool:
        match __o:
            case str():
                return self.c == __o
            case _:
                return self.c == __o.c

    def __str__(self) -> str:
        return self.c

    @property
    def x(self) -> int:
        return self.vec.x

    @property
    def y(self) -> int:
        return self.vec.y


@dataclass(frozen=True)
class directions:
    up = Vec(0, -1)
    right = Vec(1, 0)
    down = Vec(0, 1)
    left = Vec(-1, 0)

    def __iter__(self):
        yield self.right
        yield self.down
        yield self.left
        yield self.up

    @classmethod
    def score(cls, dir: Vec) -> int:
        match dir:
            case cls.right:
                return 0
            case cls.down:
                return 1
            case cls.left:
                return 3
            case cls.up:
                return 3

    @classmethod
    def arrows(cls, dir: Vec, pos: Vec) -> Tile:
        match dir:
            case cls.right:
                return Tile(">", pos)
            case cls.down:
                return Tile("v", pos)
            case cls.up:
                return Tile("^", pos)
            case cls.left:
                return Tile("<", pos)
            case _:
                raise Exception("Unknown directions")


def draw(board, max_x, max_y):
    for y in range(max_y):
        for x in range(max_x):
            try:
                print(board[Vec(x, y)], end="")
            except KeyError:
                print(" ", end="")
        print()
    print()


def get_moves(unparsed_moves: str) -> Iterable[Move | int]:
    for move, turn in re.findall(r"(\d+)([RL]?)", unparsed_moves):
        yield int(move)
        if turn != "":
            yield turn


def parse_board(unparsed_board: str) -> tuple[dict[Vec, Tile], Vec, int, int]:
    position: Vec | None = None
    board: dict[Vec, Tile] = {}

    max_y: int = 0
    max_x: int = 0

    for y, line in enumerate(unparsed_board.split("\n")):
        max_y = max(max_y, y)
        for x, i in enumerate(line):
            max_x = max(max_x, x)
            if i == "." or i == "#":
                board[Vec(x, y)] = Tile(i, Vec(x, y))

            if i == "." and position is None:
                position = Vec(x, y)

    if position is None:
        raise ValueError("No position found")

    return board, position, max_x + 1, max_y + 1


def part_1(input: str) -> int:
    unparsed_board, unparsed_moves = input.split("\n\n")

    moves = get_moves(unparsed_moves)
    board, position, max_x, max_y = parse_board(unparsed_board)

    facing = deque(directions())

    for move in moves:
        match move:
            case "L":
                facing.rotate(1)
            case "R":
                facing.rotate(-1)
            case int():
                for _ in range(move):
                    next_position = position + facing[0]
                    if next_position not in board:
                        if facing[0] == directions.up:
                            next_position = Vec(next_position.x, max_y)
                        if facing[0] == directions.down:
                            next_position = Vec(next_position.x, 0)
                        if facing[0] == directions.left:
                            next_position = Vec(max_x, next_position.y)
                        if facing[0] == directions.right:
                            next_position = Vec(0, next_position.y)
                        while next_position not in board:
                            next_position = next_position + facing[0]

                    if board[next_position] == "#":
                        break
                    board[position] = directions.arrows(facing[0], board[position].vec)
                    position = next_position
            case _:
                raise ValueError(f"Unrecognised move: {move}")

    final_tile = board[position]

    return (1000 * (final_tile.y + 1)) + (4 * (final_tile.x + 1)) + directions.score(facing[0])


def part_2(input: str) -> int:
    unparsed_board, unparsed_moves = input.split("\n\n")

    moves = get_moves(unparsed_moves)
    board, position, max_x, max_y = parse_board(unparsed_board)
    _draw = partial(draw, board=board, max_x=max_x, max_y=max_y)

    ic(max_x, max_y)
    tile_size = max(max_x, max_y) // 4
    ic(tile_size)

    for y in range(max_y):
        for x in range(max_x):
            p = Vec(x, y)
            if p not in board:
                board[p] = Tile(str((x // tile_size) + (y // tile_size)))

    _draw()

    return 0

    facing = deque([D_RIGHT, D_DOWN, D_LEFT, D_UP])

    for move in moves:
        match move:
            case "L":
                facing.rotate(1)
            case "R":
                facing.rotate(-1)
            case int():
                for _ in range(move):
                    next_position = position + facing[0]
                    if next_position not in board:
                        if facing[0] == D_UP:
                            next_position = Vec(next_position.x, max_y)
                        if facing[0] == D_DOWN:
                            next_position = Vec(next_position.x, 0)
                        if facing[0] == D_LEFT:
                            next_position = Vec(max_x, next_position.y)
                        if facing[0] == D_RIGHT:
                            next_position = Vec(0, next_position.y)
                        while next_position not in board:
                            next_position = next_position + facing[0]

                    if board[next_position] == "#":
                        break
                    board[position] = ARROWS[facing[0]]
                    position = next_position
            case _:
                raise ValueError(f"Unrecognised move: {move}")

    return (1000 * (position.y + 1)) + (4 * (position.x + 1)) + SCORES[facing[0]]


# -- Tests


def get_example_input() -> str:
    return """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 6032


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 5031


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 27436


# @no_input_skip
# def test_part_2_real():
#     real_input = read_input(__file__)
#     assert part_2(real_input) is not None


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)
    real_input = get_example_input()
    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

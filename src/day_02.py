# Standard Library

# First Party
from utils import no_input_skip, read_input

ROCK = 1
PAPAER = 2
SCISSORS = 3

LOOSE = 1
DRAW = 2
WIN = 3

moves: dict[str, int] = {
    "A": ROCK,
    "B": PAPAER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPAER,
    "Z": SCISSORS,
}


scores: dict[tuple[int, int], int] = {
    (ROCK, PAPAER): 6,
    (PAPAER, SCISSORS): 6,
    (SCISSORS, ROCK): 6,
    (ROCK, ROCK): 3,
    (PAPAER, PAPAER): 3,
    (SCISSORS, SCISSORS): 3,
    (PAPAER, ROCK): 0,
    (SCISSORS, PAPAER): 0,
    (ROCK, SCISSORS): 0,
}


def part_1(input: str) -> int:
    score = 0
    for game in input.split("\n"):
        them, you = game.split(" ")
        score += scores[(moves[them], moves[you])] + moves[you]

    return score


def fix_game(them: int, you: int) -> int:
    losses = dict(zip([ROCK, PAPAER, SCISSORS], [SCISSORS, ROCK, PAPAER]))

    actions = {
        LOOSE: losses,
        WIN: {v: k + 6 for k, v in losses.items()},
        DRAW: dict(zip([ROCK, PAPAER, SCISSORS], map(lambda m: m + 3, [ROCK, PAPAER, SCISSORS]))),
    }

    return actions[you][them]


def part_2(input: str) -> int:
    score = 0
    for game in input.split("\n"):
        them, you = game.split(" ")
        score += fix_game(moves[them], moves[you])

    return score


# -- Tests


def get_example_input() -> str:
    return """A Y
B X
C Z"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 15


def test_part_2():
    test_input = get_example_input()
    assert part_2(test_input) == 12


@no_input_skip
def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 13526


@no_input_skip
def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 14204


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

# Standard Library
from collections import defaultdict

# First Party
from utils import read_input

ROCK = 1
PAPAER = 2
SCISSORS = 3

LOOSE = 1
DRAW = 2
WIN = 3

thems = {
    "A": ROCK,
    "B": PAPAER,
    "C": SCISSORS,
}

yous = {
    "X": ROCK,
    "Y": PAPAER,
    "Z": SCISSORS,
}


def get_scores() -> dict[tuple[int, int], int]:
    scores = defaultdict(lambda: 0)
    scores[(ROCK, PAPAER)] = 6
    scores[(PAPAER, SCISSORS)] = 6
    scores[(SCISSORS, ROCK)] = 6
    for i in [ROCK, PAPAER, SCISSORS]:
        scores[(i, i)] = 3

    return scores


def part_1(input: str) -> int:
    scores = get_scores()
    score = 0
    for game in input.split("\n"):
        them, you = game.split(" ")
        score += scores[(thems[them], yous[you])] + yous[you]

    return score


def fix_game(them: int, you: int) -> int:
    losses = {
        ROCK: SCISSORS,
        PAPAER: ROCK,
        SCISSORS: PAPAER,
    }
    wins = {v: k for k, v in losses.items()}

    if you == LOOSE:
        print(f"loose {them} {you} : 0 + {losses[them]}")
        return 0 + losses[them]

    if you == WIN:
        print(f"win {them} {you} : 6 + {wins[them]}")
        return 6 + wins[them]

    print(f"draw {them} {you} : 3 + {them}")
    return 3 + them


def part_2(input: str) -> int:
    score = 0
    for game in input.split("\n"):
        them, you = game.split(" ")

        score += fix_game(int(thems[them]), int(yous[you]))

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


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 13526


def test_part_2_real():
    real_input = read_input(__file__)
    assert part_2(real_input) == 14204


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

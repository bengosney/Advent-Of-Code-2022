# Standard Library
from collections import defaultdict

# First Party
from utils import read_input

SCREEN_WIDTH = 40


def processor(input: str):
    register = 1
    cycle = 0

    for line in input.split("\n"):
        cycle += 1
        yield cycle, register
        match line.split(" "):
            case "noop", *_:
                pass
            case "addx", value:
                cycle += 1
                yield cycle, register
                register += int(value)
            case _:
                raise Exception(f"Invalid command: {line}")


def part_1(input: str) -> int:
    strength = 0
    check_cycle = 20
    for i, signal_strength in processor(input):
        if i == check_cycle:
            strength += signal_strength * i
            check_cycle += 40

        if i == 220:
            return strength

    raise Exception("Not enough input")


def part_2(input: str, lit: str = "#", unlit: str = " ") -> str:
    display: dict[int, str] = defaultdict(lambda: "")

    for cycle, signal in processor(input):
        sprite = list(range(signal, signal + 3))
        state = lit if cycle % SCREEN_WIDTH in sprite else unlit
        display[(cycle - 1) // SCREEN_WIDTH] += state

    return "\n" + "\n".join(display.values())


# -- Tests


def get_example_input() -> str:
    return """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def test_part_1():
    test_input = get_example_input()
    assert part_1(test_input) == 13140


def test_part_2():
    test_input = get_example_input()

    assert (
        part_2(test_input, unlit=".")
        == """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......###.
#######.......#######.......#######....."""
    )


def test_part_1_real():
    real_input = read_input(__file__)
    assert part_1(real_input) == 13440


def test_part_2_real():
    real_input = read_input(__file__)

    assert (
        part_2(real_input, unlit=".")
        == """
###..###..####..##..###...##..####..##..
#..#.#..#....#.#..#.#..#.#..#....#.#..#.
#..#.###....#..#....#..#.#..#...#..#..#.
###..#..#..#...#.##.###..####..#...####.
#....#..#.#....#..#.#.#..#..#.#....#..#.
#....###..####..###.#..#.#..#.####.#..#."""
    )


# -- Main

if __name__ == "__main__":
    real_input = read_input(__file__)

    print(f"Part1: {part_1(real_input)}")
    print(f"Part2: {part_2(real_input)}")

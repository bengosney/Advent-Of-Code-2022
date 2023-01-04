# Standard Library
import contextlib
from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from statistics import mean
from time import time

# First Party
from utils import read_input

# Third Party
import typer
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

app = typer.Typer()


def time_it(day: str, iterations: int = 1, progress: Callable = lambda: None) -> tuple[float, float]:
    module = import_module(day)
    input_str = read_input(day)

    times: dict[int, list[float]] = {}

    for i in [1, 2]:
        times[i] = []
        for _ in range(iterations):
            start = time()
            with contextlib.suppress(Exception):
                getattr(module, f"part_{i}")(input_str)
            times[i].append(time() - start)
            progress()

    return mean(times[1]), mean(times[2])


@app.command()
def benchmark(iterations: int = 10, days: list[str] = []) -> None:
    table = Table(title=f"AOC 2022 - Timings\n({iterations:,} iterations)")

    table.add_column("Day", justify="center", style="bold")
    table.add_column("Part 1", justify="right")
    table.add_column("Part 2", justify="right")

    if not days:
        days = [p.name.replace(".py", "") for p in list(Path("./src").glob("day_*.py"))]

    with Progress(transient=True) as progress:
        task = progress.add_task("Running code", total=(len(days) * 2) * iterations)
        for day in sorted(days):
            p1, p2 = time_it(day, iterations, lambda: progress.update(task, advance=1))

            _, d = day.split("_")
            table.add_row(f"{int(d)}", f"{p1:.4f}s", f"{p2:.4f}s")

    with Console() as console:
        console.print(table)


def run_day(day: str, progress: Callable = lambda: None) -> tuple[float, float]:
    module = import_module(day)
    input_str = read_input(day)

    part_1 = 0
    part_2 = 0
    with contextlib.suppress(Exception):
        part_1 = getattr(module, "part_1")(input_str)
        progress()

        part_2 = getattr(module, "part_2")(input_str)
        progress()

    return part_1, part_2


def day_from_name(file_name: str) -> int:
    return int(file_name.replace(".py", "").replace("day_", ""))


@app.command()
def answers(days: list[int] = []) -> None:
    table = Table(title="Advent of Code 2022 - Answers")

    table.add_column("Day", justify="center", style="bold")
    table.add_column("Part 1", justify="left")
    table.add_column("Part 2", justify="left")

    if not days:
        days = [day_from_name(p.name) for p in list(Path("./src").glob("day_*.py"))]

    with Progress(transient=True) as progress:
        task = progress.add_task("Running code", total=(len(days) * 2))
        for d in sorted(days):
            p1, p2 = run_day(f"day_{d:02}", lambda: progress.update(task, advance=1))

            table.add_row(f"{int(d)}", f"{p1}", f"{p2}")

    with Console() as console:
        console.print(table)


if __name__ == "__main__":
    app()

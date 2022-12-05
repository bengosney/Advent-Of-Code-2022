# Standard Library
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


def timeit(day: str, iterations: int = 1, progress: Callable = lambda: None) -> tuple[float, float]:
    module = import_module(day)
    input = read_input(day)

    times: dict[int, list[float]] = {}

    for i in [1, 2]:
        times[i] = []
        for _ in range(iterations):
            start = time()
            getattr(module, f"part_{i}")(input)
            times[i].append(time() - start)
            progress()

    return mean(times[1]), mean(times[2])


def time_everything(iterations: int = 10, days: list[str] = []) -> None:
    table = Table(title=f"AOC 2021 - Timings\n({iterations:,} iterations)")

    table.add_column("Day", justify="center", style="bold")
    table.add_column("Part 1", justify="right")
    table.add_column("Part 2", justify="right")

    if not days:
        days = [p.name.replace(".py", "") for p in list(Path("./src").glob("day_*.py"))]

    with Progress(transient=True) as progress:
        task = progress.add_task("Running code", total=(len(days) * 2) * iterations)
        for day in sorted(days):
            p1, p2 = timeit(day, iterations, lambda: progress.update(task, advance=1))

            _, d = day.split("_")
            table.add_row(f"{int(d)}", f"{p1:.4f}s", f"{p2:.4f}s")

    with Console() as console:
        console.print(table)


if __name__ == "__main__":
    typer.run(time_everything)

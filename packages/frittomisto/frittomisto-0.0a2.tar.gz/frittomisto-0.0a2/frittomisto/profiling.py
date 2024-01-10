"""
Perf measuring utilities
"""
import time
import os
import fcntl
from typing import Dict, Optional, List, Union
from itertools import chain


class _PP:
    def __init__(self, name: str):
        """
        name: name of the profiler
        """
        self.name: str = name
        self.tot_time: float = 0
        self.rounds: int = 0
        self.started: Optional[float] = None
        self.max_time = 0

    def start(self, allow_restart: bool = False) -> None:
        """
        Starts the perf counter
        """
        if not allow_restart and self.started is not None:
            raise RuntimeError("Already started")
        self.started = time.perf_counter()

    def stop(self, stop_time: float) -> None:
        """
        Stops the perf counter, trowhs an error if it was not started.
        Note: `stop_time` is the time returned by `time.perf_counter()`,
        this value is passed as parameter to avoid overhead.
        """
        if self.started is None:
            raise RuntimeError("Not started")
        runtime = stop_time - self.started
        self.max_time = max(self.max_time, runtime)
        self.tot_time += runtime
        self.rounds += 1
        self.started = None

    def stop_if_started(self, stop_time: float) -> None:
        """
        Stops the perf counter if it was started
        """
        if self.started is None:
            return
        self.stop(stop_time)


__pp__: Dict[str, _PP] = {}


def pp_start(name: str, allow_restart: bool = False):
    """
    Start a perf counter named `name`.
    If allow_restart is True, the perf counter can be started multiple times,
    in which case only the last start time is considered.
    """
    if name not in __pp__:
        __pp__[name] = _PP(name)
    # Start the perf counter as last as possible to avoid overhead
    __pp__[name].start(allow_restart)


def pp_stop(name: str, allow_restop: bool = False):
    """
    Stop a perf counter named `name`.
    If allow_restop is True, the perf counter can be stopped multiple times,
    in which case only the first stop time is considered.
    """
    # Stop the perf counter as soon as possible to avoid overhead
    stop_time = time.perf_counter()
    if name not in __pp__:
        __pp__[name] = _PP(name)
    if not allow_restop:
        __pp__[name].stop(stop_time)
    else:
        __pp__[name].stop_if_started(stop_time)

def pp_get(name: str) -> _PP:
    """
    Return the perf counter named `name`
    """
    return __pp__[name]

def pp_reset(name: Optional[str] = None) -> None:
    """
    Reset the perf counter named `name`.
    If `name` is None, reset all perf counters.
    """
    if name is None:
        __pp__.clear()
    else:
        del __pp__[name]

def pp_stats():
    """ 
    Pretty print perf counters stats
    """

    def _truncate(string: str, max_length: int):
        """
        Truncate a string to `max_length` characters,
        adding "..." if the string is longer than `max_length`
        """
        if len(string) > max_length:
            return string[: max_length - 3] + "..."
        return string

    def _print_row(row: Union[List[str], List[Union[str, int, float]]], column_widths: List[int]):
        """
        Print a row of the table
        """
        formatted_row = [_truncate(str(item), w).ljust(w) for item, w in zip(row, column_widths)]
        print(" | ".join(formatted_row))

    # Determine the maximum width of each column
    headers: List[str] = ["PID", "Name", "tot_time", "rounds", "avg_time", "max_time"]
    rows: List[List[Union[str, int, float]]] = [
        [os.getpid(), pp.name, pp.tot_time, pp.rounds, pp.tot_time / pp.rounds, pp.max_time]
        for pp in sorted(__pp__.values(), key=lambda pp: pp.tot_time, reverse=True)
    ]

    # Ensure that all rows have the same number of columns
    assert all(len(headers) == len(r) for r in rows)

    # Determine the maximum width of each column
    max_col_width = 25
    column_widths = [
        min(max_col_width, max(len(str(r[i])) for r in chain([headers], rows)))
        for i in range(len(headers))
    ]

    # Print the table
    with open(os.path.expanduser("~/.frittomisto_lock"), "w", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            _print_row(headers, column_widths)
            for pp in sorted(__pp__.values(), key=lambda pp: pp.tot_time, reverse=True):
                _print_row(
                    [
                        os.getpid(),
                        pp.name,
                        pp.tot_time,
                        pp.rounds,
                        pp.tot_time / pp.rounds,
                        pp.max_time,
                    ],
                    column_widths,
                )
            print()
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

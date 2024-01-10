"""
Time management utilities.
"""
import signal
from contextlib import contextmanager
from typing import Generator, Any


@contextmanager
def timeout(seconds: int, msg: str = "") -> Generator[None, None, None]:
    """
    Context manager to set a timeout
    """
    def _raise_timeout(signum: int, frame: Any) -> None:
        """
        Raise a timeout exception
        """
        raise TimeoutError(msg)

    signal.signal(signal.SIGALRM, _raise_timeout)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

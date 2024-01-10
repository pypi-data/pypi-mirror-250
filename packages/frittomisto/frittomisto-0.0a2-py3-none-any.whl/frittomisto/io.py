"""
Module for managing outputs
"""
from unittest.mock import patch
from contextlib import contextmanager

@contextmanager
def no_print():
    """
    Context manager to disable printing, use it like this:
    with no_print():
        print("This will not be printed")
        func() # This will not print anything either
    """
    with patch("builtins.print") as mock_print:
        mock_print.side_effect = lambda : None
        yield

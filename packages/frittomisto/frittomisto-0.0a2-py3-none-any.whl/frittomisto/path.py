"""
Module to manage paths
"""
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Union

@contextmanager
def cd(path: Union[str, Path]):
    """
    Context manager to change the current working directory
    """
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

def sanitize_path(path: str, allowed_dir: str) -> str:
    """
    Sanitizes a path, ensuring it's within the allowed directory
    """
    # Remove any trailing slashes
    path = os.path.normpath(path)

    # Replace backslashes with forward slashes
    path = path.replace("\\", "/")

    # Remove any relative path components
    path = os.path.abspath(path)

    # Check if the path is within the allowed directory
    allowed_dir = os.path.abspath(allowed_dir)
    if os.path.commonprefix([path, allowed_dir]) != allowed_dir:
        raise ValueError(f"Path {path} is not within allowed directory {allowed_dir}")

    return path

"""
Utilities for async functions
"""
import asyncio
from typing import Callable, Any, Coroutine, List, Dict
from functools import wraps


def make_sync(func: Callable[...,Coroutine[Any, Any, Any]]) -> Callable[...,Any]:
    """
    Decorator to run async functions synchronously
    Usage:

    @make_sync
    async def foo():
        pass

    """

    @wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[Any, Any]) -> Any:
        return asyncio.run(func(*args, **kwargs))

    return wrapper

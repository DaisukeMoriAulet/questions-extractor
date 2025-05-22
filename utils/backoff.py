"""
Utility for exponential backoff with optional jitter.

This module provides a decorator or function to implement exponential backoff
retry logic for function calls that might fail temporarily.
"""

import functools
import random
import time
from typing import Any, Callable, Optional, Tuple, Type, TypeVar, Union, cast

# Type variables for function signatures
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])


def exponential_backoff(
    target_function: Optional[F] = None,
    *,
    max_retries: int = 3,
    base_delay_seconds: float = 1.0,
    max_delay_seconds: float = 60.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Union[F, Callable[[F], F]]:
    """
    Retries a function call with exponential backoff upon failure.

    This can be used as a decorator or as a regular function to wrap a callable.
    The function will be called up to `max_retries + 1` times (initial attempt plus retries).
    If it succeeds, the result is returned. If it fails with a retryable exception,
    it waits with exponential backoff before retrying.

    Args:
        target_function: The function to call and retry. If None, returns a decorator.
        max_retries: Maximum number of retry attempts (default: 3).
        base_delay_seconds: Initial delay in seconds (default: 1.0).
        max_delay_seconds: Maximum possible delay in seconds (default: 60.0).
        jitter: If True, adds random jitter to the delay (default: True).
        retryable_exceptions: Tuple of Exception types that trigger a retry (default: (Exception,)).

    Returns:
        If target_function is provided, returns the wrapped function.
        Otherwise, returns a decorator that wraps a function with retry logic.

    Raises:
        The last caught exception if all retries are exhausted.
        Any non-retryable exception immediately.

    Example:
        # As a decorator
        @exponential_backoff(max_retries=3, jitter=True)
        def api_call():
            # Function that might fail temporarily

        # As a function
        result = exponential_backoff(api_call, max_retries=3, jitter=True)()
    """
    # When called without a function, return a decorator
    if target_function is None:
        return lambda f: exponential_backoff(
            f,
            max_retries=max_retries,
            base_delay_seconds=base_delay_seconds,
            max_delay_seconds=max_delay_seconds,
            jitter=jitter,
            retryable_exceptions=retryable_exceptions
        )

    @functools.wraps(target_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper function that implements retry logic."""
        last_exception = None

        for attempt in range(max_retries + 1):  # +1 for the initial attempt
            try:
                return target_function(*args, **kwargs)
            except retryable_exceptions as e:
                last_exception = e
                
                # If this was the last attempt, re-raise the exception
                if attempt >= max_retries:
                    raise last_exception

                # Calculate delay using exponential backoff
                current_delay = min(max_delay_seconds, base_delay_seconds * (2 ** attempt))
                
                # Add jitter if enabled
                if jitter:
                    current_delay += random.uniform(0, current_delay * 0.25)
                
                # Wait before retrying
                time.sleep(current_delay)
            except Exception as e:
                # Immediately re-raise non-retryable exceptions
                raise e

        # This should never be reached as we either return or raise an exception
        # But keeping it to satisfy type checking
        if last_exception:
            raise last_exception
        
        return None  # To satisfy type checker

    return cast(F, wrapper)
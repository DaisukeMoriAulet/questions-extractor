# Overview

## Parent Epic

- To be linked with Epic for Phase 5: Reliability & Logging (see `docs/roadmap.md`)

## Background / Why

- Quote the relevant line from `docs/mvp_breakdown.md` (line 26 under "2. Common Utilities"):
  > - [ ] **backoff.py** ― `exponential_backoff(jitter=True, retries=3)`

## What to do / How

1.  Create a new Python file: `utils/backoff.py`.
2.  Implement a function or decorator named `exponential_backoff`.
3.  The function should be designed to wrap a callable (e.g., an API call) and retry it upon failure.
4.  Parameters for the `exponential_backoff` utility:
    *   `target_function`: The function to call and retry.
    *   `max_retries`: `int` (default: 3, as per task description) - Maximum number of retry attempts.
    *   `base_delay_seconds`: `float` (default: 1.0) - The initial delay in seconds.
    *   `max_delay_seconds`: `float` (default: 60.0) - The maximum possible delay in seconds.
    *   `jitter`: `bool` (default: True, as per task description) - If True, add random jitter to the delay.
    *   `retryable_exceptions`: `tuple` of Exception types (default: `(Exception,)`) - Exceptions that trigger a retry.
5.  Logic:
    *   Loop for `max_retries` attempts (i.e., up to `max_retries + 1` total calls).
    *   In each attempt, call `target_function` with its arguments.
    *   If `target_function` succeeds, return its result.
    *   If `target_function` raises an exception that is an instance of any type in `retryable_exceptions`:
        *   If it's the last attempt (i.e., `attempt_number == max_retries`), re-raise the caught exception.
        *   Calculate delay: `current_delay = min(max_delay_seconds, base_delay_seconds * (2 ** attempt_number))`.
        *   If `jitter` is True, add randomness (e.g., `current_delay += random.uniform(0, current_delay * 0.25)`).
        *   Wait for `current_delay` seconds (e.g., using `time.sleep()`).
    *   If `target_function` raises an exception NOT in `retryable_exceptions`, re-raise it immediately without retrying.
6.  Ensure the implementation is robust, well-documented with type hints, and includes clear docstrings. This utility is critical for reliable interactions with external services like the Gemini API (see PRD 3.1 OCR Retry).

## Acceptance Criteria / AC

- [ ] `exponential_backoff` function/decorator is implemented in `utils/backoff.py`.
- [ ] The function correctly calculates exponential backoff times.
- [ ] Jitter can be enabled/disabled and works as expected.
- [ ] The number of retries is configurable.
- [ ] Specific exceptions can be configured as retryable.
- [ ] Unit tests for `backoff.py` cover:
    - [ ] Successful execution on the first attempt.
    - [ ] Successful execution after one or more retries.
    - [ ] Failure after exhausting all retries (the last exception is raised).
    - [ ] Correct delay calculation with and without jitter.
    - [ ] Non-retryable exceptions are immediately raised.
    - [ ] Behavior with `max_retries=0` (should attempt once).
- [ ] Docstrings clearly explain usage, parameters, return values, and exceptions raised.

## Predefined Checklist

- [ ] Docstring & comments
- [ ] Test cases added

## Related Materials

- PRD: `docs/prd.md` (See section 3.1 OCR: Retry - "Exponential backoff 3 times (2^n coefficient + Jitter recommended)")
- Roadmap: `docs/roadmap.md` (See Phase 5: Reliability & Logging - "Implement Exponential Backoff + Jitter in the common library")
- Break-down Task: `docs/mvp_breakdown.md` (Line 26 in "2. Common Utilities" section)

"""Brute-force lockout for the two password-bearing endpoints (F36).

`time.sleep(1)` on a failed login slows one connection down; it does
nothing against many connections guessing in parallel, which is exactly
what an internet-exposed login page gets. This module counts recent
failures per key (the client IP) and refuses further attempts for a
while once a limit is hit — the guesser gets an immediate 429, no thread
held, no hash computed.

Pure data structure, no Flask and no clock of its own: every method
takes `now` explicitly, so tests never sleep. State is in-memory and
per-process, which is the right size for this app: waitress runs one
process, and a restart forgiving all counters costs an attacker nothing
compared to the window doing the same a few minutes later.
"""

from collections import deque

DEFAULT_LIMIT = 10
DEFAULT_WINDOW_SECONDS = 15 * 60


class FailureThrottle:
    """Sliding-window failure counter: after `limit` failures within
    `window_seconds`, the key is blocked until the oldest of those
    failures ages out of the window."""

    def __init__(self, limit: int = DEFAULT_LIMIT, window_seconds: int = DEFAULT_WINDOW_SECONDS):
        self.limit = limit
        self.window_seconds = window_seconds
        self._failures: dict[str, deque] = {}

    def _prune(self, key: str, now: float) -> None:
        timestamps = self._failures.get(key)
        if timestamps is None:
            return
        cutoff = now - self.window_seconds
        while timestamps and timestamps[0] <= cutoff:
            timestamps.popleft()
        if not timestamps:
            del self._failures[key]

    def is_blocked(self, key: str, now: float) -> bool:
        self._prune(key, now)
        timestamps = self._failures.get(key)
        return timestamps is not None and len(timestamps) >= self.limit

    def retry_after(self, key: str, now: float) -> int:
        """Whole seconds until the key unblocks (for a Retry-After
        header); 0 if it isn't blocked."""
        if not self.is_blocked(key, now):
            return 0
        oldest = self._failures[key][0]
        remaining = oldest + self.window_seconds - now
        return max(1, int(remaining) + 1)

    def register_failure(self, key: str, now: float) -> None:
        self._prune(key, now)
        self._failures.setdefault(key, deque()).append(now)
        # A key already at the limit gains nothing from more entries, and
        # bounding the deque keeps an aggressive client from growing
        # memory: everything beyond the limit tells us nothing new.
        timestamps = self._failures[key]
        while len(timestamps) > self.limit:
            timestamps.popleft()

    def clear(self, key: str) -> None:
        """A successful login wipes the slate — the family member who
        fumbled their password a few times shouldn't stay one typo away
        from a lockout for the rest of the window."""
        self._failures.pop(key, None)

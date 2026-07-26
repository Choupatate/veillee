"""Tests for app/throttle.py (F36): the pure sliding-window failure
counter behind the login/invite-code brute-force lockout. No Flask and no
real clock — `now` is always passed in, so nothing here sleeps."""

from app.throttle import FailureThrottle


def test_fresh_key_is_not_blocked():
    t = FailureThrottle(limit=3, window_seconds=60)
    assert not t.is_blocked("1.2.3.4", now=1000.0)
    assert t.retry_after("1.2.3.4", now=1000.0) == 0


def test_blocks_at_the_limit_not_before():
    t = FailureThrottle(limit=3, window_seconds=60)
    t.register_failure("ip", now=1000.0)
    t.register_failure("ip", now=1001.0)
    assert not t.is_blocked("ip", now=1002.0)
    t.register_failure("ip", now=1002.0)
    assert t.is_blocked("ip", now=1003.0)


def test_unblocks_when_the_oldest_failure_ages_out():
    t = FailureThrottle(limit=3, window_seconds=60)
    for i in range(3):
        t.register_failure("ip", now=1000.0 + i)
    assert t.is_blocked("ip", now=1059.0)
    # The oldest failure was at t=1000; the window is 60s.
    assert not t.is_blocked("ip", now=1060.5)


def test_retry_after_counts_down_and_is_always_at_least_one():
    t = FailureThrottle(limit=2, window_seconds=60)
    t.register_failure("ip", now=1000.0)
    t.register_failure("ip", now=1000.0)
    assert t.retry_after("ip", now=1000.0) == 61  # ceil + 1s margin
    assert t.retry_after("ip", now=1059.5) == 1
    assert t.retry_after("ip", now=1061.0) == 0


def test_keys_are_independent():
    t = FailureThrottle(limit=2, window_seconds=60)
    t.register_failure("attacker", now=1000.0)
    t.register_failure("attacker", now=1000.0)
    assert t.is_blocked("attacker", now=1001.0)
    assert not t.is_blocked("family-member", now=1001.0)


def test_success_clears_the_slate():
    t = FailureThrottle(limit=3, window_seconds=60)
    t.register_failure("ip", now=1000.0)
    t.register_failure("ip", now=1001.0)
    t.clear("ip")
    t.register_failure("ip", now=1002.0)
    assert not t.is_blocked("ip", now=1003.0)


def test_old_failures_do_not_linger_in_memory():
    t = FailureThrottle(limit=3, window_seconds=60)
    for i in range(1000):
        t.register_failure(f"ip-{i}", now=1000.0)
    # Any lookup after the window prunes the touched key entirely.
    for i in range(1000):
        assert not t.is_blocked(f"ip-{i}", now=2000.0)
    assert len(t._failures) == 0


def test_failure_memory_is_bounded_per_key():
    """Routes never register failures for an already-blocked client (they
    return 429 before checking anything), but even if one slipped
    through, the per-key deque stays bounded at the limit."""
    t = FailureThrottle(limit=2, window_seconds=60)
    t.register_failure("ip", now=1000.0)
    t.register_failure("ip", now=1001.0)
    t.register_failure("ip", now=1002.0)
    assert len(t._failures["ip"]) == 2

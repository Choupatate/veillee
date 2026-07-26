"""Pure date-math helpers, no framework dependencies."""

from datetime import date
from typing import Optional, Tuple


def age_parts(birthdate: date, on_date: date) -> Optional[Tuple[str, int]]:
    """The arithmetic behind the F3 age phrase, without the words:
    ("day" | "month" | "year", amount), or None for a date before birth.

    Split out from `age_label` for F38 so i18n.py can put the same numbers
    into French wording without reimplementing the month/day rounding."""
    if on_date < birthdate:
        return None

    days = (on_date - birthdate).days
    years = on_date.year - birthdate.year
    months = on_date.month - birthdate.month
    if on_date.day < birthdate.day:
        months -= 1
    total_months = years * 12 + months

    if total_months < 1:
        return ("day", days)
    if total_months < 12:
        return ("month", total_months)
    return ("year", total_months // 12)


def age_label(birthdate: date, on_date: date) -> str:
    """Human age phrase for `on_date` relative to `birthdate` (FEATURES.md F3).

    English only — templates go through i18n.age_label, which localizes it.
    Kept because the MCP server and tests use the plain English phrasing."""
    parts = age_parts(birthdate, on_date)
    if parts is None:
        return "before you were born"
    unit, amount = parts
    plural = "" if amount == 1 else "s"
    return f"{amount} {unit}{plural} old"

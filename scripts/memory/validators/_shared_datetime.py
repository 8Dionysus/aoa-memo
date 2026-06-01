from __future__ import annotations

from datetime import datetime, timedelta
import re

from ._shared_schema_constants import FORMAT_CHECKER, RFC3339_DATETIME, RFC3339_UTC_LEAP_SECOND_DATES

def is_rfc3339_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def is_rfc3339_date(year: int, month: int, day: int) -> bool:
    month_lengths = [
        31,
        29 if is_rfc3339_leap_year(year) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    return 1 <= month <= 12 and 1 <= day <= month_lengths[month - 1]

def is_rfc3339_leap_second(
    match: re.Match[str], year: int, month: int, day: int, hour: int, minute: int
) -> bool:
    if match["zone"] in ("Z", "z"):
        return hour == 23 and minute == 59 and (year, month, day) in RFC3339_UTC_LEAP_SECOND_DATES
    if year == 0:
        return False
    offset_minutes = int(match["offset_hour"]) * 60 + int(match["offset_minute"])
    if match["offset_sign"] == "-":
        offset_minutes = -offset_minutes
    try:
        local_second = datetime(year, month, day, hour, minute, 59)
        utc_second = local_second - timedelta(minutes=offset_minutes)
    except (OverflowError, ValueError):
        return False
    return (
        utc_second.hour == 23
        and utc_second.minute == 59
        and (utc_second.year, utc_second.month, utc_second.day) in RFC3339_UTC_LEAP_SECOND_DATES
    )

@FORMAT_CHECKER.checks("date-time")
def is_rfc3339_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    match = RFC3339_DATETIME.fullmatch(value)
    if not match:
        return False
    year = int(match["year"])
    month = int(match["month"])
    day = int(match["day"])
    if not is_rfc3339_date(year, month, day):
        return False
    hour = int(match["hour"])
    minute = int(match["minute"])
    second = int(match["second"])
    if hour > 23 or minute > 59 or second > 60:
        return False
    if second == 60 and not is_rfc3339_leap_second(match, year, month, day, hour, minute):
        return False
    if match["offset_hour"] is not None:
        if int(match["offset_hour"]) > 23 or int(match["offset_minute"]) > 59:
            return False
    return True

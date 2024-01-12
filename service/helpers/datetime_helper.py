import logging
from datetime import date, datetime, time, timedelta, timezone

log = logging.getLogger(__name__)


def str_to_datetime(str_: str) -> datetime:
    """Parse an ISO-8601 datetime string into a `datetime`.

    Args:
        str_: ISO-8601 datetime string to parse

    Returns:
        datetime representing the string
    """
    return datetime_parser.isoparse(str_)


def datetime_to_str(datetime_: datetime) -> str:
    """Parse an ISO-8601 datetime datetime into a `string`.

    Args:
        datetime_: ISO-8601 datetime string to parse

    Returns:
        string with ISO-8601 format representing the datetime
    """
    return datetime_.isoformat()

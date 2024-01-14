"""
utils.py Contains util functions.
"""
from datetime import datetime
from typing import Optional


def format_date_string(
    date_string: str, format_string: str = "%Y-%m-%dT%H:%M:%S.%fZ"
) -> Optional[datetime]:
    """
    Format a date string.
    :param date_string: The date string.
    :param format_string: The format.
    :return:
    """

    if isinstance(date_string, datetime):
        return date_string

    if date_string is None:
        return None

    return datetime.strptime(date_string, format_string)

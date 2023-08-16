import datetime
import pytz
import re


def timestamp_to_datetime_with_timezone_str(timestamp: float = 0, timezone: str = '', timedelta: float = 0, format: str = 'isoformat') -> str:
    if timezone is None or timezone == '':
        hour, minute = divmod(timedelta, 1)
        minute = minute * 60
        current_timezone = datetime.timezone(datetime.timedelta(hours=int(hour), minutes=minute))
    else:
        current_timezone = pytz.timezone(timezone)

    if timestamp == 0:
        datetime_obj = datetime.datetime.now(current_timezone)
    else:
        datetime_obj = datetime.datetime.fromtimestamp(timestamp, current_timezone)

    if format == 'isoformat':
        return datetime_obj.isoformat()
    else:
        return datetime.datetime.strftime(datetime_obj, format)


def get_utc_datetime(timestamp: float) -> datetime.datetime:
    return datetime.datetime.utcfromtimestamp(timestamp)


def remove_floating_point(timestamp: float) -> float:
    return float(re.sub(r'.\d{6}', '', str(timestamp)))

                 
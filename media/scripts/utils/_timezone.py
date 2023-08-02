from datetime import datetime, timezone, timedelta


def timestamp_to_datetime_with_timezone(timestamp: float = 0, time_delta: int = 9) -> str:
    current_timezone = timezone(timedelta(hours=time_delta))

    if timestamp == 0:
        datetime_obj = datetime.now(current_timezone)
    else:
        datetime_obj = datetime.fromtimestamp(timestamp, current_timezone)

    return datetime_obj.isoformat()

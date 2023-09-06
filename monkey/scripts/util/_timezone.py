from datetime import datetime


def get_utc_datetime(timestamp: float, remove_float_point: bool=False) -> datetime:
    dt_obj = datetime.utcfromtimestamp(timestamp)
    if remove_float_point:
        dt_obj = dt_obj.replace(microsecond=0)
    return dt_obj


def get_time_str(timestamp: float=None) -> str:
    if timestamp:
        return get_utc_datetime(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
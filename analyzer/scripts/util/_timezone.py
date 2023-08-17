import datetime


def get_utc_datetime(timestamp: float, remove_float_point: bool=False) -> datetime.datetime:
    dt_obj = datetime.datetime.utcfromtimestamp(timestamp)
    if remove_float_point:
        dt_obj = dt_obj.replace(microsecond=0)
    return dt_obj

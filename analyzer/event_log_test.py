from datetime import datetime
from scripts.connection.external import get_data_of_event_log


def datetimestr_to_datetime_obj(datetimestr: str):
    return datetime.strptime(datetimestr, "%Y-%m-%dT%H:%M:%SZ")

d1_obj = datetimestr_to_datetime_obj('2023-08-17T07:10:31Z')
d2_obj = datetimestr_to_datetime_obj('2023-08-17T07:38:43Z')

res = get_data_of_event_log(d1_obj, d2_obj)
print(res)
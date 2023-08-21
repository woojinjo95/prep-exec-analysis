from datetime import datetime
import sys
from scripts.external.event import get_data_of_event_log


def datetimestr_to_datetime_obj(datetimestr: str):
    return datetime.strptime(datetimestr, "%Y-%m-%dT%H:%M:%SZ")


d1 = sys.argv[1]
d2 = sys.argv[2]

# d1 = '2023-08-17T07:10:31Z'
# d2 = '2023-08-17T07:38:43Z'

d1_obj = datetimestr_to_datetime_obj(d1)
d2_obj = datetimestr_to_datetime_obj(d2)

res = get_data_of_event_log(d1_obj, d2_obj)
print(res)

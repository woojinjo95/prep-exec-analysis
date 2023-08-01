
from datetime import datetime, timedelta

from scripts.log_service.log_manage.log_handle import load_page



start = datetime.now() - timedelta(minutes=60, seconds=0)
end = datetime.now() - timedelta(minutes=1, seconds=0)
# get all lines in page
page = 1
while True:
    logs = load_page(start.timestamp(), end.timestamp(), page, 1000)
    if len(logs) == 0:
        break
    print(f'start : {start}, \nend : {end}, \npage: {page}, \nstart_log : {logs[0] if len(logs) > 0 else ""}, \nend_log : {logs[-1] if len(logs) > 0 else ""}, \nlen : {len(logs)}')
    page += 1

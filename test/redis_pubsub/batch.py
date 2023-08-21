from start import main as start_main
from stop import main as stop_main
from remote import main as remote_main
from simple_logger import simple_logger


logger = simple_logger('test')

start_main()
remote_main()
stop_main()

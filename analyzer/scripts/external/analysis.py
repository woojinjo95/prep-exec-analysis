import time

from scripts.util._timezone import get_utc_datetime
from scripts.external.scenario import update_analysis_to_scenario


def set_analysis_info(command: str):
    current_time = get_utc_datetime(time.time())
    update_analysis_to_scenario({
        'type': command,
        'timestamp': current_time
    }, current_time)
    

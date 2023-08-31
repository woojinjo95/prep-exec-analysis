import logging
from scripts.monkey.monkey import Monkey
from scripts.log_service.log_organizer import LogOrganizer


log_organizer = LogOrganizer(name='monkey')
log_organizer.set_stream_logger('monkey_test')

logger = logging.getLogger('monkey_test')

monkey = Monkey(duration=180,
                key_candidates=['right', 'down'],
                root_keyset=['home'],
                key_interval=1.3,
                profile='roku',
                enable_smart_sense=True,
                waiting_time=3,
                report_data={
                    'analysis_type': 'monkey',
                    'section_id': 0,
                })
monkey.run()

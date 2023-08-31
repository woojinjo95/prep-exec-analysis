from scripts.monkey.monkey import Monkey
import logging

logger = logging.getLogger('monkey_test')


monkey = Monkey(duration=180,
                key_candidates=['right', 'down'],
                root_keyset=['home'],
                key_interval=1.3,
                profile='roku',
                enable_smart_sense=True,
                waiting_time=3,
                report_data={})
monkey.run()

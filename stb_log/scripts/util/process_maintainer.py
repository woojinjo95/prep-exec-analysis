import logging
import threading
import gc
from multiprocessing import Event, Process


logger = logging.getLogger('connection')


class ProcessMaintainer:
    def __init__(self, target, kwargs=(), revive_interval=None, daemon=True):
        self.init_property()
        self.target = target
        self.kwargs = kwargs
        self.revive_interval = revive_interval
        self.daemon = daemon

    def init_property(self):
        self.process = None
        self.reviver = None

    def start(self):
        if self.process:
            raise Exception('duplicate processes')

        self.process = Process(target=self.target, kwargs=self.kwargs)
        self.process.daemon = self.daemon
        self.process.start()
        # If interval is set, run the revive task
        if self.revive_interval:
            self.revive(self.revive_interval)

    def terminate(self):
        if self.process:
            # Stop revive task first
            if self.reviver:
                self.reviver.cancel()

            # Stop process on running state
            if self.process.is_alive():
                self.process.terminate()

            # Wait whether forced or normal exit
            self.process.join(timeout=5)
            self.init_property()

    # Periodic task when interval is given, also it can be done immediately without interval as needed
    def revive(self, interval=None):
        if not self.process.is_alive():
            logger.info(f'Revive {self.target.__name__}() process.')
            self.terminate()
            self.start()
            interval = None

        # If interval is set, run timer to execute task after a few seconds
        if interval:
            self.reviver = threading.Timer(self.revive_interval, self.revive, args=(interval, ))
            self.reviver.daemon = True
            self.reviver.start()

        gc.collect()

    def is_alive(self):
        if self.process and self.process.is_alive():
            return True
        else:
            return False

    def __del__(self):
        self.terminate()

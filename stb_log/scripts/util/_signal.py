import signal


def run_with_timeout(func, timeout_sec):
    def handler(signum, frame):
        raise TimeoutError(f"Function execution exceeded {timeout_sec} seconds timeout.")
    
    # Set the signal handler and an alarm
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_sec)
    
    try:
        func()
    finally:
        signal.alarm(0)  # Cancel the alarm

from ..utils._subprocess import kill_pid_grep, get_pid_grep
from signal import SIGTERM

streaming_ffmpeg_command_key_args = ('ffmpeg', 'v4l2', 'alsa', '-segment_time')


def get_active_capture_process() -> bool:
    if len(get_pid_grep(*streaming_ffmpeg_command_key_args)) > 0:
        return True
    else:
        return False


def kill_active_capture_process(signal=SIGTERM):
    # SIGTERM = 15
    kill_pid_grep(*streaming_ffmpeg_command_key_args, signal=signal)
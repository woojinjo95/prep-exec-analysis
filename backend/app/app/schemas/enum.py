from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class RemoteControlTypeEnum(ExtendedEnum):
    ir = "ir"
    bluetooth = "bluetooth"


class StbConnectionTypeEnum(ExtendedEnum):
    ssh = "ssh"
    adb = "adb"


class ProtocolEnum(ExtendedEnum):
    all = "all"
    tcp = "tcp"
    udp = "udp"


class ResumeMeasurementRecognizingKeyEventEnum(ExtendedEnum):
    power = "power"


class AnalysisTypeEnum(ExtendedEnum):
    freeze = "freeze"
    macroblock = "macroblock"
    resume = "resume"
    boot = "boot"
    channel_change_time = "channel_change_time"
    log_level_finder = "log_level_finder"


class LogLevelFinderTargetEnum(ExtendedEnum):
    logcat_f = "logcat_f"
    logcat_e = "logcat_e"
    logcat_s = "logcat_s"
    logcat_w = "logcat_w"
    logcat_i = "logcat_i"
    logcat_d = "logcat_d"
    logcat_v = "logcat_v"


class ChannelChangeTimeTargetEnum(ExtendedEnum):
    adjoint_channel = "adjoint_channel"
    nonadjoint_channel = "nonadjoint_channel"
    previous_channel = "previous_channel"

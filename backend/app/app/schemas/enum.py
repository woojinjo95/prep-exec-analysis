from enum import Enum

from app.core.config import settings

RemoconEnum = Enum('MeasureDirectionEnum', [(r, r) for r
                                            in settings.REMOCON_COMPANY.split(',')])


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
    loudness = "loudness"
    resume = "resume"
    boot = "boot"
    channel_change_time = "channel_change_time"
    log_level_finder = "log_level_finder"
    log_pattern_matching = "log_pattern_matching"


class LogLevelFinderTargetEnum(ExtendedEnum):
    V = "V" # verbose 가장 낮은 우선 순위 
    D = "D" # debug
    I = "I" # info
    W = "W" # warning
    E = "E" # error
    F = "F" # fatal
    S = "S" # silent 가장 높은 우선 순위


class ChannelChangeTimeTargetEnum(ExtendedEnum):
    adjoint_channel = "adjoint_channel"
    nonadjoint_channel = "nonadjoint_channel"
    previous_channel = "previous_channel"


class BlockTypeEnum(ExtendedEnum):
    rcu = "rcu"
    config = "config"
    shell = "shell"
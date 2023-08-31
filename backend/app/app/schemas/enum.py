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
    bt = "bt"


class ProtocolEnum(ExtendedEnum):
    all = "all"
    tcp = "tcp"
    udp = "udp"
    ip = "ip"
    icmp = "icmp"
    igmp = "igmp"


class ResumeTypeEnum(ExtendedEnum):
    image_matching = "image_matching"
    screen_change_rate = "screen_change_rate"


class BootTypeEnum(ExtendedEnum):
    image_matching = "image_matching"


class AnalysisTypeEnum(ExtendedEnum):
    freeze = "freeze"
    # macroblock = "macroblock"
    resume = "resume"
    boot = "boot"
    channel_change_time = "channel_change_time"
    log_level_finder = "log_level_finder"
    log_pattern_matching = "log_pattern_matching"
    # process_lifecycle_analysis = "process_lifecycle_analysis"
    # network_filter = "network_filter"


class LogLevelEnum(ExtendedEnum):
    V = "V"  # verbose 가장 낮은 우선 순위
    D = "D"  # debug
    I = "I"  # info
    W = "W"  # warning
    E = "E"  # error
    F = "F"  # fatal
    S = "S"  # silent 가장 높은 우선 순위


class ChannelChangeTimeTargetEnum(ExtendedEnum):
    adjoint_channel = "adjoint_channel"
    nonadjoint_channel = "nonadjoint_channel"


class BlockTypeEnum(ExtendedEnum):
    remocon_transmit = "remocon_transmit"
    on_off_control = "on_off_control"
    shell = "shell"
    packet_control = "packet_control"
    packet_block = "packet_block"
    monkey_test = "monkey_test"
    intelligent_monkey_test = "intelligent_monkey_test"


class LogModuleEnum(ExtendedEnum):
    stdin = "stdin"  # 입력
    stdout = "stdout"  # 출력
    stderr = "stderr"  # 에러


class ShellModeEnum(ExtendedEnum):
    adb = "adb"
    ssh = "ssh"


class ServiceStateEnum(ExtendedEnum):
    idle = "idle"
    streaming = "streaming"
    playblock = "playblock"
    analysis = "analysis"


class FreezeTypeEnum(ExtendedEnum):
    no_signal = "no_signal"
    black = "black"
    white = "white"
    one_colored = "one_colored"
    default = "default"

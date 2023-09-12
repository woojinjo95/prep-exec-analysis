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
    macroblock = "macroblock"
    loudness = "loudness"
    resume = "resume"
    boot = "boot"
    channel_change_time = "channel_change_time"
    log_level_finder = "log_level_finder"
    log_pattern_matching = "log_pattern_matching"
    process_lifecycle_analysis = "process_lifecycle_analysis"
    network_filter = "network_filter"
    monkey_test = "monkey_test"
    intelligent_monkey_test = "intelligent_monkey_test"


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
    non_adjoint_channel = "non_adjoint_channel"


class BlockTypeEnum(ExtendedEnum):
    remocon_transmit = "remocon_transmit"
    remocon_properties = "remocon_properties"
    on_off_control = "on_off_control"
    packet_control = "packet_control"
    packet_block = "packet_block"
    device_info = "device_info"
    network_emulation = "network_emulation"
    capture_board = "capture_board"
    shell = "shell"
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


class ExportItemEnum(ExtendedEnum):
    scenario = "scenario"
    stb_log = "stb_log"
    stb_info = "stb_info"
    loudness = "loudness"
    network_trace = "network_trace"
    terminal_log = "terminal_log"
    monkey_smart_sense = "monkey_smart_sense"
    monkey_section = "monkey_section"
    an_color_reference = "an_color_reference"
    an_freeze = "an_freeze"
    an_warm_boot = "an_warm_boot"
    an_cold_boot = "an_cold_boot"
    an_log_pattern = "an_log_pattern"
    videos = "videos"
    frames = "frames"

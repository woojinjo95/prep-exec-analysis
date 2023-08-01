from enum import Enum


class RemoteControlTypeEnum(str, Enum):
    ir = "ir"
    bluetooth = "bluetooth"


class StbConnectionTypeEnum(str, Enum):
    ssh = "ssh"
    adb = "adb"

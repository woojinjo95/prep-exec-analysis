from typing import List, Optional

from app.schemas.enum import ProtocolEnum, RemoteControlTypeEnum, ShellModeEnum
from pydantic import BaseModel


class StbConnection(BaseModel):
    mode: ShellModeEnum
    host: str
    port: str
    username: Optional[str]
    password: Optional[str]


class StbConnectionBase(BaseModel):
    items: List[StbConnection]


class PacketBlock(BaseModel):
    id: str
    ip: str
    port: Optional[int]
    protocol: Optional[ProtocolEnum] = ProtocolEnum.all


class HardwareConfiguration(BaseModel):
    remote_control_type: RemoteControlTypeEnum
    enable_dut_power: bool
    enable_hdmi: bool
    enable_dut_wan: bool
    enable_network_emulation: bool
    packet_bandwidth: int
    packet_delay: float
    packet_loss: float
    stb_connection: Optional[StbConnection]
    packet_block: Optional[List[PacketBlock]]


class HardwareConfigurationBase(BaseModel):
    items: HardwareConfiguration


class HardwareConfigurationUpdate(BaseModel):
    remote_control_type: Optional[RemoteControlTypeEnum]
    enable_dut_power: Optional[bool]
    enable_hdmi: Optional[bool]
    enable_dut_wan: Optional[bool]
    enable_network_emulation: Optional[bool]
    packet_bandwidth: Optional[int]
    packet_delay: Optional[float]
    packet_loss: Optional[float]

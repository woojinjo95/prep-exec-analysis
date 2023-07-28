from typing import List, Optional

from pydantic import BaseModel


class HardwareConfigurationIpLimit(BaseModel):
    id: str
    ip: str
    port: str
    type: str
    created_at: float


class HardwareConfiguration(BaseModel):
    remote_control_type: str  # TODO enum
    enable_dut_power: bool
    enable_hdmi: bool
    enable_dut_wan: bool
    enable_network_emulation: bool
    packet_bandwidth: int
    packet_delay: float
    packet_loss: float
    ip_limit: List[HardwareConfigurationIpLimit]


class HardwareConfigurationBase(BaseModel):
    items: HardwareConfiguration


class HardwareConfigurationUpdate(BaseModel):
    remote_control_type: Optional[str]
    enable_dut_power: Optional[bool]
    enable_hdmi: Optional[bool]
    enable_dut_wan: Optional[bool]
    enable_network_emulation: Optional[bool]
    packet_bandwidth: Optional[int]
    packet_delay: Optional[float]
    packet_loss: Optional[float]

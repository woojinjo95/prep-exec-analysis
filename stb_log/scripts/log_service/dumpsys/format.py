from dataclasses import dataclass


@dataclass
class CPUInfo:
    cpu_usage: str = ''
    total: str = ''
    user: str = ''
    kernel: str = ''
    iowait: str = ''
    irq: str = ''
    softirq: str = ''


@dataclass
class MemoryInfo:
    memory_usage: str = ''
    total_ram: str = ''
    free_ram: str = ''
    used_ram: str = ''
    lost_ram: str = ''


import { LogLevel } from '@global/constant'

export interface Logcat {
  timestamp: string
  module: string
  log_level: keyof typeof LogLevel
  process_name: string
  pid: number
  tid: number
  message: string
}

export interface Network {
  timestamp: string
  source: string
  destination: string
  protocol: 'all' | 'tcp' | 'udp' | 'ip' | 'icmp' | 'igmp'
  length: number
  info: string
}

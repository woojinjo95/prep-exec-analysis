import { LogLevel } from '@global/constant'
import { LogModule } from '../constants'

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
  src: string
  dst: string
  protocol: 'all' | 'tcp' | 'udp' | 'ip' | 'icmp' | 'igmp'
  length: number
  info: string
}

/**
 * 열린 쉘 정보
 */
export interface Shell {
  mode: 'adb' | 'ssh'
}

/**
 * 쉘 로그
 */
export interface ShellLog {
  timestamp: string
  module: keyof typeof LogModule
  message: string
}

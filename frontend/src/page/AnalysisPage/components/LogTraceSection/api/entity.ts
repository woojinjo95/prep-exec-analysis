// 'Silent' | 'Fatal' | 'Error' | 'Warning' | 'Info' | 'Debug' | 'Verbose'
export type LogcatLogLevel = 'S' | 'F' | 'E' | 'W' | 'I' | 'D' | 'V'

export interface Logcat {
  timestamp: string
  module: string
  log_level: string
  process_name: string
  pid: number
  tid: number
  message: string
}

export interface Network {
  timestamp: string
  source: string
  destination: string
  protocol: string
  length: number
  info: string
}

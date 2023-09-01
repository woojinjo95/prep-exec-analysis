import { FreezeType } from '@global/constant'

export interface LogLevelFinder {
  /**
   * @format timestamp
   */
  timestamp: string
  log_level: string
}

/**
 * 온전치 못한 데이터일 경우(ex: 에러) -> 빈문자열
 */
export interface CPU {
  /**
   * @format timestamp
   */
  timestamp: string
  cpu_usage: string
  total: string
  user: string
  kernel: string
  iowait: string
  irq: string
  softirq: string
}

/**
 * 온전치 못한 데이터일 경우(ex: 에러) -> 빈문자열
 */
export interface Memory {
  /**
   * @format timestamp
   */
  timestamp: string
  memory_usage: string
  total_ram: string
  free_ram: string
  used_ram: string
  lost_ram: string
}

export interface EventLog {
  /**
   * @format timestamp
   */
  timestamp: string
  service: string
  msg: string
  data: object
}

export interface ColorReference {
  /**
   * @format timestamp
   */
  timestamp: string

  /**
   * @min 0
   * @max 8
   */
  color_reference: number
}

export interface Freeze {
  /**
   * @format timestamp
   */
  timestamp: string
  freeze_type: keyof typeof FreezeType
  /**
   * 단위: s(초)
   */
  duration: number
}

export interface Loudness {
  /**
   * @format timestamp
   */
  timestamp: string
  m: number
}

export interface Resume {
  /**
   * @format timestamp
   */
  timestamp: string
  /**
   * 단위: ms(밀리초)
   */
  measure_time: number
}

export interface Boot {
  /**
   * @format timestamp
   */
  timestamp: string
  /**
   * 단위: ms(밀리초)
   */
  measure_time: number
}

export interface LogPatternMatching {
  /**
   * @format timestamp
   */
  timestamp: string
  log_pattern_name: string
  log_level: string
  message: string
}

import { AnalysisFrame, BootType, ResumeType } from '@global/api/entity'
import { FreezeType, LogLevel } from '@global/constant'

/**
 * 분석 설정
 */
export interface AnalysisConfig {
  freeze?: {
    color: string
    duration: number // second
  }
  loudness?: {
    color: string
  }
  resume?: {
    color: string
    type: ResumeType
    frame: AnalysisFrame
  }
  boot?: {
    color: string
    type: BootType
    frame: AnalysisFrame
  }
  channel_change_time?: {
    color: string
    targets: ('adjoint_channel' | 'nonadjoint_channel')[]
  }
  log_level_finder?: {
    color: string
    targets: (keyof typeof LogLevel)[]
  }
  log_pattern_matching?: {
    color: string
    items: {
      color: string
      name: string
      level: keyof typeof LogLevel
      regular_expression: string
    }[]
  }
  monkey_test?: {
    color: string
  }
  intelligent_monkey_test?: {
    color: string
  }
}

/**
 * 분석 결과 요약 데이터
 */
export interface AnalysisResultSummary {
  boot?: {
    color: string
    results: {
      total: number
      target: BootType
      avg_time: number // 단위: ms
    }[]
  }
  freeze?: {
    color: string
    results: {
      total: number
      error_type: keyof typeof FreezeType
    }[]
  }
  intelligent_monkey_test?: {
    color: string
    results: {
      section_id: number
      smart_sense: number
      image_path: string
    }[]
  }
  last_updated_timestamp: string
  log_level_finder?: {
    color: string
    results: {
      total: number
      target: keyof typeof LogLevel
    }[]
  }
  log_pattern_matching?: {
    color: string
    results: {
      total: number
      log_pattern_name: string
      color: string
    }[]
  }
  loudness?: {
    color: string
    lkfs: number
  }
  resume?: {
    color: string
    results: {
      total: number
      target: ResumeType
      avg_time: number // 단위: ms
    }[]
  }
  monkey_test?: {
    color: string
    results: {
      id: string
      duration_time: number // 단위: s
      smart_sense: number
    }[]
  }
}

export interface LogLevelFinder {
  /**
   * @format timestamp
   */
  timestamp: string
  log_level: keyof typeof LogLevel
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

interface RemoconResponseEventLog {
  msg: 'remocon_response'
  data: {
    key: string
    type: 'ir' | 'bt' // IR / BT
    press_time: number
    sensor_time: number
  }
}

interface OnOffControlResponseEventLog {
  msg: 'on_off_control_response'
  data: {
    enable_dut_power_transition?: string // DUT Power
    enable_hdmi_transition?: string // HDMI
    enable_dut_wan_transition?: string // DUT Wan
    vac: 'on' | 'off'
    sensor_time: number
  }
}

interface ShellResponseEventLog {
  msg: 'shell_response'
  data: {
    mode: 'adb' | 'ssh'
    command: string
  }
}

interface ConfigResponseEventLog {
  msg: 'config_response'
  data: {
    mode: 'adb' | 'ssh'
    host: string
    port: number
    username?: string
    password?: string
  }
}

export type EventLogTooltip =
  | RemoconResponseEventLog
  | OnOffControlResponseEventLog
  | ShellResponseEventLog
  | ConfigResponseEventLog

export type EventLog = {
  /**
   * @format timestamp
   */
  timestamp: string
  service: string
} & EventLogTooltip

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
  target: ResumeType
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
  target: BootType
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
  log_level: keyof typeof LogLevel
  message: string
  color: string
  regex: string
}

export interface MonkeySection {
  id: string
  /**
   * @format timestamp
   */
  start_timestamp: string
  /**
   * @format timestamp
   */
  end_timestamp: string
}

export interface MonkeySmartSense {
  id: string
  /**
   * @format timestamp
   */
  timestamp: string
  smart_sense_key: string[]
}

export interface IntelligentMonkeySection {
  section_id: number
  /**
   * @format timestamp
   */
  start_timestamp: string
  /**
   * @format timestamp
   */
  end_timestamp: string
}

export interface IntelligentMonkeySmartSense {
  /**
   * @format timestamp
   */
  timestamp: string
  section_id: number
  smart_sense_key: string[]
}

import { AnalysisFrame } from '@global/api/entity'
import { FreezeType, LogLevel } from '@global/constant'

export type ResumeType = 'image_matching' | 'screen_change_rate'
export type BootType = 'image_matching'

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
  // intelligent_monkey_test?: null
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
  // monkey_test?: null
}

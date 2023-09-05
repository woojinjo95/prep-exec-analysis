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
    frame: {
      image_path: string
      roi: {
        x: number
        y: number
        w: number
        h: number
      }
    }
  }
  boot?: {
    color: string
    type: BootType
    frame: {
      image_path: string
      roi: {
        x: number
        y: number
        w: number
        h: number
      }
    }
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
    total: number
    target: BootType
    avg_time: number // 단위: ms
  }[]
  freeze?: {
    total: number
    target: keyof typeof FreezeType
  }[]
  // intelligent_monkey_test?: null
  log_level_finder?: {
    total: number
    target: keyof typeof LogLevel
  }[]
  log_pattern_matching?: {
    total: number
    log_pattern_name: string
    color: string
  }[]
  loudness?: [
    {
      lkfs: number
    },
  ]
  resume?: {
    total: number
    target: ResumeType
    avg_time: number // 단위: ms
  }[]
  // monkey_test?: null
}

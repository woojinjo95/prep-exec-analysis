import { LogLevel } from '@global/constant'

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

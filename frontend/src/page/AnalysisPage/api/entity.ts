import { AnalysisFrame } from '@global/api/entity'
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

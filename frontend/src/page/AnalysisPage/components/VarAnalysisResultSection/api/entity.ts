import LogLevel from '@global/constant/logLevel'

/**
 * 분석 설정
 */
export interface AnalysisConfig {
  freeze?: {
    color: string
    duration: number
  }
  loudness?: {
    color: string
  }
  resume?: {
    color: string
    type: 'image_maching' | 'screen_change_rate'
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
    type: 'image_maching'
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

import { FreezeType, LogLevel } from '@global/constant'
import { BootType, ResumeType } from '@page/AnalysisPage/api/entity'

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

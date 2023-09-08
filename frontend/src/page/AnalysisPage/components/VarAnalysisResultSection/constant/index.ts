import { BootType, ResumeType } from '@global/api/entity'
import { AnalysisType, FreezeType } from '@global/constant'

/**
 * 설정 가능한 분석유형 리스트
 */
export const ConfigurableAnalysisTypes: (keyof typeof AnalysisType)[] = [
  'freeze',
  'loudness',
  'resume',
  'boot',
  'log_level_finder',
  'log_pattern_matching',
] as const

/**
 * 측정타입 라벨
 */
export const AnalysisTypeLabel: { [key in keyof typeof AnalysisType]: string } = {
  freeze: 'Freeze Detection',
  loudness: 'Loudness Measurement',
  resume: 'Resume Measurement',
  boot: 'Boot Measurement',
  channel_change_time: 'Channel Change Time Measurement',
  log_level_finder: 'Log Level Finder',
  log_pattern_matching: 'Log Pattern Matching',
  monkey_test: 'Monkey Test',
  intelligent_monkey_test: 'Intelligent Monkey Test (All-Menu Navigation)',
} as const

/**
 * AnalysisType - Resume의 Type 항목 라벨
 */
export const ResumeTypeLabel: { [key in ResumeType]: string } = {
  image_matching: 'Image Matching',
  screen_change_rate: 'Screen Change Rate',
} as const

/**
 * AnalysisType - Boot의 Type 항목 라벨
 */
export const BootTypeLabel: { [key in BootType]: string } = {
  image_matching: 'Image Matching',
} as const

/**
 * AnalysisType - Freeze의 Target 항목 라벨
 */
export const FreezeTypeLabel: { [key in keyof typeof FreezeType]: string } = {
  black: 'Black',
  default: 'Default',
  no_signal: 'No signal',
  one_colored: 'One colored',
  white: 'White',
}

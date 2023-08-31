import { AnalysisType } from '@global/constant'

/**
 * 설정 가능한 분석유형 리스트
 */
export const ConfigurableAnalysisTypes: (keyof typeof AnalysisType)[] = [
  'freeze',
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
} as const

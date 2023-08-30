import { AnalysisType } from '@global/constant'

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

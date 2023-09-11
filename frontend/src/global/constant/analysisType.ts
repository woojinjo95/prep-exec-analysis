/**
 * 분석 타입 enum
 */
const AnalysisType = {
  freeze: 'freeze',
  loudness: 'loudness',
  resume: 'resume', // warm booting
  boot: 'boot', // cold booting
  channel_change_time: 'channel_change_time',
  log_level_finder: 'log_level_finder',
  log_pattern_matching: 'log_pattern_matching',
  monkey_test: 'monkey_test',
  intelligent_monkey_test: 'intelligent_monkey_test',
} as const

export default AnalysisType

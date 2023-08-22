/**
 * 측정 유형 enum
 */
const AnalysisType = {
  freeze: 'freeze',
  loudness: 'loudness',
  resume: 'resume', // warm booting
  boot: 'boot', // cold booting
  channelChangeTime: 'channel_change_time',
  logLevelFinder: 'log_level_finder',
  logPatternMatching: 'log_pattern_matching',
} as const

export default AnalysisType

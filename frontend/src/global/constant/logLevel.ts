/**
 * 로그 레벨 enum
 */
const LogLevel = {
  F: 'F', // fatal
  E: 'E', // error
  W: 'W', // warning
  I: 'I', // info
  D: 'D', // debug
  V: 'V', // verbose 가장 낮은 우선 순위
} as const

export default LogLevel

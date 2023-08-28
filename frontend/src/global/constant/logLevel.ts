/**
 * 로그 레벨 enum
 */
const LogLevel = {
  V: 'V', // verbose 가장 낮은 우선 순위
  D: 'D', // debug
  I: 'I', // info
  W: 'W', // warning
  E: 'E', // error
  F: 'F', // fatal
} as const

export default LogLevel

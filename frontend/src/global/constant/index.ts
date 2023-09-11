import { LogConnectionStatus } from '@global/api/entity'
import PagePath from './pagePath'

export { default as AnalysisType } from './analysisType'
export { default as AppURL } from './appURL'
export { default as LogLevel } from './logLevel'
export { default as PagePath } from './pagePath'
export { default as FreezeType } from './freezeType'

/**
 * 웹사이트 접속 시 메인페이지
 */
export const DEFAULT_PAGE_PATH = PagePath.scenario

export const MILLISECONDS_PER_SECOND = 1000
export const MILLISECONDS_PER_MINUTE = 60 * MILLISECONDS_PER_SECOND

/**
 * 유효한 IP 문자열인지 체크하는 정규표현식
 */
export const IPRegex = /^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$/

export const PAGE_SIZE_TWENTY = 20
export const PAGE_SIZE_FIFTEEN = 15
export const PAGE_SIZE_TWELVE = 12
export const PAGE_SIZE_TEN = 10

/**
 * AreaChart, PointChart 높이
 */
export const CHART_HEIGHT = 64

/**
 * 월 영어 이름
 */
export const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

/**
 * 로그 연결여부 라벨
 */
export const LogConnectionStatusLabel: { [key in LogConnectionStatus]: string } = {
  log_connected: 'Log Connected',
  log_disconnected: 'Log Disconnected',
} as const

/**
 * 분석 모듈에 전달 가능한 분석유형
 *
 * AnalysisType 참고
 */
export const AnalyzableTypes = [
  'freeze',
  'loudness',
  'resume',
  'boot',
  'log_level_finder',
  'log_pattern_matching',
] as const

export type AnalyzableType = (typeof AnalyzableTypes)[number]

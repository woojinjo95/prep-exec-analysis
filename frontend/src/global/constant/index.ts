import { LogConnectionStatus } from '@global/api/entity'
import PagePath from './pagePath'
import LogLevel from './logLevel'
import AnalysisType from './analysisType'

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
 * 비디오 스냅샷 높이
 */
export const VIDEO_SNAPSHOT_HEIGHT = 64

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
 * 설정 가능한 분석유형
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
  'monkey_test',
  'intelligent_monkey_test',
] as const

export type AnalyzableType = (typeof AnalyzableTypes)[number]

/**
 * 로그레벨 색상
 */
export const LogLevelColor: {
  [log_level in keyof typeof LogLevel]: 'pink' | 'red' | 'orange' | 'yellow' | 'navy' | 'green' | 'grey'
} = {
  F: 'red',
  E: 'orange',
  W: 'yellow',
  I: 'navy',
  D: 'green',
  V: 'grey',
}

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

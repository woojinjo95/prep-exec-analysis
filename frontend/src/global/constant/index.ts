import { LogConnectionStatus } from '@global/api/entity'
import PagePath from './pagePath'

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

export const LogConnectionStatusLabel: { [key in LogConnectionStatus]: string } = {
  log_connected: 'Log Connected',
  log_disconnected: 'Log Disconnected',
} as const

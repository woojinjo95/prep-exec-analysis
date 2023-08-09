import PagePath from './pagePath'

/**
 * 웹사이트 접속 시 메인페이지
 */
export const DEFAULT_PAGE_PATH = PagePath.action

export const MILLISECONDS_PER_SECOND = 1000
export const MILLISECONDS_PER_MINUTE = 60 * MILLISECONDS_PER_SECOND

/**
 * 유효한 IP 문자열인지 체크하는 정규표현식
 */
export const IPRegex = /(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}/

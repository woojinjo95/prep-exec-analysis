import { atom } from 'recoil'
import { FreezeType, LogLevel } from '@global/constant'
import { BootType, ResumeType } from '@global/api/entity'

/**
 * 서비스가 타겟중인 시나리오 id
 */
export const scenarioIdState = atom<string | null>({
  key: 'scenarioIdState',
  // default: '61e34251-73da-4614-b460-999a4f29c44b',
  // default: '3201ba8a-b96d-4b11-9298-35cdee3eb476',
  default: null,
})

/**
 * 분석 페이지가 타겟중인 테스트런 id
 */
export const testRunIdState = atom<string | null>({
  key: 'testRunIdState',
  // default: '2023-09-01T065554F133036',
  default: null,
})

/**
 * 타임라인에서 파란색 커서가 가리키는 시간
 */
export const cursorDateTimeState = atom<Date | null>({
  key: 'cursorDateTimeState',
  default: null,
})

/**
 * block 녹화 모드 상태
 */
export const isBlockRecordModeState = atom<boolean>({
  key: 'isBlockRecordModeState',
  default: false,
})

/**
 * selected block id list
 */
export const selectedBlockIdsState = atom<string[]>({
  key: 'selectedBlockIdsState',
  default: [],
})

/**
 * 현재 선택한 remocon
 */
export const selectedRemoconNameState = atom<string | null>({
  key: 'selectedRemoconState',
  default: null,
})

/**
 * action page 재생 start time (unix timestamp)
 */
export const playStartTimeState = atom<number | null>({
  key: 'playStartTimeState',
  default: null,
})

/**
 * 분석 페이지 freeze 결과 filter 리스트(freeze type으로 필터링)
 */
export const freezeTypeFilterListState = atom<(keyof typeof FreezeType)[]>({
  key: 'freezeTypeFilterListState',
  default: [],
})

/**
 * 분석 페이지 resume 결과 filter 리스트(resume type으로 필터링)
 */
export const resumeTypeFilterListState = atom<ResumeType[]>({
  key: 'resumeTypeFilterListState',
  default: [],
})

/**
 * 분석 페이지 boot 결과 filter 리스트(boot type으로 필터링)
 */
export const bootTypeFilterListState = atom<BootType[]>({
  key: 'bootTypeFilterListState',
  default: [],
})

/**
 * 분석 페이지 log level filter 결과 filter 리스트(log level로 필터링)
 */
export const logLevelFinderLogLevelFilterListState = atom<(keyof typeof LogLevel)[]>({
  key: 'logLevelFinderLogLevelFilterListState',
  default: [],
})

/**
 * 분석 페이지 log pattern matching 결과 filter 리스트(log pattern name으로 필터링)
 */
export const logPatternMatchingNameFilterListState = atom<string[]>({
  key: 'logPatternMatchingNameFilterListState',
  default: [],
})

/**
 * 분석 페이지 monkey test 결과 filter 리스트(id로 필터링)
 */
export const monkeyTestIdFilterListState = atom<string[]>({
  key: 'monkeyTestIdFilterListState',
  default: [],
})

/**
 * 분석 페이지 intelligent monkey test 결과 filter 리스트(section id로 필터링)
 */
export const intelligentMonkeyTestSectionIdFilterListState = atom<number[]>({
  key: 'intelligentMonkeyTestSectionIdFilterListState',
  default: [],
})

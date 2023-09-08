import { atom } from 'recoil'
import { FreezeType } from '@global/constant'
import { ResumeType } from '@page/AnalysisPage/api/entity'

/**
 * 분석페이지 특정 시나리오의 비디오 Blob URL
 */
export const videoBlobURLState = atom<string | null>({
  key: 'videoBlobURLState',
  default: null,
})

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
 * test Option Modal open
 */
export const isTestOptionModalOpenState = atom<boolean>({
  key: 'isTestOptionModalOpenState',
  default: false,
})

/**
 * action page 재생 start time (unix timestamp)
 */
export const playStartTimeState = atom<number | null>({
  key: 'playStartTimeState',
  default: null,
})

/**
 * 분석 페이지 freeze 결과 filter 리스트
 */
export const freezeTypeFilterListState = atom<(keyof typeof FreezeType)[]>({
  key: 'freezeTypeFilterListState',
  default: [],
})

/**
 * 분석 페이지 resume 결과 filter 리스트
 */
export const resumeTypeFilterListState = atom<ResumeType[]>({
  key: 'resumeTypeFilterListState',
  default: [],
})

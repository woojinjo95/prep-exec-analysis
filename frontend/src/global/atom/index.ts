import { atom } from 'recoil'

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
  // FIXME: null로 변경,  페이지 진입 시 설정되도록 변경필요
  default: '5e731960-616a-436e-9cad-84fdbb39bbf4',
})

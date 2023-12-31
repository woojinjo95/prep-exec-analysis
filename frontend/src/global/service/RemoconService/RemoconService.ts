import { Subject } from 'rxjs'
import { CustomKeyTransmit, RemoconTransmit } from './type'

// --------------------------------------------------------------------------------//
// 이벤트 정의
const buttonClick$ = new Subject<RemoconTransmit>()
const customKeyClick$ = new Subject<CustomKeyTransmit>()

// TODO: Action 생성 여부 (customKey 수정, 삭제 시)

// --------------------------------------------------------------------------------//
// remocon 관련 Service

export const remoconService = {
  onButton$: () => buttonClick$.asObservable(),
  onCustomKey$: () => customKeyClick$.asObservable(),

  buttonClick: (remoconArgs: RemoconTransmit) => buttonClick$.next(remoconArgs),
  customKeyClick: (customKeyArgs: CustomKeyTransmit) => customKeyClick$.next(customKeyArgs),
}

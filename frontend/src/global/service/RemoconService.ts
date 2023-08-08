import { Subject } from 'rxjs'
import { BlockEvent } from './type'

// --------------------------------------------------------------------------------//
// 이벤트 정의
const buttonClick$ = new Subject<BlockEvent>()
const customKeyClick$ = new Subject<BlockEvent>()

// TODO: Action 생성 여부 (customKey 수정, 삭제 시)

// --------------------------------------------------------------------------------//
// remocon 관련 Service

export const remoconService = {
  onButton$: () => buttonClick$.asObservable(),
  onCustomKey$: () => customKeyClick$.asObservable(),

  buttonClick: (buttonName: string) => buttonClick$.next({ type: 'RCU', value: buttonName }),
  customKeyClick: (keyName: string) => customKeyClick$.next({ type: 'RCU', value: keyName }),
}

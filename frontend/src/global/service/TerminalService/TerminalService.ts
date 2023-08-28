import { Subject } from 'rxjs'
import { CommandTransmit } from './type'

// --------------------------------------------------------------------------------//
// 이벤트 정의
const buttonClick$ = new Subject<CommandTransmit>()

// --------------------------------------------------------------------------------//
// terminal 관련 Service

export const terminalService = {
  onButton$: () => buttonClick$.asObservable(),

  buttonClick: (terminalArgs: CommandTransmit) => buttonClick$.next(terminalArgs),
}

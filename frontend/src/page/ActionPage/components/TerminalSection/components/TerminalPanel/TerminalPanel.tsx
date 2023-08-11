import ws from '@global/module/websocket'
import { Button, Text } from '@global/ui'
import React, { useEffect, useState } from 'react'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import classNames from 'classnames/bind'
import styles from './TerminalPanel.module.scss'
import TerminalShell from './TerminalShell'
import { Terminal } from '../../types'

const cx = classNames.bind(styles)

/**
 * Terminal 탭의 패널
 */

const TerminalPanel: React.FC = () => {
  // useEffect(() => {
  //   ws.send('{"level": "info", "msg": "shell", "service": "test", "data": {"command": "ls", "shell_id": 2}}')

  //   ws.onmessage = (e: MessageEvent) => {
  //     console.log(e.data)
  //   }
  // }, [])

  // config type은 어떻게 될지 모르겠음
  // backend에 현재 해당 config로 connect할 수 있는지에 대한 api 요청 후 허용 되면 terminal 생성 가능
  const [terminals, setTerminals] = useState<Terminal[]>([])

  const [curTerminal, setCurTerminal] = useState<Terminal | null>(null)

  // useEffect(() => {
  //   setTerminals((prev) => [...prev, { config: 'test' }])
  // }, [])

  useEffect(() => {
    if (terminals.length > 0) {
      setCurTerminal(terminals[terminals.length - 1])
    }
  }, [terminals])

  return (
    <div className="grid grid-cols-[4.5fr_1fr]">
      <div>{curTerminal && <TerminalShell terminal={curTerminal} />}</div>
      <div className="flex flex-col justify-center p-5">
        <Button
          colorScheme="grey"
          onClick={() => setTerminals((prev) => [...prev, { config: `test ${terminals.length}` }])}
          className="h-12"
        >
          Add Terminal
        </Button>
        <div className="flex flex-col w-full mt-3">
          {terminals &&
            terminals.map((terminal, idx) => {
              return (
                <div
                  className="w-full flex justify-between h-10 items-center mb-1 cursor-pointer"
                  key={`terminal_${idx}`}
                  onClick={() => setCurTerminal(terminal)}
                >
                  <Text colorScheme="light" className="text-[15px]">
                    Adb #{idx}
                  </Text>
                  <div className="flex">
                    <TrashIcon className={cx('trash-icon', 'h-5 w-5 mr-3')} />
                    <TrashIcon className={cx('trash-icon', 'h-5 w-5')} />
                  </div>
                </div>
              )
            })}
        </div>
      </div>
    </div>
  )
}

export default TerminalPanel

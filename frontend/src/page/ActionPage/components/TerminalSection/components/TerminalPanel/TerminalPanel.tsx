import { Button, Text } from '@global/ui'
import React, { useEffect, useRef, useState } from 'react'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import classNames from 'classnames/bind'
import useWebsocket from '@global/module/websocket'
import styles from './TerminalPanel.module.scss'
import TerminalShell from './TerminalShell'
import { ShellMessage, Terminal } from '../../types'

const cx = classNames.bind(styles)

/**
 * Terminal 탭의 패널
 */

const TerminalPanel: React.FC = () => {
  const [terminals, setTerminals] = useState<Terminal[]>([])

  const [currentTerminal, setCurrentTerminal] = useState<Terminal | null>(null)

  const scrollContainerRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    if (terminals.length > 0) {
      setCurrentTerminal(terminals[terminals.length - 1])
    }
  }, [terminals])

  useWebsocket<ShellMessage>({
    onMessage: (msg) => {
      if (msg.data && msg.msg === 'shell' && scrollContainerRef.current) {
        scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight
      }
    },
  })

  return (
    <div className="grid grid-cols-[4.5fr_1fr] h-full">
      <div className="h-full overflow-y-auto" ref={scrollContainerRef}>
        {currentTerminal &&
          terminals &&
          terminals.map((terminal) => (
            <TerminalShell terminal={terminal} currentTerminal={currentTerminal} key={`terminal_${terminal.id}`} />
          ))}
      </div>
      <div className="flex flex-col justify-center p-5 h-full">
        <Button
          colorScheme="grey"
          onClick={() => setTerminals((prev) => [...prev, { id: `${terminals.length}` }])}
          className="h-12"
        >
          Add Terminal
        </Button>
        <div className="flex flex-col w-full mt-3 h-full">
          {terminals &&
            terminals.map((terminal, idx) => {
              return (
                <div
                  className="w-full flex justify-between h-10 items-center mb-1 cursor-pointer"
                  key={`terminal_${idx}`}
                  onClick={() => setCurrentTerminal(terminal)}
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

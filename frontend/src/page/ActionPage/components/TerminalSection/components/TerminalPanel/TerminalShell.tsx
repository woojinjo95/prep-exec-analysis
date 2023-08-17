import React, { useState } from 'react'
import { Text } from '@global/ui'
import useWebsocket from '@global/module/websocket'
import { History, ShellMessage, Terminal } from '../../types'
import CommandInput from './CommandInput'

interface TerminalShellProps {
  terminal: Terminal
  currentTerminal: Terminal
}

const TerminalShell: React.FC<TerminalShellProps> = ({ terminal, currentTerminal }) => {
  const [historys, setHistorys] = useState<History[]>([])

  useWebsocket<ShellMessage>({
    onMessage: (msg) => {
      if (msg.data && msg.msg === 'shell') {
        const newHistory: History = {
          type: msg.data.data.module === 'stdin' ? 'command' : 'response',
          message: msg.data.data.message,
        }

        setHistorys((prev) => [...prev, newHistory])
      }
    },
  })

  return (
    <div className="w-full h-full flex flex-col" style={{ display: currentTerminal.id !== terminal.id ? 'none' : '' }}>
      {historys.map((history, idx) => (
        <div key={`history_${idx}_${terminal.id}`} className="flex">
          {/* 명령어 history면 CommandInput처럼 표기 */}
          {history.type === 'command' && (
            <Text className="whitespace-pre">
              {`${terminal.id}: / $`}
              {`    `}
            </Text>
          )}

          <Text>{history.message}</Text>
        </div>
      ))}
      <CommandInput terminal={terminal} />
    </div>
  )
}

export default TerminalShell

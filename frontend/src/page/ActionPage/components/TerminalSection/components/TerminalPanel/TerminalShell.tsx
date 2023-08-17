import React, { useEffect, useRef, useState } from 'react'
import { Text } from '@global/ui'
import useWebsocket from '@global/module/websocket'
import { SubscribeMessage } from '@global/module/websocket/types'
import { History, Message, Terminal } from '../../types'
import CommandInput from './CommandInput'

interface TerminalShellProps {
  terminal: Terminal
  currentTerminal: Terminal
}

interface ShellMessage {
  shell_id: 1 | 2
  mode: 'adb' | 'ssh'
  data: { timestamp: string; module: 'stdin' | 'stdout' | 'stderr'; message: string }
}

const TerminalShell: React.FC<TerminalShellProps> = ({ terminal, currentTerminal }) => {
  const [historys, setHistorys] = useState<History[]>([])

  useWebsocket<ShellMessage>({
    onMessage: (msg) => {
      if (msg.data && msg.msg === 'shell') {
        console.log('test', msg)
        const newHistory: History = {
          type: msg.data.data.module === 'stdin' ? 'command' : 'response',
          message: msg.data.data.message,
        }

        setHistorys((prev) => [...prev, newHistory])
      }
    },
  })

  return (
    <div className="w-full flex flex-col" style={{ display: currentTerminal.id !== terminal.id ? 'none' : '' }}>
      {historys.map((history, idx) => (
        <div key={`history_${idx}_${terminal.id}`} className="flex">
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

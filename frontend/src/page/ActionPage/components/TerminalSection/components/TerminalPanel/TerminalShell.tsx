import React, { useEffect, useRef, useState } from 'react'
import { Text } from '@global/ui'
import ws from '@global/module/websocket'
import { History, Message, Terminal } from '../../types'

interface TerminalShellProps {
  terminal: Terminal
  curTerminal: Terminal
}

const CommandInput = ({ terminal }: { terminal: Terminal }): JSX.Element => {
  // const [isMessageEnd, setIsMessageEnd] = useState<boolean>(false)

  const [curCommand, setCurCommand] = useState<string | null>(null)
  // const [curServerMessages, setCurServerMessages] = useState<string[]>([])

  // useEffect(() => {
  //   if (isMessageEnd && curCommand) {
  //     const newInputLog: HistoryLog = { type: 'input', message: curCommand }
  //     const newResponseLogs: HistoryLog[] = curServerMessages.map((msg) => {
  //       return {
  //         type: 'response',
  //         message: msg,
  //       }
  //     })

  //     const newHistory: History = { logs: [newInputLog, ...newResponseLogs] }

  //     setHistorys((prev) => [...prev, newHistory])
  //   }
  // }, [isMessageEnd])

  useEffect(() => {
    if (curCommand) {
      ws.send(
        `{"level": "info", "msg": "shell", "service": "test", "data": {"command": "${curCommand}", "shell_id": 2}}`,
      )
    }
  }, [curCommand])

  const textareaRef = useRef<HTMLTextAreaElement | null>(null)

  const defaultValue = `${terminal.id}: / $    `
  const [value, setValue] = useState<string>(defaultValue)

  const handleResizeHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`

      setValue(defaultValue + textareaRef.current.value.substring(defaultValue.length))
    }
  }

  return (
    <div className="flex flex-col">
      <textarea
        onChange={handleResizeHeight}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            setCurCommand(value.substring(defaultValue.length))

            if (textareaRef.current) {
              textareaRef.current.blur()
            }
          }
        }}
        ref={textareaRef}
        className="w-full whitespace-pre-wrap bg-transparent text-white border-none h-auto outline-none"
        rows={1}
        value={value}
      />
      {/* {curServerMessages.length > 0 &&
        curServerMessages.map((msg, index) => <Text key={`msg_${msg}_${terminal.id}_${index}`}>{msg}</Text>)} */}
    </div>
  )
}

const TerminalShell: React.FC<TerminalShellProps> = ({ terminal, curTerminal }) => {
  // const divRef = useRef<HTMLDivElement | null>(null)

  const [historys, setHistorys] = useState<History[]>([])
  // const [curServerMessages, setCurServerMessages] = useState<string[]>([])

  useEffect(() => {
    ws.onmessage = (e: MessageEvent) => {
      // type을 지정한 뒤 JSON으로 파싱하여 사용
      const msg = JSON.parse(e.data as string) as Message

      if (msg.data && msg.data.data) {
        const newHistory: History = {
          type: msg.data.data.module === 'stdin' ? 'command' : 'response',
          message: msg.data.data.message,
        }

        setHistorys((prev) => [...prev, newHistory])
      }
    }
  }, [])

  return (
    <div className="w-full flex flex-col" style={{ display: curTerminal.id !== terminal.id ? 'none' : '' }}>
      {historys.map((history, idx) => (
        <Text key={`history_${history.message}_${terminal.id}_${idx}`}>{history.message}</Text>
      ))}
      <CommandInput terminal={terminal} />
    </div>
  )
}

export default TerminalShell

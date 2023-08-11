import React, { useEffect, useRef, useState } from 'react'
import { Text } from '@global/ui'
import ws from '@global/module/websocket'
import { Terminal } from '../../types'

interface TerminalShellProps {
  terminal: Terminal
}

const CommandInput = ({
  terminal,
  setCurCommand,
}: {
  terminal: Terminal
  setCurCommand: React.Dispatch<React.SetStateAction<string | null>>
}): JSX.Element => {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)

  const defaultValue = `${terminal.config}: / $    `
  const [value, setValue] = useState<string>(defaultValue)

  const handleResizeHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`

      setValue(defaultValue + textareaRef.current.value.substring(defaultValue.length))
    }
  }

  return (
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
  )
}

const TerminalShell = ({ terminal }: TerminalShellProps): JSX.Element => {
  const [curCommand, setCurCommand] = useState<string | null>(null)
  const [curServerMessage, setServerCurMessage] = useState<string | null>(null)

  useEffect(() => {
    if (curCommand) {
      ws.send(
        `{"level": "info", "msg": "shell", "service": "test", "data": {"command": "${curCommand}", "shell_id": 2}}`,
      )
    }
  }, [curCommand])

  useEffect(() => {
    ws.onmessage = (e: MessageEvent) => {
      setServerCurMessage(e.data as string)
    }
  }, [])

  return (
    <div className="w-full flex flex-col">
      <CommandInput terminal={terminal} setCurCommand={setCurCommand} />
      {curServerMessage && <Text>{curServerMessage}</Text>}
    </div>
  )
}

export default TerminalShell

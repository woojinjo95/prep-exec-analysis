import React, { useRef, useState } from 'react'
import useWebsocket from '@global/module/websocket'
import { ShellMessage, Terminal } from '../../types'

const CommandInput = ({
  terminal, // sendMessage,
}: {
  terminal: Terminal
}): JSX.Element => {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)
  const { sendMessage } = useWebsocket<ShellMessage>({
    onMessage: (msg) => {
      if (msg.data && msg.msg === 'shell' && textareaRef.current && msg.service === 'shell') {
        textareaRef.current.focus()
      }
    },
  })

  const defaultValue = `${terminal.id}: / $    `
  const [value, setValue] = useState<string>(defaultValue)

  const handleResizeHeight = () => {
    if (textareaRef.current) {
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
            sendMessage({
              msg: 'shell',
              data: { command: `${value.substring(defaultValue.length)}`, shell_id: 2 },
            })

            if (textareaRef.current) {
              textareaRef.current.blur()
            }

            setValue(defaultValue)
          }
        }}
        ref={textareaRef}
        className="w-full whitespace-pre-wrap bg-transparent text-white border-none h-auto outline-none"
        rows={1}
        value={value}
        // 크기 조절 ui 제거
        style={{ resize: 'none' }}
      />
    </div>
  )
}

export default CommandInput

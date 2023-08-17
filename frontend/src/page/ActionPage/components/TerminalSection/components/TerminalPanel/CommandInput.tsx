import React, { useEffect, useRef, useState } from 'react'
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
      if (msg.data && msg.msg === 'shell' && textareaRef.current) {
        textareaRef.current.focus()
      }
    },
  })

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
            console.log('enter')
            sendMessage({
              level: 'info',
              msg: 'shell',
              time: new Date().getTime(),
              data: { command: `${value.substring(defaultValue.length)}`, shell_id: 2 },
            })
            // setCurCommand(value.substring(defaultValue.length))

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
      />
    </div>
  )
}

export default CommandInput

import React, { useEffect, useMemo, useRef, useState } from 'react'
import useWebsocket from '@global/module/websocket'
import { useHardwareConfiguration } from '@global/api/hook'
import { Text } from '@global/ui'
import { History, ShellMessage, Terminal } from '@global/types'
import { terminalService } from '@global/service/TerminalService/TerminalService'

interface CommandInputProps {
  terminal: Terminal
  historys: History[]
  isShellClicked: boolean
  setIsShellClicked: React.Dispatch<React.SetStateAction<boolean>>
}

const CommandInput: React.FC<CommandInputProps> = ({
  terminal,
  historys,
  isShellClicked,
  setIsShellClicked,
}): JSX.Element => {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null)
  const { sendMessage } = useWebsocket<ShellMessage>({
    onMessage: (msg) => {
      if (msg.data && msg.msg === 'shell' && textareaRef.current && msg.service === 'shell') {
        textareaRef.current.focus()
      }
    },
  })

  const { hardwareConfiguration } = useHardwareConfiguration()

  const [value, setValue] = useState<string>('')

  const commandHistory: string[] = useMemo(() => {
    return historys.filter((history) => history.type === 'command').map((data) => data.message)
  }, [historys])

  const [currentHistoryIdx, setCurrentHistoryIdx] = useState<number>(0)

  useEffect(() => {
    if (commandHistory && commandHistory.length >= 1) {
      setCurrentHistoryIdx(commandHistory.length)
    }
  }, [commandHistory])

  useEffect(() => {
    if (!textareaRef.current) {
      return
    }

    if (isShellClicked) {
      textareaRef.current.focus()
      setIsShellClicked(false)
    }
  }, [isShellClicked, setIsShellClicked])

  const handleResizeHeight = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (textareaRef.current) {
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`

      setValue(e.currentTarget.value)
    }
  }

  return (
    <div className="flex">
      <Text colorScheme="light" className="mr-[10px]">
        {terminal.id} / ${' '}
      </Text>
      <textarea
        onChange={handleResizeHeight}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && hardwareConfiguration && hardwareConfiguration.stb_connection) {
            sendMessage({
              msg: 'shell',
              data: {
                command: `${value}`,
                shell_id: hardwareConfiguration.stb_connection.mode === 'adb' ? 1 : 2,
              },
            })

            terminalService.buttonClick({
              type: 'shell',
              data: {
                command: value,
              },
            })

            if (textareaRef.current) {
              textareaRef.current.blur()
            }

            setValue('')
          }

          if (e.key === 'ArrowUp' && commandHistory) {
            if (currentHistoryIdx !== 0) {
              setValue(commandHistory[currentHistoryIdx - 1])
              setCurrentHistoryIdx((prev) => prev - 1)
            }
          }

          if (e.key === 'ArrowDown' && commandHistory) {
            if (currentHistoryIdx !== commandHistory.length - 1) {
              setValue(commandHistory[currentHistoryIdx + 1])
              setCurrentHistoryIdx((prev) => prev + 1)
            }
          }
        }}
        ref={textareaRef}
        className="whitespace-pre-wrap bg-transparent text-white border-none h-auto outline-none flex-1"
        rows={1}
        value={value}
        // 크기 조절 ui 제거
        style={{ resize: 'none' }}
      />
    </div>
  )
}

export default CommandInput

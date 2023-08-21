import { Button, Text } from '@global/ui'
import React, { useEffect, useRef, useState } from 'react'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import useWebsocket from '@global/module/websocket'
import { useMutation } from 'react-query'
import { useToast } from '@chakra-ui/react'
import { useHardwareConfiguration } from '@global/api/hook'
import TerminalShell from './TerminalShell'
import { ShellMessage, Terminal } from '../../types'
import { postConnect, postDisconnect } from '../../api/func'

/**
 * Terminal 탭의 패널
 */

const TerminalPanel: React.FC = () => {
  const toast = useToast({ duration: 3000, isClosable: true })
  // 지금은 terminal 한개 연결만 고려
  const [terminals, setTerminals] = useState<Terminal[]>([])

  const [currentTerminal, setCurrentTerminal] = useState<Terminal | null>(null)

  const scrollContainerRef = useRef<HTMLDivElement | null>(null)

  const { hardwareConfiguration } = useHardwareConfiguration()

  const { mutate: shellConnect } = useMutation(postConnect, {
    onSuccess: () => {
      if (hardwareConfiguration?.stb_connection) {
        setTerminals((prev) => [
          ...prev,
          { id: `${terminals.length}`, mode: hardwareConfiguration.stb_connection!.mode },
        ])
      }
    },
    onError: (err) => {
      console.error(err)
      toast({ status: 'error', title: 'An error has occurred while connecting. Please try again.' })
    },
  })

  const { mutate: shellDisconnect } = useMutation(postDisconnect, {
    onSuccess: () => {
      // 지금은 terminal 연결 하나만 있다고 고려
      setTerminals([])
      setCurrentTerminal(null)
    },
    onError: (err) => {
      console.error(err)
      toast({ status: 'error', title: 'An error has occurred while connecting. Please try again.' })
    },
  })

  useEffect(() => {
    if (terminals.length > 0) {
      setCurrentTerminal(terminals[terminals.length - 1])
    }
  }, [terminals])

  useWebsocket<ShellMessage>({
    onMessage: (msg) => {
      if (msg.data && msg.msg === 'shell' && msg.service === 'shell' && scrollContainerRef.current) {
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
          onClick={() => {
            // terminal 1개만 고려
            if (hardwareConfiguration) {
              if (!hardwareConfiguration.stb_connection) {
                toast({ status: 'warning', title: 'Device info setting is not completed.' })
              }

              if (terminals.length < 1) {
                shellConnect()
              }
            }
          }}
          className="h-12"
        >
          Add Terminal
        </Button>
        <div className="flex flex-col w-full mt-3 h-full">
          {terminals?.map((terminal, idx) => {
            return (
              <div
                className="w-full flex justify-between h-10 items-center mb-1 cursor-pointer"
                key={`terminal_${idx}`}
                onClick={() => setCurrentTerminal(terminal)}
              >
                <Text colorScheme="light" className="text-[15px]">
                  {terminal.mode} #{idx}
                </Text>
                <div className="flex">
                  <TrashIcon className="h-5 w-5 mr-3 fill-white" />
                  <TrashIcon
                    className="h-5 w-5 fill-white"
                    onClick={() => {
                      shellDisconnect()
                    }}
                  />
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

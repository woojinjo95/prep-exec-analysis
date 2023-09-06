import { playStartTimeState, scenarioIdState } from '@global/atom'
import { useWebsocket } from '@global/hook'
import { Button, Input, Modal, Text } from '@global/ui'
import React, { useEffect, useRef, useState } from 'react'
import { useRecoilState, useRecoilValue } from 'recoil'

interface TestOptionModalProps {
  isOpen: boolean
  close: () => void
}

const TestOptionModal: React.FC<TestOptionModalProps> = ({ isOpen, close }) => {
  const firstFocusableElementRef = useRef<HTMLInputElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        // shift : 역으로 이동
        if (event.shiftKey) {
          if (document.activeElement === firstFocusableElementRef.current) {
            event.preventDefault()
            lastFocusableElementRef.current?.focus()
          }
        } else if (document.activeElement === lastFocusableElementRef.current) {
          event.preventDefault()
          firstFocusableElementRef.current?.focus()
        }
      }
    }

    firstFocusableElementRef.current?.focus()

    document.addEventListener('keydown', handleKeyDown)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [])

  const scenarioId = useRecoilValue(scenarioIdState)

  const { sendMessage } = useWebsocket()

  const [repeatTime, setRepeatTime] = useState<number>(1)

  const [, setPlayStartTime] = useRecoilState(playStartTimeState)

  return (
    <Modal
      isOpen={isOpen}
      close={() => {
        close()
      }}
      title="Test Option"
    >
      <div className="h-[100px] w-[620px] flex flex-col justify-between">
        <div className="flex items-center">
          <Text colorScheme="light" className="w-[180px]">
            Repeat
          </Text>
          <Input
            ref={firstFocusableElementRef}
            className="w-[151px] h-12"
            value={repeatTime}
            onChange={(e) => setRepeatTime(Number(e.target.value))}
          />
          <Text colorScheme="light" className="ml-3">
            Time(s)
          </Text>
        </div>
        <Text size="xs" colorScheme="orange">
          If you run the test for more than 2 hours, have difficulty checking the analysis results.
        </Text>
      </div>
      <div className="flex justify-end mt-7">
        <Button
          colorScheme="primary"
          className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
          onClick={() => {
            if (!scenarioId) return

            sendMessage({
              level: 'info',
              msg: 'start_playblock',
              data: { scenario_id: scenarioId },
            })
            // TODO: repeat 횟수 반영 작업이 필요함

            setPlayStartTime(new Date().getTime() / 1000)
            close()
          }}
        >
          Open
        </Button>
        <Button
          colorScheme="grey"
          className="w-[132px] h-[48px] text-white rounded-3xl"
          ref={lastFocusableElementRef}
          onClick={() => {
            close()
          }}
        >
          Cancel
        </Button>
      </div>
    </Modal>
  )
}

export default TestOptionModal

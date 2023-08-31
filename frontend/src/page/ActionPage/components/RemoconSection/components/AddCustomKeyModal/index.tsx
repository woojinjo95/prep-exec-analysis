import React, { useEffect, useRef, useState } from 'react'
import cx from 'classnames'
import { AppURL } from '@global/constant'
import { KeyEvent } from '@page/ActionPage/types'
import { Button, Text, Modal } from '@global/ui'
import { Remocon } from '../../api/entity'
import AddCustomKeyModalRemoconButtons from './AddCustomKeyModalRemoconButtons'
import SaveCustomKeyModal from './SaveCustomKeyModal'

interface AddCustomKeyModalProps {
  remocon: Remocon
  isOpen: boolean
  close: () => void
  keyEvent: KeyEvent | null
}

const AddCustomKeyModal: React.FC<AddCustomKeyModalProps> = ({
  remocon,
  isOpen,
  close,
  keyEvent,
}: AddCustomKeyModalProps) => {
  // 리모컨 입력 확인을 위한 임시 string
  const [remoconInput, setRemoconInput] = useState<string[]>([])

  const firstFocusableElementRef = useRef<HTMLButtonElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const remoconRef = useRef<HTMLImageElement | null>(null)
  const [isLoadedRemoconImage, setIsLoadedRemoconImage] = useState<boolean>(false)

  /**
   * Submit 버튼을 눌렀는지 여부
   * 추가 리모콘 모달은 isSubmitted 여부에 따라 렌더링 결정 (isSubmitted 이후에는 최종 추가 모달이 생성)
   */
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false)

  useEffect(() => {
    setIsLoadedRemoconImage(false)
  }, [remocon])

  // Tab 이동 제어
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

  const [remoconWidth, setRemoconWidth] = useState<number | null>(null)

  useEffect(() => {
    const handleResize = () => {
      if (remoconRef.current) {
        setRemoconWidth(remoconRef.current.offsetWidth)
      }
    }

    handleResize()

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  return (
    <>
      {!isSubmitted && (
        <Modal
          isOpen={isOpen}
          close={() => {
            setRemoconInput([])
            close()
          }}
          mode="normal"
          className={cx('right-3.5 h-[95vh] w-[700px] top-1/2 -translate-y-1/2')}
        >
          <div className="h-full w-full flex flex-col items-center justify-between relative">
            <div className="flex flex-col items-center">
              <p className="text-white text-lg">Press the Keys in order and press the [Submit] button</p>
              <div>
                <div className="mt-[15px] h-[75vh]">
                  <div className={cx('w-full h-full flex relative')}>
                    <img
                      ref={remoconRef}
                      onLoad={() => {
                        setIsLoadedRemoconImage(true)
                      }}
                      src={`${AppURL.backendURL}${remocon.image_path}`}
                      alt="remocon"
                      className="w-full"
                    />
                    {isLoadedRemoconImage && (
                      <AddCustomKeyModalRemoconButtons
                        keyEvent={keyEvent}
                        remoconRef={remoconRef}
                        remocon={remocon}
                        setRemoconInput={setRemoconInput}
                      />
                    )}
                  </div>
                </div>
                {remoconWidth && (
                  <div
                    className="absolute top-[100px] flex flex-col"
                    style={{ left: 400 + remoconWidth / 2, width: 350 - remoconWidth / 2 }}
                  >
                    <div className="w-full flex flex-col">
                      <Text colorScheme="grey" className="!text-[18px] mb-3" weight="bold">
                        Pressed Key
                      </Text>
                      {remoconInput.map((input, idx) => (
                        <Text colorScheme="light" className="!text-[16px]" key={`remocon-input-${input}-${idx}`}>
                          {input}
                        </Text>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
            <div className="flex flex-col items-center">
              <div className="flex">
                <Button
                  colorScheme="primary"
                  className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
                  ref={firstFocusableElementRef}
                  onClick={() => {
                    setIsSubmitted(true)
                  }}
                >
                  Submit
                </Button>
                <Button
                  colorScheme="grey"
                  className="w-[132px] h-[48px] text-white rounded-3xl"
                  ref={lastFocusableElementRef}
                  onClick={() => {
                    setRemoconInput([])
                    close()
                  }}
                >
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        </Modal>
      )}

      {isSubmitted && (
        <SaveCustomKeyModal
          isOpen={isSubmitted}
          close={() => {
            setIsSubmitted(false)
            close()
          }}
          remoconInput={remoconInput}
          remocon={remocon}
        />
      )}
    </>
  )
}

export default AddCustomKeyModal

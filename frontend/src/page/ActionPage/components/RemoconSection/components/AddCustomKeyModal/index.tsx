import React, { useEffect, useRef, useState } from 'react'
import { useMutation, useQuery } from 'react-query'
import cx from 'classnames'
import useOutSideRef from '@global/hook/useOutsideRef'
import AppURL from '@global/constant/appURL'
import { KeyEvent } from '@page/ActionPage/types'
import { Remocon } from '../../api/entity'
import AddCustomKeyModalRemoconButtons from './AddCustomKeyModalRemoconButtons'
import { getRemocon, postCustomKey } from '../../api/func'

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

  const { ref: customKeyModalRef } = useOutSideRef({
    isOpen,
    closeHook: () => {
      setRemoconInput([])
      close()
    },
  })

  const firstFocusableElementRef = useRef<HTMLButtonElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const remoconRef = useRef<HTMLImageElement | null>(null)
  const [isLoadedRemoconImage, setIsLoadedRemoconImage] = useState<boolean>(false)

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

  const { refetch } = useQuery<Remocon[]>(['remocon'], () => getRemocon(), {
    onError: (err) => {
      console.error(err)
    },
  })

  const { mutate: postCustomKeyMutate } = useMutation(postCustomKey, {
    onSuccess: () => {
      refetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  return (
    <div
      className={cx('absolute top-[10px] right-3.5 h-auto z-10', {
        left: customKeyModalRef.current && customKeyModalRef.current.getBoundingClientRect().left,
      })}
      ref={customKeyModalRef}
    >
      <div className="flex flex-col h-[95vh] w-[700px] bg-[#323339] rounded-[10px] pt-7 pl-[72px] pr-[72px] pb-7 items-center justify-between">
        <div className="flex flex-col items-center">
          <p className="text-white text-lg">Press the Keys in order and press the [Submit] button</p>
          <div className="mt-[15px] w-[150px]">
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
        </div>
        <div className="flex flex-col items-center">
          <div className="text-white mb-5">{remoconInput.join(',')}</div>
          <div className="flex">
            <button
              type="button"
              className="bg-[#00B1FF] w-[132px] h-[48px] mr-3 text-white rounded-3xl"
              ref={firstFocusableElementRef}
              onClick={() => {
                postCustomKeyMutate({
                  newCustomKey: { name: remoconInput.join(','), custom_code: remoconInput, remocon_name: remocon.name },
                })
                setRemoconInput([])
                close()
              }}
            >
              Submit
            </button>
            <button
              type="button"
              className="bg-[#8F949E] w-[132px] h-[48px] text-white rounded-3xl"
              ref={lastFocusableElementRef}
              onClick={() => {
                setRemoconInput([])
                close()
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AddCustomKeyModal

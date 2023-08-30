import Modal from '@global/ui/Modal'
import React, { useEffect, useRef, useState } from 'react'
import { Button, Input, Text } from '@global/ui'
import { useMutation, useQuery } from 'react-query'
import { getRemocon, postCustomKey } from '../../../api/func'
import { Remocon } from '../../../api/entity'

interface SaveCustomKeyModalProps {
  isOpen: boolean
  close: () => void
  remoconInput: string[]
  remocon: Remocon
}

const SaveCustomKeyModal: React.FC<SaveCustomKeyModalProps> = ({ isOpen, close, remoconInput, remocon }) => {
  /**
   * 최종적으로 추가할 new CustomKeyName
   */
  const [newCustomKeyName, setNewCustomKeyName] = useState<string>(remoconInput.toString())

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
    <Modal
      mode="center"
      isOpen={isOpen}
      close={() => {
        setNewCustomKeyName('')
        close()
      }}
    >
      <div className="w-[500px] h-[230px] flex flex-col bg-light-black rounded-[10px] p-6">
        <Text colorScheme="light" className="!text-2xl" weight="bold">
          Custom key
        </Text>
        <Input
          className="mt-6"
          value={newCustomKeyName}
          onChange={(e) => setNewCustomKeyName(e.target.value)}
          ref={firstFocusableElementRef}
        />
        <div className="flex justify-end mt-6">
          <Button
            colorScheme="primary"
            className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
            onClick={() => {
              postCustomKeyMutate({
                newCustomKey: { name: newCustomKeyName, custom_code: remoconInput, remocon_name: remocon.name },
              })
              close()
            }}
          >
            Save
          </Button>
          <Button
            colorScheme="grey"
            className="w-[132px] h-[48px] text-white rounded-3xl"
            ref={lastFocusableElementRef}
            onClick={() => {
              setNewCustomKeyName('')
              close()
            }}
          >
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default SaveCustomKeyModal

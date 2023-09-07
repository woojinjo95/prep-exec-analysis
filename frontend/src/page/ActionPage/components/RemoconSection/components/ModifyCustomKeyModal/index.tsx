import React, { useEffect, useRef, useState } from 'react'
import { Button, Input, Modal } from '@global/ui'
import { useMutation, useQuery } from 'react-query'
import { getRemocon, postCustomKey, putCustomKey } from '../../api/func'
import { CustomKey, Remocon } from '../../api/entity'

interface ModifyCustomKeyModalProps {
  isOpen: boolean
  close: () => void
  customKey: CustomKey
  remocon: Remocon
}

const ModifyCustomKeyModal: React.FC<ModifyCustomKeyModalProps> = ({ isOpen, close, customKey, remocon }) => {
  /**
   * 최종적으로 수정할 new CustomKeyName
   */
  const [newCustomKeyName, setNewCustomKeyName] = useState<string>(customKey.name)

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

  const { mutate: putCustomKeyMutate } = useMutation(putCustomKey, {
    onSuccess: () => {
      refetch()
    },
    onError: (err) => {
      console.error(err)
    },
  })

  return (
    <Modal
      isOpen={isOpen}
      close={() => {
        setNewCustomKeyName('')
        close()
      }}
      className="w-[500px] h-[230px]"
      title="Custom key"
    >
      <div className="flex flex-col">
        <Input
          value={newCustomKeyName}
          onChange={(e) => setNewCustomKeyName(e.target.value)}
          ref={firstFocusableElementRef}
        />
        <div className="flex justify-end mt-6">
          <Button
            colorScheme="primary"
            className="w-[132px] h-[48px] mr-3 text-white rounded-3xl"
            onClick={() => {
              putCustomKeyMutate({
                remocon_name: remocon.name,
                custom_key_id: customKey.id,
                newCustomKey: { name: newCustomKeyName, custom_code: customKey.custom_code, id: customKey.id },
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

export default ModifyCustomKeyModal

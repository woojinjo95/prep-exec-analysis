import Modal from '@global/ui/Modal'
import React, { useEffect, useRef, useState } from 'react'
import { Input, Text } from '@global/ui'

interface SaveBlocksModalProps {
  isOpen: boolean
  close: () => void
}

const SaveBlocksModal: React.FC<SaveBlocksModalProps> = ({ isOpen, close }) => {
  const firstFocusableElementRef = useRef<HTMLInputElement>(null)
  const lastFocusableElementRef = useRef<HTMLButtonElement>(null)

  const [blocksName, setBlocksName] = useState<string>('')

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
  return (
    <Modal
      mode="center"
      isOpen={isOpen}
      close={() => {
        close()
      }}
    >
      <div className="h-[90%] w-[1140px] flex flex-col bg-light-black rounded-[10px] p-6">
        <Text colorScheme="light" className="!text-2xl mb-5" weight="bold">
          Save Blocks
        </Text>
        <div className="w-full grid grid-cols-[1fr_6fr] items-center h-12 mb-4">
          <Text colorScheme="light" className="!text-lg " weight="bold">
            Name
          </Text>
          <Input value={blocksName} onChange={(e) => setBlocksName(e.target.value)} ref={firstFocusableElementRef} />
        </div>
        <div className="w-full grid grid-cols-[1fr_6fr] items-center h-12">
          <Text colorScheme="light" className="!text-lg " weight="bold">
            Tag
          </Text>
          <Input value={blocksName} onChange={(e) => setBlocksName(e.target.value)} ref={firstFocusableElementRef} />
        </div>
      </div>
    </Modal>
  )
}

export default SaveBlocksModal

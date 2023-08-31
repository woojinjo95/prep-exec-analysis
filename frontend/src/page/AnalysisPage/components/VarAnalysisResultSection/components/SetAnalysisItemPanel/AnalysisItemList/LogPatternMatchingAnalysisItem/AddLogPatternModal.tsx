import React from 'react'
import { Button, ColorPickerBox, Input, Modal, Title } from '@global/ui'

interface AddLogPatternModalProps {
  isOpen: boolean
  close: () => void
}

/**
 * 로그 패턴 추가 모달
 *
 * TODO:
 */
const AddLogPatternModal: React.FC<AddLogPatternModalProps> = ({ isOpen, close }) => {
  return (
    <Modal
      isOpen={isOpen}
      close={close}
      title="Add Log Pattern"
      className="w-[60vw] h-[60vh] min-h-[600px] min-w-[960px]"
    >
      <div className="w-full h-full grid grid-cols-[auto_1fr] grid-rows-[auto_auto_1fr_auto_auto] gap-x-10 gap-y-3">
        <Title as="h3" colorScheme="light" className="pt-3">
          Log Pattern Name
        </Title>
        <div className="flex">
          <Input placeholder="Untitled Log Pattern" />
        </div>

        <Title as="h3" colorScheme="light" className="pt-3">
          Log Level
        </Title>
        <div className="flex">
          <Input />
        </div>

        <Title as="h3" colorScheme="light" className="pt-3">
          Regular Expression
        </Title>
        <div />

        <div>
          <Title as="h3" colorScheme="light">
            Color
          </Title>
        </div>
        <div className="flex items-center">
          <ColorPickerBox color="red" />
        </div>

        <div className="col-span-2 flex justify-end items-center gap-x-3">
          <Button colorScheme="primary">Save</Button>
          <Button colorScheme="grey">Cancel</Button>
        </div>
      </div>
    </Modal>
  )
}

export default AddLogPatternModal

import React from 'react'
import { Modal } from '@global/ui'

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
    <Modal isOpen={isOpen} close={close} title="Add Log Pattern">
      <div>hi</div>
    </Modal>
  )
}

export default AddLogPatternModal

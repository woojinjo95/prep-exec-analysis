import React from 'react'
import { Button, useDisclosure } from '@chakra-ui/react'
import SetROIModal from './SetROIModal'

/**
 * ROI 설정 버튼 및 모달
 */
const SetROIButton: React.FC = () => {
  const { isOpen, onClose, onOpen } = useDisclosure()

  return (
    <>
      <Button onClick={onOpen}>Set ROI</Button>
      <SetROIModal isOpen={isOpen} onClose={onClose} />
    </>
  )
}

export default SetROIButton

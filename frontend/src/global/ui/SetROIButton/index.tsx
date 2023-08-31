import React, { useState } from 'react'
import SetROIModal from './SetROIModal'
import { Button } from '..'

/**
 * ROI 설정 버튼 및 모달
 */
const SetROIButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false)

  return (
    <>
      <Button colorScheme="charcoal" className="w-[132px]" onClick={() => setIsOpen(true)}>
        Add
      </Button>
      <SetROIModal isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  )
}

export default SetROIButton

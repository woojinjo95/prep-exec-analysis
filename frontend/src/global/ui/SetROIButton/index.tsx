import React, { useState } from 'react'
import { AnalysisFrame } from '@global/api/entity'
import SetROIModal from './SetROIModal'
import { Button } from '..'

interface SetROIButtonProps {
  onSave: (frame: AnalysisFrame) => void
  defaultFrame?: AnalysisFrame
}

/**
 * ROI 설정 버튼 및 모달
 */
const SetROIButton: React.FC<SetROIButtonProps> = ({ onSave, defaultFrame }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false)

  return (
    <>
      <Button colorScheme="charcoal" className="w-[132px]" onClick={() => setIsOpen(true)}>
        {defaultFrame !== undefined ? 'Modify' : 'Add'}
      </Button>
      <SetROIModal isOpen={isOpen} onClose={() => setIsOpen(false)} onSave={onSave} defaultFrame={defaultFrame} />
    </>
  )
}

export default SetROIButton

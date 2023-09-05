import React, { useState } from 'react'
import { AnalysisFrame } from '@global/api/entity'
import SetROIModal from './SetROIModal'
import { Button } from '..'

interface SetROIButtonProps {
  onSave: (frame: AnalysisFrame) => void
  defaultCurrentTime?: number
  defaultROI?: AnalysisFrame['roi']
}

/**
 * ROI 설정 버튼 및 모달
 */
const SetROIButton: React.FC<SetROIButtonProps> = ({ onSave, defaultCurrentTime, defaultROI }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false)

  return (
    <>
      <Button colorScheme="charcoal" className="w-[132px]" onClick={() => setIsOpen(true)}>
        {defaultCurrentTime !== undefined && defaultROI !== undefined ? 'Modify' : 'Add'}
      </Button>
      <SetROIModal
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        onSave={onSave}
        defaultCurrentTime={defaultCurrentTime}
        defaultROI={defaultROI}
      />
    </>
  )
}

export default SetROIButton

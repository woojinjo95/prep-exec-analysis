import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../../constant'

interface ResumeAnalysisItemProps {
  onClickDeleteItem: () => void
}

/**
 * resume 분석 아이템
 */
const ResumeAnalysisItem: React.FC<ResumeAnalysisItemProps> = ({ onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.resume}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div />
    </Accordion>
  )
}

export default ResumeAnalysisItem

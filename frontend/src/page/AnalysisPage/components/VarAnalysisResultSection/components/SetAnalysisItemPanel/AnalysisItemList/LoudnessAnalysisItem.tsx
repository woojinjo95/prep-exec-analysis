import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'

interface LoudnessAnalysisItemProps {
  onClickDeleteItem: () => void
}

/**
 * loudness 분석 아이템
 */
const LoudnessAnalysisItem: React.FC<LoudnessAnalysisItemProps> = ({ onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.loudness}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    />
  )
}

export default LoudnessAnalysisItem

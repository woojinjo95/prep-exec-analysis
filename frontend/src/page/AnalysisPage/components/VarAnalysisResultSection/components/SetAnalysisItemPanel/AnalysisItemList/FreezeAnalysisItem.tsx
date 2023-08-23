import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'

interface FreezeAnalysisItemProps {
  onClickDeleteItem: () => void
}

/**
 * freeze 분석 아이템
 */
const FreezeAnalysisItem: React.FC<FreezeAnalysisItemProps> = ({ onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.freeze}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div>hi</div>
    </Accordion>
  )
}

export default FreezeAnalysisItem

import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'

interface BootAnalysisItemProps {
  onClickDeleteItem: () => void
}

/**
 * boot 분석 아이템
 */
const BootAnalysisItem: React.FC<BootAnalysisItemProps> = ({ onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.boot}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    />
  )
}

export default BootAnalysisItem

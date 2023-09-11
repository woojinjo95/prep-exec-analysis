import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'

interface IntelligentMonkeyTestAnalysisItemProps {
  onClickDeleteItem: React.MouseEventHandler<SVGSVGElement>
}

/**
 * Intelligent Monkey Test 분석 아이템
 */
const IntelligentMonkeyTestAnalysisItem: React.FC<IntelligentMonkeyTestAnalysisItemProps> = ({ onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.intelligent_monkey_test}
          </Text>

          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    />
  )
}

export default IntelligentMonkeyTestAnalysisItem

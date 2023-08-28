import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../../constant'

interface LogPatternMatchingAnalysisItemProps {
  onClickDeleteItem: () => void
}

/**
 * log pattern matching 분석 아이템
 */
const LogPatternMatchingAnalysisItem: React.FC<LogPatternMatchingAnalysisItemProps> = ({ onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.log_pattern_matching}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    />
  )
}

export default LogPatternMatchingAnalysisItem

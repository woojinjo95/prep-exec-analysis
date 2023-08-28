import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../../constant'

interface LogLevelFinderAnalysisItemProps {
  onClickDeleteItem: () => void
}

/**
 * log level finder 분석 아이템
 */
const LogLevelFinderAnalysisItem: React.FC<LogLevelFinderAnalysisItemProps> = ({ onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.log_level_finder}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    />
  )
}

export default LogLevelFinderAnalysisItem

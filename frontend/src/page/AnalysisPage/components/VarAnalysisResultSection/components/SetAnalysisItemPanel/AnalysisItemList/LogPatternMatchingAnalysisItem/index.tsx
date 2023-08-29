import React, { useState } from 'react'
import { Accordion, Button, Checkbox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { UnsavedAnalysisConfig } from '@page/AnalysisPage/components/VarAnalysisResultSection/types'
import { AnalysisTypeLabel } from '../../../../constant'
import LogPattern from './LogPattern'

interface LogPatternMatchingAnalysisItemProps {
  onClickDeleteItem: () => void
  patterns: NonNullable<UnsavedAnalysisConfig['log_pattern_matching']>['items']
}

/**
 * log pattern matching 분석 아이템
 */
const LogPatternMatchingAnalysisItem: React.FC<LogPatternMatchingAnalysisItemProps> = ({
  onClickDeleteItem,
  patterns,
}) => {
  const [isRememberChecked, setIsRememberChecked] = useState<boolean>(false)

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
    >
      <div>
        <div className="grid grid-cols-1 gap-y-4 pt-2">
          {patterns.map((pattern, index) => (
            <LogPattern key={`log-pattern-matching-analysis-item-${index}`} logPattern={pattern} />
          ))}
        </div>

        <Button className="w-full mt-6 mb-4">Add Log Pattern</Button>

        {/* TODO: local storage에 저장 */}
        <Checkbox
          colorScheme="light"
          isChecked={isRememberChecked}
          label="Remember current settings"
          onClick={(isChecked) => setIsRememberChecked(isChecked)}
        />
      </div>
    </Accordion>
  )
}

export default LogPatternMatchingAnalysisItem

import React, { useState } from 'react'
import { Accordion, Button, Checkbox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { UnsavedAnalysisConfig } from '@page/AnalysisPage/components/VarAnalysisResultSection/types'
import { AnalysisType } from '@global/constant'
import { AnalysisTypeLabel } from '../../../../constant'
import LogPattern from './LogPattern'
import LogPatternModal from './LogPatternModal'

interface LogPatternMatchingAnalysisItemProps {
  patterns: NonNullable<UnsavedAnalysisConfig['log_pattern_matching']>['items']
  warningMessage?: string
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
  onClickDeleteItem: React.MouseEventHandler<SVGSVGElement>
  isRememberChecked: boolean
  setIsRememberedConfig: React.Dispatch<React.SetStateAction<{ [key in keyof typeof AnalysisType]?: boolean }>>
}

/**
 * log pattern matching 분석 아이템
 */
const LogPatternMatchingAnalysisItem: React.FC<LogPatternMatchingAnalysisItemProps> = ({
  patterns,
  warningMessage,
  setUnsavedAnalysisConfig,
  onClickDeleteItem,
  isRememberChecked,
  setIsRememberedConfig,
}) => {
  const [isOpenAddLogPatternModal, setIsOpenAddLogPatternModal] = useState<boolean>(false)

  return (
    <Accordion
      warningMessage={warningMessage}
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
            <LogPattern
              key={`log-pattern-matching-analysis-item-${index}`}
              logPattern={pattern}
              patterns={patterns}
              setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
            />
          ))}
        </div>

        <Button className="w-full mt-6 mb-4" onClick={() => setIsOpenAddLogPatternModal(true)}>
          Add Log Pattern
        </Button>

        <Checkbox
          colorScheme="light"
          isChecked={isRememberChecked}
          label="Remember current settings"
          onClick={(isChecked) => setIsRememberedConfig((prev) => ({ ...prev, log_pattern_matching: isChecked }))}
        />

        {!!warningMessage && (
          <div className="pt-2">
            <Text colorScheme="orange">{warningMessage}</Text>
          </div>
        )}

        {isOpenAddLogPatternModal && (
          <LogPatternModal
            isOpen={isOpenAddLogPatternModal}
            close={() => setIsOpenAddLogPatternModal(false)}
            patterns={patterns}
            setUnsavedAnalysisConfig={setUnsavedAnalysisConfig}
          />
        )}
      </div>
    </Accordion>
  )
}

export default LogPatternMatchingAnalysisItem

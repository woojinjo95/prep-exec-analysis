import React, { useState } from 'react'
import { Accordion, Button, Checkbox, ColorPickerBox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { UnsavedAnalysisConfig } from '@page/AnalysisPage/components/VarAnalysisResultSection/types'
import { AnalysisType, AnalysisTypeLabel } from '@global/constant'
import LogPattern from './LogPattern'
import LogPatternModal from './LogPatternModal'

interface LogPatternMatchingAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['log_pattern_matching']>['color']
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
  color,
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
          <div className="flex items-center gap-x-3">
            <ColorPickerBox
              color={color}
              onChange={(newColor) => {
                setUnsavedAnalysisConfig((prev) => ({
                  ...prev,
                  log_pattern_matching: {
                    ...prev.log_pattern_matching!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.log_pattern_matching}
            </Text>
          </div>

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

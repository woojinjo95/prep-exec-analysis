import React from 'react'
import { Accordion, Checkbox, ColorPickerBox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { LogLevel } from '@global/constant'
import { AnalysisTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

interface LogLevelFinderAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['log_level_finder']>['color']
  targets: NonNullable<UnsavedAnalysisConfig['log_level_finder']>['targets']
  warningMessage?: string
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * log level finder 분석 아이템
 */
const LogLevelFinderAnalysisItem: React.FC<LogLevelFinderAnalysisItemProps> = ({
  color,
  targets,
  warningMessage,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
}) => {
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
                  log_level_finder: {
                    ...prev.log_level_finder!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.log_level_finder}
            </Text>
          </div>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="flex justify-between pt-2">
        <Text colorScheme="light" weight="medium">
          Target
        </Text>

        <div className="grid grid-cols-3 grid-rows-2 gap-x-6 gap-y-4">
          {Object.keys(LogLevel).map((_level) => {
            const level = _level as NonNullable<typeof targets>[number]
            return (
              <Checkbox
                key={`log-level-finder-analysis-item-${level}`}
                colorScheme="light"
                label={`Logcat ${level}`}
                isChecked={targets.includes(level)}
                onClick={(isChecked) => {
                  setUnsavedAnalysisConfig((prev) => ({
                    ...prev,
                    log_level_finder: {
                      ...prev.log_level_finder!,
                      targets: isChecked
                        ? [...(prev.log_level_finder?.targets || []), level]
                        : prev.log_level_finder?.targets.filter((l) => l !== level) || [],
                    },
                  }))
                }}
              />
            )
          })}
        </div>
      </div>

      {!!warningMessage && (
        <div className="pt-2">
          <Text colorScheme="orange">{warningMessage}</Text>
        </div>
      )}
    </Accordion>
  )
}

export default LogLevelFinderAnalysisItem

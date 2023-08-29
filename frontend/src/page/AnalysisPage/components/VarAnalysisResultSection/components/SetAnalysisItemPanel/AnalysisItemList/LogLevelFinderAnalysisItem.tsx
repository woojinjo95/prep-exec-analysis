import React from 'react'
import { Accordion, Checkbox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import LogLevel from '@global/constant/logLevel'
import { AnalysisTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

interface LogLevelFinderAnalysisItemProps {
  targets: NonNullable<UnsavedAnalysisConfig['log_level_finder']>['targets']
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * log level finder 분석 아이템
 */
const LogLevelFinderAnalysisItem: React.FC<LogLevelFinderAnalysisItemProps> = ({
  targets,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
}) => {
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
    </Accordion>
  )
}

export default LogLevelFinderAnalysisItem

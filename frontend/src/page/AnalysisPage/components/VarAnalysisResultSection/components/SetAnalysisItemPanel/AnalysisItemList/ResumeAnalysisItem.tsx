import React from 'react'
import { Accordion, ColorPickerBox, OptionItem, Select, SetROIButton, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { ReactComponent as ISValidIcon } from '@assets/images/icon_Is_valid.svg'
import { AnalysisTypeLabel, ResumeTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

interface ResumeAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['resume']>['color']
  frame: NonNullable<UnsavedAnalysisConfig['resume']>['frame']
  resumeType: NonNullable<UnsavedAnalysisConfig['resume']>['type']
  warningMessage?: string
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * resume 분석 아이템
 */
const ResumeAnalysisItem: React.FC<ResumeAnalysisItemProps> = ({
  color,
  frame,
  resumeType,
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
                  resume: {
                    ...prev.resume!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.resume}
            </Text>
          </div>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="flex flex-col w-full gap-y-4">
        <div className="grid grid-rows-1 grid-cols-2 items-center">
          <Text colorScheme="light" weight="medium">
            Type
          </Text>

          <Select
            header={
              <Text weight="bold" colorScheme="light">
                {ResumeTypeLabel[resumeType]}
              </Text>
            }
          >
            {Object.keys(ResumeTypeLabel).map((_type) => {
              const type = _type as keyof typeof ResumeTypeLabel

              return (
                <OptionItem
                  key={`resume-analysis-item-${type}`}
                  onClick={() => {
                    setUnsavedAnalysisConfig((prev) => ({
                      ...prev,
                      resume: { ...prev.resume!, type, frame: undefined },
                    }))
                  }}
                  isActive={type === resumeType}
                >
                  {ResumeTypeLabel[type]}
                </OptionItem>
              )
            })}
          </Select>
        </div>

        {resumeType === 'image_matching' && (
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-x-2">
              <Text colorScheme="light" weight="medium">
                Set ROI
              </Text>
              {!!frame && <ISValidIcon className="w-5 h-5" />}
            </div>

            <SetROIButton
              defaultCurrentTime={frame?.relative_time}
              defaultROI={frame?.roi}
              onSave={(frame) => {
                setUnsavedAnalysisConfig((prev) => ({
                  ...prev,
                  resume: {
                    ...prev.resume!,
                    frame,
                  },
                }))
              }}
            />
          </div>
        )}

        {!!warningMessage && (
          <div className="pt-2">
            <Text colorScheme="orange">{warningMessage}</Text>
          </div>
        )}
      </div>
    </Accordion>
  )
}

export default ResumeAnalysisItem

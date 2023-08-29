import React from 'react'
import { Accordion, ColorPickerBox, OptionItem, Select, SetROIButton, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'
import { AnalysisConfig } from '../../../api/entity'
import { UnsavedAnalysisConfig } from '../../../types'

type ResumeType = NonNullable<AnalysisConfig['resume']>['type']

const ResumeTypeLabel: { [key in ResumeType]: string } = {
  image_matching: 'Image Matching',
  screen_change_rate: 'Screen Change Rate',
} as const

interface ResumeAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['resume']>['color']
  resumeType: NonNullable<UnsavedAnalysisConfig['resume']>['type']
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * resume 분석 아이템
 */
const ResumeAnalysisItem: React.FC<ResumeAnalysisItemProps> = ({
  color,
  resumeType,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
}) => {
  return (
    <Accordion
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

          <Select value={ResumeTypeLabel[resumeType]}>
            {Object.keys(ResumeTypeLabel).map((_type) => {
              const type = _type as keyof typeof ResumeTypeLabel

              return (
                <OptionItem
                  key={`resume-analysis-item-${type}`}
                  onClick={() => {
                    setUnsavedAnalysisConfig((prev) => ({
                      ...prev,
                      resume: { ...prev.resume!, type },
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
            <Text colorScheme="light" weight="medium">
              Set ROI
            </Text>

            <SetROIButton />
          </div>
        )}
      </div>
    </Accordion>
  )
}

export default ResumeAnalysisItem

import React, { useEffect } from 'react'
import { Accordion, OptionItem, Select, SetROIButton, Text } from '@global/ui'
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
  resumeType: NonNullable<UnsavedAnalysisConfig['resume']>['type']
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * resume 분석 아이템
 */
const ResumeAnalysisItem: React.FC<ResumeAnalysisItemProps> = ({
  resumeType,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
}) => {
  useEffect(() => {
    if (!resumeType) {
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        resume: {
          ...prev.resume,
          type: 'image_matching',
        },
      }))
    }
  }, [resumeType])

  console.log(resumeType)

  if (!resumeType) return <div />
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.resume}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="grid grid-rows-2 grid-cols-1 gap-y-4">
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
                      resume: { ...prev.resume, type },
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

        <div className="flex justify-between items-center">
          <Text colorScheme="light" weight="medium">
            Set ROI
          </Text>

          <SetROIButton />
        </div>
      </div>
    </Accordion>
  )
}

export default ResumeAnalysisItem

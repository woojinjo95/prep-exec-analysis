import React from 'react'
import { Accordion, SetROIButton, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'
import { AnalysisConfig } from '../../../api/entity'
import { UnsavedAnalysisConfig } from '../../../types'

const BootTypeLabel: { [key in NonNullable<AnalysisConfig['boot']>['type']]: string } = {
  image_matching: 'Image Matching',
} as const

interface BootAnalysisItemProps {
  bootType: NonNullable<UnsavedAnalysisConfig['boot']>['type']
  onClickDeleteItem: () => void
}

/**
 * boot 분석 아이템
 */
const BootAnalysisItem: React.FC<BootAnalysisItemProps> = ({ bootType, onClickDeleteItem }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.boot}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="flex flex-col gap-y-6 pt-4">
        <div className="flex justify-between items-center">
          <Text colorScheme="light" weight="medium">
            Type
          </Text>

          <Text size="sm" weight="medium">
            {BootTypeLabel[bootType]}
          </Text>
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

export default BootAnalysisItem

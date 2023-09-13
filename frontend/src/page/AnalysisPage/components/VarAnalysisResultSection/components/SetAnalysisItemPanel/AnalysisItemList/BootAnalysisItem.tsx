import React from 'react'
import { Accordion, ColorPickerBox, SetROIButton, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { ReactComponent as ISValidIcon } from '@assets/images/icon_Is_valid.svg'
import { AnalysisTypeLabel, BootTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

interface BootAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['boot']>['color']
  frame: NonNullable<UnsavedAnalysisConfig['boot']>['frame']
  bootType: NonNullable<UnsavedAnalysisConfig['boot']>['type']
  warningMessage?: string
  onClickDeleteItem: React.MouseEventHandler<SVGSVGElement>
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * boot 분석 아이템
 */
const BootAnalysisItem: React.FC<BootAnalysisItemProps> = ({
  color,
  frame,
  bootType,
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
                  boot: {
                    ...prev.boot!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.boot}
            </Text>
          </div>
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
          <div className="flex items-center gap-x-2">
            <Text colorScheme="light" weight="medium">
              Set ROI
            </Text>
            {!!frame && <ISValidIcon className="w-5 h-5" />}
          </div>

          <SetROIButton
            defaultFrame={frame}
            onSave={(frame) => {
              setUnsavedAnalysisConfig((prev) => ({
                ...prev,
                boot: {
                  ...prev.boot!,
                  frame,
                },
              }))
            }}
          />
        </div>
      </div>
    </Accordion>
  )
}

export default BootAnalysisItem

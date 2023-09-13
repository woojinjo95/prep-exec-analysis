import React from 'react'
import { Accordion, ColorPickerBox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '@global/constant'
import { UnsavedAnalysisConfig } from '../../../types'

interface MonkeyTestAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['monkey_test']>['color']
  onClickDeleteItem: React.MouseEventHandler<SVGSVGElement>
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * Monkey Test 분석 아이템
 */
const MonkeyTestAnalysisItem: React.FC<MonkeyTestAnalysisItemProps> = ({
  color,
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
                  monkey_test: {
                    ...prev.monkey_test!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.monkey_test}
            </Text>
          </div>

          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    />
  )
}

export default MonkeyTestAnalysisItem

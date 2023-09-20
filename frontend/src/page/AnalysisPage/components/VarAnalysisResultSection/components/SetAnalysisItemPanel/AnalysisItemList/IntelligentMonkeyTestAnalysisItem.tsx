import React from 'react'
import { Accordion, ColorPickerBox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '@global/constant'
import { UnsavedAnalysisConfig } from '../../../types'

interface IntelligentMonkeyTestAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['intelligent_monkey_test']>['color']
  onClickDeleteItem: React.MouseEventHandler<SVGSVGElement>
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * Intelligent Monkey Test 분석 아이템
 */
const IntelligentMonkeyTestAnalysisItem: React.FC<IntelligentMonkeyTestAnalysisItemProps> = ({
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
                  intelligent_monkey_test: {
                    ...prev.intelligent_monkey_test!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.intelligent_monkey_test}
            </Text>
          </div>

          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    />
  )
}

export default IntelligentMonkeyTestAnalysisItem

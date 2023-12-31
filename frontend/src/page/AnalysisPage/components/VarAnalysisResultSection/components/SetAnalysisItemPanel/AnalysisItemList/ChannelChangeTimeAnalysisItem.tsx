import React from 'react'
import { Accordion, Checkbox, ColorPickerBox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '@global/constant'
import { UnsavedAnalysisConfig } from '../../../types'

const ChannelChangeTargetLabel: {
  [key in NonNullable<UnsavedAnalysisConfig['channel_change_time']>['targets'][number]]: string
} = {
  adjoint_channel: 'Adjoint Channel',
  nonadjoint_channel: 'Nonadjoint Channel',
} as const

interface ChannelChangeTimeAnalysisItemProps {
  color: NonNullable<UnsavedAnalysisConfig['channel_change_time']>['color']
  targets: NonNullable<UnsavedAnalysisConfig['channel_change_time']>['targets']
  onClickDeleteItem: React.MouseEventHandler<SVGSVGElement>
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * channel change time 분석 아이템
 */
const ChannelChangeTimeAnalysisItem: React.FC<ChannelChangeTimeAnalysisItemProps> = ({
  color,
  targets,
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
                  channel_change_time: {
                    ...prev.channel_change_time!,
                    color: newColor,
                  },
                }))
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.channel_change_time}
            </Text>
          </div>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="flex justify-between items-center pt-2">
        <Text colorScheme="light" weight="medium">
          Target
        </Text>

        <div className="flex items-center justify-end gap-x-4">
          {Object.keys(ChannelChangeTargetLabel).map((_target) => {
            const target = _target as NonNullable<typeof targets>[number]

            return (
              <Checkbox
                key={`channel-change-itme-analysis-item-${target}`}
                colorScheme="light"
                label={ChannelChangeTargetLabel[target]}
                isChecked={targets.includes(target)}
                onClick={(isChecked) => {
                  setUnsavedAnalysisConfig((prev) => ({
                    ...prev,
                    channel_change_time: {
                      ...prev.channel_change_time!,
                      targets: isChecked
                        ? [...(prev.channel_change_time?.targets || []), target]
                        : prev.channel_change_time?.targets.filter((t) => t !== target) || [],
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

export default ChannelChangeTimeAnalysisItem

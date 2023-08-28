import React, { useCallback } from 'react'
import { Accordion, Checkbox, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'
import { UnsavedAnalysisConfig } from '../../../types'

interface ChannelChangeTimeAnalysisItemProps {
  isCheckedAdjointChannel?: boolean
  isCheckedNonadjointChannel?: boolean
  onClickDeleteItem: () => void
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * channel change time 분석 아이템
 */
const ChannelChangeTimeAnalysisItem: React.FC<ChannelChangeTimeAnalysisItemProps> = ({
  isCheckedAdjointChannel,
  isCheckedNonadjointChannel,
  onClickDeleteItem,
  setUnsavedAnalysisConfig,
}) => {
  const onClickCheckbox = useCallback(
    (target: 'adjoint_channel' | 'nonadjoint_channel') => (isChecked: boolean) => {
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        channel_change_time: {
          ...prev.channel_change_time,
          targets: isChecked
            ? [...(prev.channel_change_time?.targets || []), target]
            : prev.channel_change_time?.targets?.filter((t) => t !== target),
        },
      }))
    },
    [],
  )

  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <Text size="sm" weight="medium">
            {AnalysisTypeLabel.channel_change_time}
          </Text>
          <TrashIcon className="w-4 fill-white" onClick={onClickDeleteItem} />
        </div>
      }
    >
      <div className="flex justify-between items-center pt-2">
        <Text colorScheme="light" weight="medium">
          Target
        </Text>

        <div className="flex items-center justify-end gap-x-4">
          <Checkbox
            colorScheme="light"
            label="Adjoint Channel"
            isChecked={isCheckedAdjointChannel || false}
            onClick={onClickCheckbox('adjoint_channel')}
          />
          <Checkbox
            colorScheme="light"
            label="Nondjoint Channel"
            isChecked={isCheckedNonadjointChannel || false}
            onClick={onClickCheckbox('nonadjoint_channel')}
          />
        </div>
      </div>
    </Accordion>
  )
}

export default ChannelChangeTimeAnalysisItem

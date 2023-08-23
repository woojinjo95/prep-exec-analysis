import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as TrashIcon } from '@assets/images/icon_trash.svg'
import { AnalysisTypeLabel } from '../../../constant'

interface ChannelChangeTimeAnalysisItemProps {
  onClickDeleteItem: () => void
}

/**
 * channel change time 분석 아이템
 */
const ChannelChangeTimeAnalysisItem: React.FC<ChannelChangeTimeAnalysisItemProps> = ({ onClickDeleteItem }) => {
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
    />
  )
}

export default ChannelChangeTimeAnalysisItem
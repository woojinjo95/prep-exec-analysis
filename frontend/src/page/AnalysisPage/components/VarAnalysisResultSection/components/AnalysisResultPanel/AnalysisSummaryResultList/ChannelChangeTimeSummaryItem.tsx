import React from 'react'
import { Accordion, SimpleButton, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { AnalysisTypeLabel } from '../../../constant'

/**
 * channel change time 분석결과 요약 아이템
 */
const ChannelChangeTimeSummaryItem: React.FC = () => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                // TODO:
                backgroundColor: 'white',
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.channel_change_time}
            </Text>
          </div>

          <Text weight="medium">times</Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto_auto] gap-x-4 gap-y-1 items-center">
          {/* header */}
          <Text weight="medium" size="sm">
            Target
          </Text>
          <Text weight="medium" size="sm">
            Total
          </Text>
          <Text weight="medium" size="sm" className="ml-4">
            Avg Time
          </Text>
          <div />

          {/* TODO: items */}
          <Text size="sm">Adjoint</Text>
          <Text size="sm" className="text-right">
            2
          </Text>
          <Text size="sm" className="text-right">
            869ms
          </Text>
          <SimpleButton colorScheme="charcoal" isIcon>
            <ShowEyeIcon className="w-5" />
          </SimpleButton>

          <Text size="sm">Nonadjoint</Text>
          <Text size="sm" className="text-right">
            2
          </Text>
          <Text size="sm" className="text-right">
            1,021ms
          </Text>
          <button type="button">
            <HiddenEyeIcon className="w-5" />
          </button>
        </div>

        <SimpleButton colorScheme="charcoal" className="ml-auto">
          <ShowRawDataIcon className="w-4 h-4" />
          <Text colorScheme="light" weight="medium">
            Show Raw Data
          </Text>
        </SimpleButton>
      </div>
    </Accordion>
  )
}

export default ChannelChangeTimeSummaryItem

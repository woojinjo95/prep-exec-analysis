import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { AnalysisTypeLabel } from '../../../constant'

/**
 * log level finder 분석결과 요약 아이템
 */
const LogLevelFinderSummaryResultItem: React.FC = () => {
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
              {AnalysisTypeLabel.log_level_finder}
            </Text>
          </div>

          <Text weight="medium">times</Text>
        </div>
      }
    >
      <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 gap-y-2 pt-1">
        {/* header */}
        <Text weight="medium" size="sm">
          Target
        </Text>
        <Text weight="medium" size="sm">
          Total
        </Text>
        <div />

        {/* TODO: items */}
        <Text size="sm">Logcat F</Text>
        <Text size="sm" className="text-right">
          2
        </Text>
        <button type="button">
          <ShowEyeIcon className="w-5" />
        </button>

        <Text size="sm">Logcat E</Text>
        <Text size="sm" className="text-right">
          2
        </Text>
        <button type="button">
          <HiddenEyeIcon className="w-5" />
        </button>
      </div>
    </Accordion>
  )
}

export default LogLevelFinderSummaryResultItem

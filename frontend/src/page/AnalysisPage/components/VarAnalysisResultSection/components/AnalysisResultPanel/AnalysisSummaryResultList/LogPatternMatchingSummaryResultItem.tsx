import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { AnalysisTypeLabel } from '../../../constant'

/**
 * log pattern matching 분석 결과 아이템
 */
const LogPatternMatchingSummaryResultItem: React.FC = () => {
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
              {AnalysisTypeLabel.log_pattern_matching}
            </Text>
          </div>

          <Text weight="medium">times</Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 gap-y-2">
          {/* header */}
          <Text weight="medium" size="sm">
            Log Pattern Name
          </Text>
          <Text weight="medium" size="sm">
            Total
          </Text>
          <div />

          {/* TODO: items */}
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: 'red',
              }}
            />
            <Text size="sm">Untitled Log Pattren (1)</Text>
          </div>
          <Text size="sm" className="text-right">
            2
          </Text>
          <button type="button">
            <ShowEyeIcon className="w-5" />
          </button>

          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: 'red',
              }}
            />
            <Text size="sm">Untitled Log Pattren (2)</Text>
          </div>
          <Text size="sm" className="text-right">
            2
          </Text>
          <button type="button">
            <HiddenEyeIcon className="w-5" />
          </button>
        </div>

        <button type="button" className="flex justify-end items-center gap-x-3">
          {/* TODO: open raw data modal */}
          <ShowRawDataIcon className="w-4 h-4" />
          <Text>Show Raw Data</Text>
        </button>
      </div>
    </Accordion>
  )
}

export default LogPatternMatchingSummaryResultItem

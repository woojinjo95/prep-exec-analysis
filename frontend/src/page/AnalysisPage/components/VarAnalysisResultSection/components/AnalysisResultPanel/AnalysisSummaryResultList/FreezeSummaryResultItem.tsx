/* eslint-disable react/jsx-no-useless-fragment */
import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { AnalysisTypeLabel } from '../../../constant'

/**
 * freeze 분석결과 요약 아이템
 */
const FreezeSummaryResultItem: React.FC = () => {
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
              {AnalysisTypeLabel.freeze}
            </Text>
          </div>

          <Text>items</Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-5 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 gap-y-2">
          {/* header */}
          <Text weight="medium" size="sm">
            Error Type
          </Text>
          <Text weight="medium" size="sm">
            Total
          </Text>
          <div />

          {/* TODO: items */}
          <>
            <Text size="sm">Standard</Text>
            <Text size="sm" className="text-right">
              2
            </Text>
            <button type="button">
              <ShowEyeIcon className="w-5" />
            </button>
          </>

          <>
            <Text size="sm">Black</Text>
            <Text size="sm" className="text-right">
              2
            </Text>
            <button type="button">
              <HiddenEyeIcon className="w-5" />
            </button>
          </>
        </div>

        <div className="flex justify-end items-center gap-x-3">
          {/* TODO: open raw data modal */}
          <ShowRawDataIcon className="w-4 h-4" />
          <Text>Show Raw Data</Text>
        </div>
      </div>
    </Accordion>
  )
}

export default FreezeSummaryResultItem

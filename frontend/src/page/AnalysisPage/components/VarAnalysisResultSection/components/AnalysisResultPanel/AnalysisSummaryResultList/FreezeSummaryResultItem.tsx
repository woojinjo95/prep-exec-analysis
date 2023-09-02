import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
// import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { AnalysisTypeLabel, FreezeTypeLabel } from '../../../constant'
import { AnalysisResultSummary } from '../../../api/entity'

interface FreezeSummaryResultItemProps {
  results: NonNullable<AnalysisResultSummary['freeze']>
}

/**
 * freeze 분석결과 요약 아이템
 */
const FreezeSummaryResultItem: React.FC<FreezeSummaryResultItemProps> = ({ results }) => {
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

          <Text weight="medium">times</Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto] gap-x-4 gap-y-2">
          {/* header */}
          <Text weight="medium" size="sm">
            Error Type
          </Text>
          <Text weight="medium" size="sm">
            Total
          </Text>
          <div />

          {results.map(({ total, target }, index) => (
            <React.Fragment key={`freeze-summary-result-${index}`}>
              <Text size="sm">{FreezeTypeLabel[target]}</Text>
              <Text size="sm" className="text-right">
                {total}
              </Text>
              <button type="button">
                <ShowEyeIcon className="w-5" />
              </button>
            </React.Fragment>
          ))}
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

export default FreezeSummaryResultItem

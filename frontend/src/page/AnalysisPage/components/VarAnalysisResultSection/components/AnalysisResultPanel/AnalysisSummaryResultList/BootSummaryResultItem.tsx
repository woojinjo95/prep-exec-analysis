import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
// import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { numberWithCommas } from '@global/usecase'
import { AnalysisTypeLabel, BootTypeLabel } from '../../../constant'
import { AnalysisResultSummary } from '../../../api/entity'

interface BootSummaryResultItemProps {
  results: NonNullable<AnalysisResultSummary['boot']>
}

/**
 * boot 분석결과 요약 아이템
 */
const BootSummaryResultItem: React.FC<BootSummaryResultItemProps> = ({ results }) => {
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
              {AnalysisTypeLabel.boot}
            </Text>
          </div>

          <Text weight="medium">{numberWithCommas(results.reduce((acc, curr) => acc + curr.total, 0))} times</Text>
        </div>
      }
    >
      <div className="grid grid-cols-1 gap-y-4 pt-1">
        <div className="grid grid-cols-[1fr_auto_auto_auto] gap-x-4 gap-y-2">
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

          {results.map(({ total, target, avg_time }, index) => (
            <React.Fragment key={`boot-summary-result-item-${index}`}>
              <Text size="sm">{BootTypeLabel[target]}</Text>
              <Text size="sm" className="text-right">
                {numberWithCommas(total)}
              </Text>
              <Text size="sm" className="text-right">
                {numberWithCommas(avg_time)} ms
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

export default BootSummaryResultItem

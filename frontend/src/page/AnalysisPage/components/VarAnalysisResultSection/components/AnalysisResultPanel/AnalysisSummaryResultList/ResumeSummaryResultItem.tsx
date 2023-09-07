import React from 'react'
import { Accordion, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
// import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { numberWithCommas } from '@global/usecase'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { AnalysisTypeLabel, ResumeTypeLabel } from '../../../constant'

interface ResumeSummaryResultItemProps {
  resume: NonNullable<AnalysisResultSummary['resume']>
}

/**
 * resume 분석결과 요약 아이템
 */
const ResumeSummaryResultItem: React.FC<ResumeSummaryResultItemProps> = ({ resume }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: resume.color,
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.resume}
            </Text>
          </div>

          <Text weight="medium">
            {numberWithCommas(resume.results.reduce((acc, curr) => acc + curr.total, 0))} times
          </Text>
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

          {resume.results.map(({ total, target, avg_time }, index) => (
            <React.Fragment key={`resume-summary-result-${index}`}>
              <Text size="sm">{ResumeTypeLabel[target]}</Text>
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

export default ResumeSummaryResultItem

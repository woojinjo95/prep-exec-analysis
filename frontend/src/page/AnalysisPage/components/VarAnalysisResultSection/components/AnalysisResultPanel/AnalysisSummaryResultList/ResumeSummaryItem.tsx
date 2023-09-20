import React, { useEffect } from 'react'
import { useRecoilState } from 'recoil'
import { Accordion, SimpleButton, Text } from '@global/ui'
import { ReactComponent as ShowRawDataIcon } from '@assets/images/icon_raw_data.svg'
import { ReactComponent as ShowEyeIcon } from '@assets/images/icon_shown_w.svg'
import { ReactComponent as HiddenEyeIcon } from '@assets/images/icon_hidden.svg'
import { convertDuration, numberWithCommas } from '@global/usecase'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { resumeTypeFilterListState } from '@global/atom'
import { AnalysisTypeLabel } from '@global/constant'
import { ResumeTypeLabel } from '../../../constant'

interface ResumeSummaryItemProps {
  resume: NonNullable<AnalysisResultSummary['resume']>
  setRawDataModalType: React.Dispatch<React.SetStateAction<keyof AnalysisResultSummary | null>>
}

/**
 * resume 분석결과 요약 아이템
 */
const ResumeSummaryItem: React.FC<ResumeSummaryItemProps> = ({ resume, setRawDataModalType }) => {
  const [resumeTypeFilterList, setResumeTypeFilterList] = useRecoilState(resumeTypeFilterListState)

  useEffect(() => {
    setResumeTypeFilterList([])
  }, [])

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

          <Text size="sm" weight="medium">
            {numberWithCommas(resume.results.reduce((acc, curr) => acc + curr.total, 0))} times
          </Text>
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

          {resume.results.map(({ total, target, avg_time }, index) => (
            <React.Fragment key={`resume-summary-result-${index}`}>
              <Text size="sm">{ResumeTypeLabel[target]}</Text>
              <Text size="sm" className="text-right">
                {numberWithCommas(total)}
              </Text>
              <Text size="sm" className="text-right">
                {convertDuration(avg_time)}
              </Text>
              {resumeTypeFilterList.includes(target) ? (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() => setResumeTypeFilterList((prev) => prev.filter((type) => type !== target))}
                >
                  <HiddenEyeIcon className="h-4 w-5" />
                </SimpleButton>
              ) : (
                <SimpleButton
                  isIcon
                  colorScheme="charcoal"
                  onClick={() => setResumeTypeFilterList((prev) => [...prev, target])}
                >
                  <ShowEyeIcon className="h-4 w-5" />
                </SimpleButton>
              )}
            </React.Fragment>
          ))}
        </div>

        <SimpleButton colorScheme="charcoal" className="ml-auto" onClick={() => setRawDataModalType('resume')}>
          <ShowRawDataIcon className="w-4 h-4" />
          <Text colorScheme="light" weight="medium">
            Show Raw Data
          </Text>
        </SimpleButton>
      </div>
    </Accordion>
  )
}

export default ResumeSummaryItem

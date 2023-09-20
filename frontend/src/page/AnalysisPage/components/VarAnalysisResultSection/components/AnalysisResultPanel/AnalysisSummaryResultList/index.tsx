import React, { useState } from 'react'
import { range } from 'd3'
import { Accordion, Skeleton, Text } from '@global/ui'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import SummaryItems from './SummaryItems'
import RawDataModals from './RawDataModals'

interface AnalysisSummaryResultListProps {
  summary?: AnalysisResultSummary
  startTime: string | null
  endTime: string | null
}

/**
 * 분석 결과(요약 데이터) 리스트
 */
const AnalysisSummaryResultList: React.FC<AnalysisSummaryResultListProps> = ({ summary, startTime, endTime }) => {
  const [rawDataModalType, setRawDataModalType] = useState<keyof AnalysisResultSummary | null>(null)

  if (!summary || !startTime || !endTime) {
    return (
      <div className="flex flex-col gap-y-1">
        {range(3).map((num) => (
          <Skeleton key={`analysis-summary-result-list-skeleton-${num}`} colorScheme="dark" className="rounded-lg">
            <Accordion
              header={
                <div className="flex">
                  <Text size="sm">loading</Text>
                </div>
              }
            />
          </Skeleton>
        ))}
      </div>
    )
  }
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
      <SummaryItems summary={summary} setRawDataModalType={setRawDataModalType} />
      <RawDataModals
        rawDataModalType={rawDataModalType}
        setRawDataModalType={setRawDataModalType}
        startTime={startTime}
        endTime={endTime}
      />
    </div>
  )
}

export default AnalysisSummaryResultList

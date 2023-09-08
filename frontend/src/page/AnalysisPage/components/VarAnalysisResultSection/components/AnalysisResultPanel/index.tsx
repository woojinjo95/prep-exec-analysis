import React, { useMemo } from 'react'
import { Text } from '@global/ui'
import { useServiceState, useVideoSummary } from '@global/api/hook'
import { formatDateTo } from '@global/usecase'
import { useAnalysisResultSummary } from '@page/AnalysisPage/api/hook'
import AnalysisSummaryResultList from './AnalysisSummaryResultList'

/**
 * 분석 결과(요약 데이터) 패널
 */
const AnalysisResultPanel: React.FC = () => {
  const { videoSummary } = useVideoSummary()
  const startTime = useMemo(
    () => (videoSummary ? new Date(videoSummary.start_time).toISOString() : null),
    [videoSummary],
  )
  const endTime = useMemo(() => (videoSummary ? new Date(videoSummary.end_time).toISOString() : null), [videoSummary])
  const { analysisResultSummary, refetch } = useAnalysisResultSummary({
    start_time: startTime,
    end_time: endTime,
  })
  useServiceState({
    onSuccess: (state) => {
      if (state !== 'analysis' && !!analysisResultSummary) {
        refetch()
      }
    },
  })

  return (
    <div className="grid grid-cols-1 grid-rows-[auto_1fr] gap-y-2 h-full">
      <Text>
        Last Update :{' '}
        {!!analysisResultSummary &&
          formatDateTo('M DD YYYY, HH:MM AA', new Date(analysisResultSummary.last_updated_timestamp))}
      </Text>

      <AnalysisSummaryResultList summary={analysisResultSummary} startTime={startTime} endTime={endTime} />
    </div>
  )
}

export default AnalysisResultPanel

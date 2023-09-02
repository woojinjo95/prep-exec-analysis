import React from 'react'
import { useVideoSummary } from '@global/api/hook'
import FreezeSummaryResultItem from './FreezeSummaryResultItem'
import LoudnessSummaryResultItem from './LoudnessSummaryResultItem'
import ResumeSummaryResultItem from './ResumeSummaryResultItem'
import BootSummaryResultItem from './BootSummaryResultItem'
import ChannelChangeTimeSummaryResultItem from './ChannelChangeTimeSummaryResultItem'
import LogLevelFinderSummaryResultItem from './LogLevelFinderSummaryResultItem'
import LogPatternMatchingSummaryResultItem from './LogPatternMatchingSummaryResultItem'
import { useAnalysisResultSummary } from '../../../api/hook'

/**
 * 분석 결과(요약 데이터) 리스트
 */
const AnalysisSummaryResultList: React.FC = () => {
  const { videoSummary } = useVideoSummary()
  const { analysisResultSummary } = useAnalysisResultSummary({
    start_time: videoSummary?.start_time!,
    end_time: videoSummary?.end_time!,
    enabled: !!videoSummary,
  })

  if (!analysisResultSummary) return null
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
      {analysisResultSummary.freeze?.length && <FreezeSummaryResultItem results={analysisResultSummary.freeze} />}
      {analysisResultSummary.loudness?.length && (
        <LoudnessSummaryResultItem result={analysisResultSummary.loudness[0]} />
      )}
      <ResumeSummaryResultItem />
      <BootSummaryResultItem />
      <ChannelChangeTimeSummaryResultItem />
      <LogLevelFinderSummaryResultItem />
      <LogPatternMatchingSummaryResultItem />
    </div>
  )
}

export default AnalysisSummaryResultList

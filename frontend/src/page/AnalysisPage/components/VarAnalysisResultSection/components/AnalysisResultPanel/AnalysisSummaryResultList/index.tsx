import React from 'react'
import { useServiceState, useVideoSummary } from '@global/api/hook'
import FreezeSummaryResultItem from './FreezeSummaryResultItem'
import LoudnessSummaryResultItem from './LoudnessSummaryResultItem'
import ResumeSummaryResultItem from './ResumeSummaryResultItem'
import BootSummaryResultItem from './BootSummaryResultItem'
// import ChannelChangeTimeSummaryResultItem from './ChannelChangeTimeSummaryResultItem'
import LogLevelFinderSummaryResultItem from './LogLevelFinderSummaryResultItem'
import LogPatternMatchingSummaryResultItem from './LogPatternMatchingSummaryResultItem'
import { useAnalysisResultSummary } from '../../../api/hook'

/**
 * 분석 결과(요약 데이터) 리스트
 */
const AnalysisSummaryResultList: React.FC = () => {
  const { videoSummary } = useVideoSummary()
  const { analysisResultSummary, refetch } = useAnalysisResultSummary({
    start_time: videoSummary?.start_time!,
    end_time: videoSummary?.end_time!,
    // FIXME: start_time, end_time이 없는데도 api를 요청함
    enabled: !!videoSummary,
  })
  useServiceState({
    onSuccess: (state) => {
      if (state !== 'analysis') {
        refetch()
      }
    },
  })

  if (!analysisResultSummary) return null
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
      {analysisResultSummary.freeze?.length && <FreezeSummaryResultItem results={analysisResultSummary.freeze} />}
      {analysisResultSummary.loudness?.length && (
        <LoudnessSummaryResultItem result={analysisResultSummary.loudness[0]} />
      )}
      {analysisResultSummary.resume?.length && <ResumeSummaryResultItem results={analysisResultSummary.resume} />}
      {analysisResultSummary.boot?.length && <BootSummaryResultItem results={analysisResultSummary.boot} />}
      {/* <ChannelChangeTimeSummaryResultItem /> */}
      {analysisResultSummary.log_level_finder?.length && (
        <LogLevelFinderSummaryResultItem results={analysisResultSummary.log_level_finder} />
      )}
      {analysisResultSummary.log_pattern_matching?.length && (
        <LogPatternMatchingSummaryResultItem results={analysisResultSummary.log_pattern_matching} />
      )}
    </div>
  )
}

export default AnalysisSummaryResultList

import React, { useState } from 'react'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import FreezeSummaryResultItem from './FreezeSummaryResultItem'
import LoudnessSummaryResultItem from './LoudnessSummaryResultItem'
import ResumeSummaryResultItem from './ResumeSummaryResultItem'
import BootSummaryResultItem from './BootSummaryResultItem'
// import ChannelChangeTimeSummaryResultItem from './ChannelChangeTimeSummaryResultItem'
import LogLevelFinderSummaryResultItem from './LogLevelFinderSummaryResultItem'
import LogPatternMatchingSummaryResultItem from './LogPatternMatchingSummaryResultItem'

interface AnalysisSummaryResultListProps {
  summary?: AnalysisResultSummary
}

/**
 * 분석 결과(요약 데이터) 리스트
 */
const AnalysisSummaryResultList: React.FC<AnalysisSummaryResultListProps> = ({ summary }) => {
  const [rawDataModalType, setRawDataModalType] = useState<keyof AnalysisResultSummary | null>(null)

  if (!summary) return null
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
      {summary.freeze && <FreezeSummaryResultItem freeze={summary.freeze} setRawDataModalType={setRawDataModalType} />}
      {summary.loudness && <LoudnessSummaryResultItem loudness={summary.loudness} />}
      {summary.resume && <ResumeSummaryResultItem resume={summary.resume} setRawDataModalType={setRawDataModalType} />}
      {summary.boot && <BootSummaryResultItem boot={summary.boot} setRawDataModalType={setRawDataModalType} />}
      {/* <ChannelChangeTimeSummaryResultItem /> */}
      {summary.log_level_finder && <LogLevelFinderSummaryResultItem logLevelFinder={summary.log_level_finder} />}
      {summary.log_pattern_matching && (
        <LogPatternMatchingSummaryResultItem
          logPatternMatching={summary.log_pattern_matching}
          setRawDataModalType={setRawDataModalType}
        />
      )}
    </div>
  )
}

export default AnalysisSummaryResultList

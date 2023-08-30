import React from 'react'
import FreezeSummaryResultItem from './FreezeSummaryResultItem'
import LoudnessSummaryResultItem from './LoudnessSummaryResultItem'
import ResumeSummaryResultItem from './ResumeSummaryResultItem'
import BootSummaryResultItem from './BootSummaryResultItem'
import ChannelChangeTimeSummaryResultItem from './ChannelChangeTimeSummaryResultItem'
import LogLevelFinderSummaryResultItem from './LogLevelFinderSummaryResultItem'
import LogPatternMatchingSummaryResultItem from './LogPatternMatchingSummaryResultItem'

/**
 * 분석 결과(요약 데이터) 리스트
 */
const AnalysisSummaryResultList: React.FC = () => {
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
      <FreezeSummaryResultItem />
      <LoudnessSummaryResultItem />
      <ResumeSummaryResultItem />
      <BootSummaryResultItem />
      <ChannelChangeTimeSummaryResultItem />
      <LogLevelFinderSummaryResultItem />
      <LogPatternMatchingSummaryResultItem />
    </div>
  )
}

export default AnalysisSummaryResultList

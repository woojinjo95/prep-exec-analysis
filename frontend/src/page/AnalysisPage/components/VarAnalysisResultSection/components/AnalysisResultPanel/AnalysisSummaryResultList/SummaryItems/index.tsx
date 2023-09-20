import React from 'react'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import FreezeSummaryItem from './FreezeSummaryItem'
import LoudnessSummaryItem from './LoudnessSummaryItem'
import ResumeSummaryItem from './ResumeSummaryItem'
import BootSummaryItem from './BootSummaryItem'
// import ChannelChangeTimeSummaryItem from './ChannelChangeTimeSummaryItem'
import LogLevelFinderSummaryItem from './LogLevelFinderSummaryItem'
import LogPatternMatchingSummaryItem from './LogPatternMatchingSummaryItem'
import MonkeyTestSummaryItem from './MonkeyTestSummaryItem'
import IntelligentMonkeyTestSummaryItem from './IntelligentMonkeyTestSummaryItem'

interface SummaryItemsProps {
  summary: AnalysisResultSummary
  setRawDataModalType: React.Dispatch<React.SetStateAction<keyof AnalysisResultSummary | null>>
}

const SummaryItems: React.FC<SummaryItemsProps> = ({ summary, setRawDataModalType }) => {
  return (
    <>
      {summary.freeze && <FreezeSummaryItem freeze={summary.freeze} setRawDataModalType={setRawDataModalType} />}
      {summary.loudness && <LoudnessSummaryItem loudness={summary.loudness} />}
      {summary.resume && <ResumeSummaryItem resume={summary.resume} setRawDataModalType={setRawDataModalType} />}
      {summary.boot && <BootSummaryItem boot={summary.boot} setRawDataModalType={setRawDataModalType} />}
      {/* <ChannelChangeTimeSummaryItem /> */}
      {summary.log_level_finder && <LogLevelFinderSummaryItem logLevelFinder={summary.log_level_finder} />}
      {summary.log_pattern_matching && (
        <LogPatternMatchingSummaryItem
          logPatternMatching={summary.log_pattern_matching}
          setRawDataModalType={setRawDataModalType}
        />
      )}
      {summary.monkey_test && (
        <MonkeyTestSummaryItem monkeyTest={summary.monkey_test} setRawDataModalType={setRawDataModalType} />
      )}
      {summary.intelligent_monkey_test && (
        <IntelligentMonkeyTestSummaryItem
          intelligentMonkeyTest={summary.intelligent_monkey_test}
          setRawDataModalType={setRawDataModalType}
        />
      )}
    </>
  )
}

export default SummaryItems

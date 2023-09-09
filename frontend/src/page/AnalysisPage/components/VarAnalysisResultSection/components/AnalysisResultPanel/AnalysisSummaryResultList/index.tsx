import React, { useState } from 'react'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import FreezeSummaryItem from './FreezeSummaryItem'
import LoudnessSummaryItem from './LoudnessSummaryItem'
import ResumeSummaryItem from './ResumeSummaryItem'
import BootSummaryItem from './BootSummaryItem'
// import ChannelChangeTimeSummaryItem from './ChannelChangeTimeSummaryItem'
import LogLevelFinderSummaryItem from './LogLevelFinderSummaryItem'
import LogPatternMatchingSummaryItem from './LogPatternMatchingSummaryItem'
import ResumeRawDataModal from './ResumeRawDataModal'
import LogPatternMatchingRawDataModal from './LogPatternMatchingRawDataModal'
import BootRawDataModal from './BootRawDataModal'
import FreezeRawDataModal from './FreezeRawDataModal'
import MonkeyTestSummaryItem from './MonkeyTestSummaryItem'
import IntelligentMonkeyTestSummaryItem from './IntelligentMonkeyTestSummaryItem'
import MonkeyTestRawDataModal from './MonkeyTestRawDataModal'

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

  if (!summary || !startTime || !endTime) return null
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
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

      {rawDataModalType === 'freeze' && (
        <FreezeRawDataModal
          isOpen={rawDataModalType === 'freeze'}
          onClose={() => setRawDataModalType(null)}
          startTime={startTime}
          endTime={endTime}
        />
      )}
      {rawDataModalType === 'resume' && (
        <ResumeRawDataModal
          isOpen={rawDataModalType === 'resume'}
          onClose={() => setRawDataModalType(null)}
          startTime={startTime}
          endTime={endTime}
        />
      )}
      {rawDataModalType === 'boot' && (
        <BootRawDataModal
          isOpen={rawDataModalType === 'boot'}
          onClose={() => setRawDataModalType(null)}
          startTime={startTime}
          endTime={endTime}
        />
      )}
      {rawDataModalType === 'log_pattern_matching' && (
        <LogPatternMatchingRawDataModal
          isOpen={rawDataModalType === 'log_pattern_matching'}
          onClose={() => setRawDataModalType(null)}
          startTime={startTime}
          endTime={endTime}
        />
      )}
      {rawDataModalType === 'monkey_test' && (
        <MonkeyTestRawDataModal
          isOpen={rawDataModalType === 'monkey_test'}
          onClose={() => setRawDataModalType(null)}
          startTime={startTime}
          endTime={endTime}
        />
      )}
    </div>
  )
}

export default AnalysisSummaryResultList

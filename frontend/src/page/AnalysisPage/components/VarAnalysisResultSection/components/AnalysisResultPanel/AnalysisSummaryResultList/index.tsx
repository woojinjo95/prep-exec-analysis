import React, { useState } from 'react'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import FreezeSummaryResultItem from './FreezeSummaryResultItem'
import LoudnessSummaryResultItem from './LoudnessSummaryResultItem'
import ResumeSummaryResultItem from './ResumeSummaryResultItem'
import BootSummaryResultItem from './BootSummaryResultItem'
// import ChannelChangeTimeSummaryResultItem from './ChannelChangeTimeSummaryResultItem'
import LogLevelFinderSummaryResultItem from './LogLevelFinderSummaryResultItem'
import LogPatternMatchingSummaryResultItem from './LogPatternMatchingSummaryResultItem'
import ResumeRawDataModal from './ResumeRawDataModal'
import LogPatternMatchingRawDataModal from './LogPatternMatchingRawDataModal'
import BootRawDataModal from './BootRawDataModal'
import FreezeRawDataModal from './FreezeRawDataModal'

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
    </div>
  )
}

export default AnalysisSummaryResultList

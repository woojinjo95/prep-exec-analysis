import React from 'react'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import ResumeRawDataModal from './ResumeRawDataModal'
import LogPatternMatchingRawDataModal from './LogPatternMatchingRawDataModal'
import BootRawDataModal from './BootRawDataModal'
import FreezeRawDataModal from './FreezeRawDataModal'
import MonkeyTestRawDataModal from './MonkeyTestRawDataModal'
import IntelligentMonkeyTestRawDataModal from './IntelligentMonkeyTestRawDataModal'

interface RawDataModalsProps {
  rawDataModalType: keyof AnalysisResultSummary | null
  setRawDataModalType: React.Dispatch<React.SetStateAction<keyof AnalysisResultSummary | null>>
  startTime: string
  endTime: string
}

const RawDataModals: React.FC<RawDataModalsProps> = ({ rawDataModalType, setRawDataModalType, startTime, endTime }) => {
  return (
    <>
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
      {rawDataModalType === 'intelligent_monkey_test' && (
        <IntelligentMonkeyTestRawDataModal
          isOpen={rawDataModalType === 'intelligent_monkey_test'}
          onClose={() => setRawDataModalType(null)}
          startTime={startTime}
          endTime={endTime}
        />
      )}
    </>
  )
}

export default RawDataModals

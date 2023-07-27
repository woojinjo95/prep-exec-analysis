import React from 'react'

import { PageContainer } from '@global/ui'
import LogTraceSection from './components/LogTraceSection'
import VideoDetailSection from './components/VideoDetailSection'
import TimelineSection from './components/TimelineSection'
import VarAnalysisResultSection from './components/VarAnalysisResultSection'

/**
 * 분석 조회 페이지
 */
const AnalysisPage: React.FC = () => {
  return (
    <PageContainer className="grid grid-cols-[65%_35%] grid-rows-[40%_25%_35%] overflow-y-hidden">
      <VideoDetailSection />
      <VarAnalysisResultSection />
      <LogTraceSection />
      <TimelineSection />
    </PageContainer>
  )
}

export default AnalysisPage

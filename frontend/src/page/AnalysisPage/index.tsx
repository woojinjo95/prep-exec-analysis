import React from 'react'

import { PageContainer } from '@global/ui'
import LogSection from './components/LogSection'
import VideoDetailSection from './components/VideoDetailSection'
import TimelineSection from './components/TimelineSection'

/**
 * 분석 조회 페이지
 */
const AnalysisPage: React.FC = () => {
  return (
    <PageContainer className="grid grid-cols-[60%_40%] grid-rows-[60%_39%]">
      <LogSection />
      <VideoDetailSection />
      <TimelineSection />
    </PageContainer>
  )
}

export default AnalysisPage

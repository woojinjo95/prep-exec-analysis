import React from 'react'

import { PageContainer } from '@global/ui'
import LogSection from './components/LogSection'
import VideoDetailSection from './components/VideoDetailSection'
import TimelineChartSection from './components/TimelineChartSection'

/**
 * 분석 조회 페이지
 */
const AnalysisPage: React.FC = () => {
  return (
    <PageContainer className="grid grid-cols-[60%_40%] grid-rows-[60%_39%]">
      <LogSection />
      <VideoDetailSection />
      <TimelineChartSection />
    </PageContainer>
  )
}

export default AnalysisPage

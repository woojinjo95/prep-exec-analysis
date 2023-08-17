import React, { useState } from 'react'

import { PageContainer, Text } from '@global/ui'
import { useScenarios } from '@global/api/hook'
import LogTraceSection from './components/LogTraceSection'
import VideoDetailSection from './components/VideoDetailSection'
import TimelineSection from './components/TimelineSection'
import VarAnalysisResultSection from './components/VarAnalysisResultSection'

/**
 * 분석 조회 페이지
 */
const AnalysisPage: React.FC = () => {
  const [startTime] = useState<Date>(new Date('2023-08-17T04:47:53.733Z'))
  const [endTime] = useState<Date>(new Date('2023-08-17T04:50:53.733Z'))
  const [scenarioId, setScenarioId] = useState<string | null>(null)

  useScenarios({
    onSuccess: (res) => {
      if (res && res.items.length > 0) {
        // setScenarioId(res.items[0].id)
        setScenarioId('e8e15536-d3d5-4944-b39e-f91bda5e126f')
      }
    },
  })

  return (
    <PageContainer className="grid grid-cols-[65%_35%] grid-rows-[40%_25%_calc(35%-28px)_28px]">
      <VideoDetailSection scenarioId={scenarioId} />
      <VarAnalysisResultSection />
      <LogTraceSection />
      <TimelineSection startTime={startTime} endTime={endTime} scenarioId={scenarioId} />
      <div className="col-span-2 bg-black border-t border-[#37383E] flex items-center px-5">
        <Text size="xs" colorScheme="grey">
          © 2023 NEXTLab ALL RIGHTS RESERVED.
        </Text>
      </div>
    </PageContainer>
  )
}

export default AnalysisPage

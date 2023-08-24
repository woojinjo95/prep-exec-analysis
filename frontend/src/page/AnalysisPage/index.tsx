import React, { useEffect, useState } from 'react'
import { useRecoilValue, useSetRecoilState } from 'recoil'
import { PageContainer, Text } from '@global/ui'
import { useScenarios } from '@global/api/hook'
import AppURL from '@global/constant/appURL'
import { scenarioIdState, videoBlobURLState } from '@global/atom'

import LogTraceSection from './components/LogTraceSection'
import VideoDetailSection from './components/VideoDetailSection'
import TimelineSection from './components/TimelineSection'
import VarAnalysisResultSection from './components/VarAnalysisResultSection'
import { prefetchVideoFile } from './usecase'

/**
 * 분석 조회 페이지
 */
const AnalysisPage: React.FC = () => {
  // TODO: rxjs? recoil? 고민
  const [startTime] = useState<Date>(new Date('2023-08-18T07:59:28.731511+00:00'))
  const [endTime] = useState<Date>(new Date('2023-08-18T08:03:13.925471+00:00'))
  const scenarioId = useRecoilValue(scenarioIdState)
  const setVideoBlobURL = useSetRecoilState(videoBlobURLState)

  useScenarios({
    onSuccess: (res) => {
      if (res && res.items.length > 0) {
        // setScenarioId(res.items[0].id)
      }
    },
  })

  useEffect(() => {
    if (!scenarioId) return

    prefetchVideoFile(
      `${AppURL.backendURL}/api/v1/file/video?scenario_id=${scenarioId}`,
      (url) => {
        setVideoBlobURL(url)
      },
      (progress) => {
        console.log(`${progress}%`)
      },
    )
  }, [scenarioId])

  return (
    <PageContainer className="grid grid-cols-[65%_35%] grid-rows-[40%_25%_calc(35%-28px)_28px]">
      <VideoDetailSection />
      <VarAnalysisResultSection />
      <LogTraceSection />
      <TimelineSection startTime={startTime} endTime={endTime} />
      <div className="col-span-2 bg-black border-t border-[#37383E] flex items-center px-5">
        <Text size="xs" colorScheme="grey">
          © 2023 NEXTLab ALL RIGHTS RESERVED.
        </Text>
      </div>
    </PageContainer>
  )
}

export default AnalysisPage

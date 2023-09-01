import React, { useEffect } from 'react'
import { useRecoilValue, useSetRecoilState } from 'recoil'
import { PageContainer, Text } from '@global/ui'
import { useVideoTimestamp } from '@global/api/hook'
import { AppURL } from '@global/constant'
import { scenarioIdState, testRunIdState, videoBlobURLState } from '@global/atom'

import { useNavigate } from 'react-router-dom'
import LogTraceSection from './components/LogTraceSection'
import VideoDetailSection from './components/VideoDetailSection'
import TimelineSection from './components/TimelineSection'
import VarAnalysisResultSection from './components/VarAnalysisResultSection'
import { prefetchVideoFile } from './usecase'
import apiUrls from './api/url'

/**
 * 분석 조회 페이지
 */
const AnalysisPage: React.FC = () => {
  const { videoTimestamp } = useVideoTimestamp()
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const setVideoBlobURL = useSetRecoilState(videoBlobURLState)

  const navigate = useNavigate()

  useEffect(() => {
    if (!scenarioId) {
      navigate('/', { replace: true })
    }
  }, [])

  useEffect(() => {
    if (!scenarioId || !testRunId) return

    prefetchVideoFile(
      `${AppURL.backendURL}${apiUrls.video}?scenario_id=${scenarioId}&testrun_id=${testRunId}`,
      (url) => {
        setVideoBlobURL(url)
      },
      (progress) => {
        console.log(`${progress}%`)
      },
    )
  }, [scenarioId, testRunId])

  return (
    <PageContainer className="grid grid-cols-[65%_35%] grid-rows-[40%_25%_calc(35%-28px)_28px]">
      <VideoDetailSection />
      <VarAnalysisResultSection />
      <LogTraceSection />
      <TimelineSection
        startTime={videoTimestamp?.start_time ? new Date(videoTimestamp.start_time) : null}
        endTime={videoTimestamp?.end_time ? new Date(videoTimestamp.end_time) : null}
      />
      <div className="col-span-2 bg-black border-t border-[#37383E] flex items-center px-5">
        <Text size="xs" colorScheme="grey">
          © 2023 NEXTLab ALL RIGHTS RESERVED.
        </Text>
      </div>
    </PageContainer>
  )
}

export default AnalysisPage

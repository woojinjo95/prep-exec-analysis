import React, { useEffect } from 'react'
import { useRecoilState, useRecoilValue, useSetRecoilState } from 'recoil'
import { PageContainer, Text } from '@global/ui'
import { useVideoSummary } from '@global/api/hook'
import { AppURL } from '@global/constant'
import { cursorDateTimeState, scenarioIdState, testRunIdState, videoBlobURLState } from '@global/atom'

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
  const navigate = useNavigate()
  const { videoSummary } = useVideoSummary()
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const setVideoBlobURL = useSetRecoilState(videoBlobURLState)
  const [cursorDateTime, setCursorDateTime] = useRecoilState(cursorDateTimeState)

  // 서비스 진입 시 선택된 시나리오 id가 없을 경우 -> 시나리오 선택 페이지로 이동
  // FIXME: testRunId가 없을때는 ..?
  useEffect(() => {
    if (!scenarioId) {
      navigate('/', { replace: true })
    }
  }, [])

  // testrun 시작시간으로 cursorDateTime 초기값 설정
  useEffect(() => {
    if (!!cursorDateTime || !videoSummary) return
    setCursorDateTime(new Date(videoSummary.start_time))
  }, [videoSummary])

  // 비디오 스냅샷 컴포넌트에서 사용할 video fetch
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
        startTime={videoSummary?.start_time ? new Date(videoSummary.start_time) : null}
        endTime={videoSummary?.end_time ? new Date(videoSummary.end_time) : null}
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

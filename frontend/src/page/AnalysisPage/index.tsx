import React, { useEffect } from 'react'
import { useRecoilState, useRecoilValue } from 'recoil'
import { useNavigate } from 'react-router-dom'
import { PageContainer, Text } from '@global/ui'
import { useVideoSummary } from '@global/api/hook'
import { cursorDateTimeState, scenarioIdState, testRunIdState } from '@global/atom'

import LogTraceSection from './components/LogTraceSection'
import VideoDetailSection from './components/VideoDetailSection'
import TimelineSection from './components/TimelineSection'
import VarAnalysisResultSection from './components/VarAnalysisResultSection'

/**
 * 분석 조회 페이지
 */
const AnalysisPage: React.FC = () => {
  const navigate = useNavigate()
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const [cursorDateTime, setCursorDateTime] = useRecoilState(cursorDateTimeState)
  const { videoSummary } = useVideoSummary({
    onSuccess: ({ start_time, end_time }) => {
      if (
        !cursorDateTime ||
        new Date(cursorDateTime).getTime() < new Date(start_time).getTime() ||
        new Date(cursorDateTime).getTime() > new Date(end_time).getTime()
      ) {
        setCursorDateTime(new Date(start_time))
      }
    },
  })

  // 분석페이지 진입 시 선택된 시나리오 id 또는 테스트한 테스트런 id가 없을 경우 -> 시나리오 선택 페이지로 이동
  useEffect(() => {
    if (!scenarioId || !testRunId) {
      navigate('/', { replace: true })
    }
  }, [])

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

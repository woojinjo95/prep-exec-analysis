import React, { useEffect, useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'
import { Skeleton, Text, VideoSnapshots } from '@global/ui'
import { CHART_HEIGHT, VIDEO_SNAPSHOT_HEIGHT } from '@global/constant'

import { useAnalysisResultSummary } from '@page/AnalysisPage/api/hook'
import ScrollComponent from '@global/ui/ScrollComponent'
import { useCursorEvent, useHandleChartWheel } from './hook'
import {
  HorizontalScrollBar,
  CPUChart,
  MemoryChart,
  EventLogChart,
  ColorReferenceChart,
  FreezeChart,
  LogLevelFinderChart,
  TimelineHeader,
  LoudnessChart,
  ResumeBootChart,
  LogPatternMatchingChart,
  TimelineChartContainer,
} from './components'
import MonkeyTestChart from './components/MonkeyTestChart'
import IntelligentMonkeyTestChart from './components/IntelligentMonkeyTestChart'
import { ChartLabel } from './constant'

interface TimelineSectionProps {
  startTime: Date | null
  endTime: Date | null
}

/**
 * 타임라인 차트 영역
 */
const TimelineSection: React.FC<TimelineSectionProps> = ({ startTime, endTime }) => {
  const chartWrapperRef = useRef<HTMLDivElement | null>(null)
  const [dimension, setDimension] = useState<{ left: number; width: number } | null>(null)
  const [scrollBarTwoPosX, setScrollBarTwoPosX] = useState<[number, number] | null>(null)
  // 순서 중요 X
  const [activeChartList, setActiveChartList] = useState<(keyof typeof ChartLabel)[]>([
    'video',
    'color_reference',
    'event_log',
    'cpu',
    'memory',
  ])
  // 순서 중요 O, 전체 차트 순서
  const [allChartList, setAllChartList] = useState<(keyof typeof ChartLabel)[]>([
    'video',
    'color_reference',
    'event_log',
    'cpu',
    'memory',
  ])
  const { analysisResultSummary } = useAnalysisResultSummary({
    start_time: startTime?.toISOString() || null,
    end_time: endTime?.toISOString() || null,
    onSuccess: (summary) => {
      let newAllChartList: (keyof typeof ChartLabel)[] = ['video', 'color_reference', 'event_log']

      if (summary.monkey_test) {
        newAllChartList = [...newAllChartList, 'monkey_test']
      }
      if (summary.intelligent_monkey_test) {
        newAllChartList = [...newAllChartList, 'intelligent_monkey_test']
      }
      if (summary.freeze) {
        newAllChartList = [...newAllChartList, 'video_analysis_result']
      }
      if (summary.loudness) {
        newAllChartList = [...newAllChartList, 'loudness']
      }
      if (summary.boot || summary.resume) {
        newAllChartList = [...newAllChartList, 'resume_boot']
      }
      ;(['log_level_finder', 'log_pattern_matching'] as const).forEach((type) => {
        if (summary[type]) {
          newAllChartList = [...newAllChartList, type]
        }
      })
      newAllChartList = [...newAllChartList, 'cpu', 'memory']

      setAllChartList(newAllChartList)
      setActiveChartList(newAllChartList)
    },
  })
  const isReadyRenderChart = useMemo(
    () => !!startTime && !!endTime && !!analysisResultSummary,
    [startTime, endTime, analysisResultSummary],
  )

  // X축 전체 scale
  const timelineScaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!dimension || !startTime || !endTime) return null
    return d3.scaleTime().domain([startTime, endTime]).range([0, dimension.width])
  }, [dimension, startTime, endTime])

  // FIXME: 전체 차트에서 변화대상 데이터가 1000개 이상일 경우 debounce 적용
  const scrollbarScaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!dimension || !timelineScaleX || !scrollBarTwoPosX) return null
    return d3
      .scaleTime()
      .domain([timelineScaleX.invert(scrollBarTwoPosX[0]), timelineScaleX.invert(scrollBarTwoPosX[1])])
      .range([0, dimension.width])
  }, [dimension, timelineScaleX, scrollBarTwoPosX])

  // 커서 드래그 관련 state
  const { onCursorPointerDown, onCursorPointerMove, onCursorPointerUp, cursorTranslateX, isCursorDragging } =
    useCursorEvent({
      scaleX: scrollbarScaleX,
      offsetLeft: dimension?.left,
      width: dimension?.width,
    })

  // 차트 가로스크롤 hook
  useHandleChartWheel({
    ref: chartWrapperRef.current,
    isReadyRenderChart,
    setScrollBarTwoPosX,
    chartWidth: dimension?.width,
  })

  const handleWindowResize = () => {
    if (!chartWrapperRef.current || dimension?.width || dimension?.left || scrollBarTwoPosX) return

    setDimension({ width: chartWrapperRef.current.clientWidth, left: chartWrapperRef.current.offsetLeft })
    setScrollBarTwoPosX([0, chartWrapperRef.current.clientWidth])
  }

  useEffect(() => {
    handleWindowResize()
    // dependency array: chartWrapperRef 렌더링 조건
  }, [isReadyRenderChart])

  useEffect(() => {
    window.addEventListener('resize', handleWindowResize)
    return () => {
      window.removeEventListener('resize', handleWindowResize)
    }
  }, [])

  // === isReadyRenderChart
  if (!startTime || !endTime || !analysisResultSummary) {
    return <section className="h-full bg-black grid grid-cols-1 grid-rows-[auto_1fr_auto]" />
  }
  return (
    <section className="h-full bg-black grid grid-cols-1 grid-rows-[auto_1fr_auto]">
      {/* time ticks */}
      <TimelineHeader
        scaleX={scrollbarScaleX}
        chartWidth={dimension?.width}
        cursorTranslateX={cursorTranslateX}
        isCursorDragging={isCursorDragging}
        activeChartList={activeChartList}
        setActiveChartList={setActiveChartList}
        allChartList={allChartList}
        setAllChartList={setAllChartList}
      />

      <ScrollComponent>
        <div className="grid grid-cols-[auto_1fr] grid-rows-1 overflow-y-auto overflow-x-hidden">
          <div className="w-48 z-10">
            {allChartList
              .filter((key) => activeChartList.includes(key))
              .map((chartKey, index) => (
                <div
                  key={`timeline-chart-title-${chartKey}-${index}`}
                  className="border-b-[1px] border-light-charcoal bg-charcoal py-2 px-5"
                  style={{ height: CHART_HEIGHT }}
                >
                  <Text colorScheme="grey" weight="medium">
                    {ChartLabel[chartKey]}
                  </Text>
                </div>
              ))}
          </div>

          {/* chart */}
          <TimelineChartContainer
            ref={chartWrapperRef}
            chartCount={activeChartList.length}
            cursorTranslateX={cursorTranslateX}
            onPointerDown={onCursorPointerDown}
            onPointerMove={onCursorPointerMove}
            onPointerUp={onCursorPointerUp}
          >
            {allChartList.map((chartKey) => {
              if (chartKey === 'video') {
                return (
                  <VideoSnapshots
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    tickCount={15}
                    scaleX={scrollbarScaleX}
                    startTime={timelineScaleX && scrollBarTwoPosX ? timelineScaleX.invert(scrollBarTwoPosX[0]) : null}
                    endTime={timelineScaleX && scrollBarTwoPosX ? timelineScaleX.invert(scrollBarTwoPosX[1]) : null}
                    loadingComponent={
                      <Skeleton
                        className="w-full border-b border-[#37383E]"
                        style={{ height: VIDEO_SNAPSHOT_HEIGHT }}
                        colorScheme="dark"
                      />
                    }
                  />
                )
              }

              if (chartKey === 'color_reference') {
                return (
                  <ColorReferenceChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                  />
                )
              }

              if (chartKey === 'event_log') {
                return (
                  <EventLogChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                  />
                )
              }

              if (chartKey === 'monkey_test') {
                return (
                  <MonkeyTestChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                    summary={analysisResultSummary}
                  />
                )
              }

              if (chartKey === 'intelligent_monkey_test') {
                return (
                  <IntelligentMonkeyTestChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                    summary={analysisResultSummary}
                  />
                )
              }

              if (chartKey === 'video_analysis_result') {
                return (
                  <FreezeChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                    summary={analysisResultSummary}
                  />
                )
              }

              if (chartKey === 'loudness') {
                return (
                  <LoudnessChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                    summary={analysisResultSummary}
                  />
                )
              }

              if (chartKey === 'resume_boot') {
                return (
                  <ResumeBootChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                    summary={analysisResultSummary}
                  />
                )
              }

              if (chartKey === 'log_level_finder') {
                // FIXME: 데이터가 너무많음. api 로딩이 오래걸림
                return (
                  <LogLevelFinderChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                    summary={analysisResultSummary}
                  />
                )
              }

              if (chartKey === 'log_pattern_matching') {
                return (
                  <LogPatternMatchingChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                    summary={analysisResultSummary}
                  />
                )
              }

              if (chartKey === 'cpu') {
                return (
                  <CPUChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                  />
                )
              }

              if (chartKey === 'memory') {
                return (
                  <MemoryChart
                    key={`chart-${chartKey}`}
                    isVisible={activeChartList.includes(chartKey)}
                    scaleX={scrollbarScaleX}
                    startTime={startTime}
                    endTime={endTime}
                    dimension={dimension}
                  />
                )
              }

              return null
            })}
          </TimelineChartContainer>
        </div>
      </ScrollComponent>

      <div className="grid grid-cols-[auto_1fr]">
        <div className="w-48" />

        {/* horizontal scrollbar */}
        <HorizontalScrollBar
          dimension={dimension}
          scrollBarTwoPosX={scrollBarTwoPosX}
          setScrollBarTwoPosX={setScrollBarTwoPosX}
        />
      </div>
    </section>
  )
}

export default TimelineSection

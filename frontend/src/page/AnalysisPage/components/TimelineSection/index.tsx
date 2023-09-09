import React, { useEffect, useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'
import { useRecoilValue } from 'recoil'
import { Text, VideoSnapshots } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { videoBlobURLState } from '@global/atom'

import { useAnalysisResultSummary } from '@page/AnalysisPage/api/hook'
import { useCursorEvent } from './hook'
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

const ChartLabel = {
  video: 'Video',
  color_reference: 'Color Reference',
  event_log: 'Event Log',
  monkey_test: 'Monkey Test',
  intelligent_monkey_test: 'Intelligent Monkey Test',
  video_analysis_result: 'Video Analysis Result',
  loudness: 'Loudness',
  resume_boot: 'Resume, Boot Measurement',
  log_level_finder: 'Log Level Finder',
  log_pattern_matching: 'Log Pattern Matching',
  cpu: 'CPU',
  memory: 'Memory',
} as const

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
  const src = useRecoilValue(videoBlobURLState)
  // TODO: 순서변경 / 숨기기 / 보기
  const [chartList, setChartList] = useState<(keyof typeof ChartLabel)[]>([
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
      setChartList((prev) => prev.filter((v) => v === 'video' || v === 'color_reference' || v === 'event_log'))

      if (summary.monkey_test) {
        setChartList((prev) => [...prev, 'monkey_test'])
      }

      if (summary.intelligent_monkey_test) {
        setChartList((prev) => [...prev, 'intelligent_monkey_test'])
      }

      if (summary.freeze) {
        setChartList((prev) => [...prev, 'video_analysis_result'])
      }

      if (summary.loudness) {
        setChartList((prev) => [...prev, 'loudness'])
      }

      if (summary.boot || summary.resume) {
        setChartList((prev) => [...prev, 'resume_boot'])
      }

      ;(['log_level_finder', 'log_pattern_matching'] as const).forEach((type) => {
        if (summary[type]) {
          setChartList((prev) => [...prev, type])
        }
      })

      setChartList((prev) => [...prev, 'cpu', 'memory'])
    },
  })

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

  useEffect(() => {
    if (!chartWrapperRef.current || dimension?.width || dimension?.left || scrollBarTwoPosX) return

    setDimension({ width: chartWrapperRef.current.clientWidth, left: chartWrapperRef.current.offsetLeft })
    setScrollBarTwoPosX([0, chartWrapperRef.current.clientWidth])
    // dependency array: chartWrapperRef 렌더링 조건
  }, [startTime, endTime, analysisResultSummary])

  /**
   * 스냅샷 시작 시간
   */
  const snapshotStartMillisecond = useMemo(() => {
    if (!startTime || !timelineScaleX || !scrollBarTwoPosX) return null
    return timelineScaleX.invert(scrollBarTwoPosX[0]).getTime() - startTime.getTime()
  }, [startTime, timelineScaleX, scrollBarTwoPosX])

  /**
   * 스냅샷 끝 시간
   */
  const snapshotEndMillisecond = useMemo(() => {
    if (!startTime || !timelineScaleX || !scrollBarTwoPosX) return null
    return timelineScaleX.invert(scrollBarTwoPosX[1]).getTime() - startTime.getTime()
  }, [startTime, timelineScaleX, scrollBarTwoPosX])

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
      />

      <div className="grid grid-cols-[auto_1fr] grid-rows-1 overflow-y-auto overflow-x-hidden">
        <div className="w-48 z-10">
          {chartList.map((chartKey, index) => (
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
          chartCount={chartList.length}
          cursorTranslateX={cursorTranslateX}
          onPointerDown={onCursorPointerDown}
          onPointerMove={onCursorPointerMove}
          onPointerUp={onCursorPointerUp}
        >
          {chartList.map((chartKey) => {
            if (chartKey === 'video') {
              return (
                // TODO: src가 없을 때 -> progress 표시 ?
                <VideoSnapshots
                  key={`chart-${chartKey}`}
                  src={src}
                  tickCount={15}
                  startMillisecond={snapshotStartMillisecond}
                  endMillisecond={snapshotEndMillisecond}
                />
              )
            }

            if (chartKey === 'color_reference') {
              return (
                <ColorReferenceChart
                  key={`chart-${chartKey}`}
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

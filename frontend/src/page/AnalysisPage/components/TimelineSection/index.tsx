import React, { useEffect, useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'
import { useRecoilValue } from 'recoil'
import { Text, VideoSnapshots } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { videoBlobURLState } from '@global/atom'

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
  const { onCursorPointerDown, onCursorPointerMove, onCursorPointerUp, cursorTranslateX } = useCursorEvent({
    scaleX: scrollbarScaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  useEffect(() => {
    if (!chartWrapperRef.current || dimension?.width || dimension?.left || scrollBarTwoPosX) return

    setDimension({ width: chartWrapperRef.current.clientWidth, left: chartWrapperRef.current.offsetLeft })
    setScrollBarTwoPosX([0, chartWrapperRef.current.clientWidth])
    // dependency array: chartWrapperRef 렌더링 조건
  }, [startTime, endTime])

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

  if (!startTime || !endTime) {
    return (
      <section className="h-full bg-black grid grid-cols-1 grid-rows-[auto_1fr_auto]">
        <TimelineHeader scaleX={scrollbarScaleX} chartWidth={dimension?.width} />
      </section>
    )
  }
  return (
    <section className="h-full bg-black grid grid-cols-1 grid-rows-[auto_1fr_auto]">
      {/* time ticks */}
      <TimelineHeader scaleX={scrollbarScaleX} chartWidth={dimension?.width} cursorTranslateX={cursorTranslateX} />

      <div className="grid grid-cols-[auto_1fr] grid-rows-1 overflow-y-auto overflow-x-hidden">
        <div className="w-48 z-10">
          {[
            'Video',
            'Color Reference',
            'Event Log',
            'Video Analysis Result',
            'Loudness',
            'Resume, Boot Measurement',
            'Log Level Finder',
            'Log Pattern Matching',
            'CPU',
            'Memory',
          ].map((title, index) => (
            <div
              key={`timeline-chart-title-${title}-${index}`}
              className="border-b-[1px] border-light-charcoal bg-charcoal py-2 px-5"
              style={{ height: CHART_HEIGHT }}
            >
              <Text colorScheme="grey" weight="medium">
                {title}
              </Text>
            </div>
          ))}
        </div>

        {/* chart */}
        <TimelineChartContainer
          ref={chartWrapperRef}
          cursorTranslateX={cursorTranslateX}
          onPointerDown={onCursorPointerDown}
          onPointerMove={onCursorPointerMove}
          onPointerUp={onCursorPointerUp}
        >
          {/* TODO: src가 없을 때 -> progress 표시 ? */}
          <VideoSnapshots
            src={src}
            tickCount={15}
            startMillisecond={snapshotStartMillisecond}
            endMillisecond={snapshotEndMillisecond}
          />
          <ColorReferenceChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} dimension={dimension} />
          <EventLogChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} dimension={dimension} />
          <FreezeChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} />
          <LoudnessChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} dimension={dimension} />
          <ResumeBootChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} />
          {/* FIXME: 데이터가 너무많음. api 로딩이 오래걸림 */}
          <LogLevelFinderChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} dimension={dimension} />
          <LogPatternMatchingChart
            scaleX={scrollbarScaleX}
            startTime={startTime}
            endTime={endTime}
            dimension={dimension}
          />
          <CPUChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} dimension={dimension} />
          <MemoryChart scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} dimension={dimension} />
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

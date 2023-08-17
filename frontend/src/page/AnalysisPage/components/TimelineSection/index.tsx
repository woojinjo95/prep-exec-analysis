import React, { useEffect, useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'

import { Text } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import HorizontalScrollBar from './components/HorizontalScrollBar'
import CPUChart from './components/CPUChart'
import MemoryChart from './components/MemoryChart'

interface TimelineSectionProps {
  startTime: Date
  endTime: Date
}

/**
 * 타임라인 차트 영역
 */
const TimelineSection: React.FC<TimelineSectionProps> = ({ startTime, endTime }) => {
  const chartWrapperRef = useRef<HTMLDivElement | null>(null)
  const [chartWidth, setChartWidth] = useState<number | null>(null)
  const [scrollBarTwoPosX, setScrollBarTwoPosX] = useState<[number, number] | null>(null)

  // 전체 스케일
  const timelineScaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!chartWidth) return null
    return d3
      .scaleTime()
      .domain([new Date(startTime), new Date(endTime)])
      .range([0, chartWidth])
  }, [chartWidth, startTime, endTime])

  // FIXME: 전체 차트에서 변화대상 데이터가 1000개 이상일 경우 debounce 적용
  const scrollbarScaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!chartWidth || !timelineScaleX || !scrollBarTwoPosX) return null
    return d3
      .scaleTime()
      .domain([timelineScaleX.invert(scrollBarTwoPosX[0]), timelineScaleX.invert(scrollBarTwoPosX[1])])
      .range([0, chartWidth])
  }, [chartWidth, timelineScaleX, scrollBarTwoPosX])

  useEffect(() => {
    if (!chartWrapperRef.current) return

    setChartWidth(chartWrapperRef.current.clientWidth)
    setScrollBarTwoPosX([0, chartWrapperRef.current.clientWidth])
  }, [])

  return (
    <section className="h-full bg-black grid grid-cols-1 grid-rows-[auto_1fr_auto]">
      {/* time */}
      <div className="text-white">time</div>

      <div className="grid grid-cols-[auto_1fr] grid-rows-1 overflow-y-auto overflow-x-hidden">
        <div className="w-48 z-10">
          {['CPU', 'Memory'].map((title, index) => (
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
        <div className="border-l-[0.5px] border-r-[0.5px] border-[#37383E]" ref={chartWrapperRef}>
          <CPUChart chartWidth={chartWidth} scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} />
          <MemoryChart chartWidth={chartWidth} scaleX={scrollbarScaleX} startTime={startTime} endTime={endTime} />
        </div>
      </div>

      <div className="grid grid-cols-[auto_1fr]">
        <div className="w-48" />

        {/* horizontal scrollbar */}
        <HorizontalScrollBar
          chartWidth={chartWidth}
          scrollBarTwoPosX={scrollBarTwoPosX}
          setScrollBarTwoPosX={setScrollBarTwoPosX}
        />
      </div>
    </section>
  )
}

export default TimelineSection

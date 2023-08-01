import React, { useEffect, useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'

import AreaChart from './components/AreaChart'
import HorizontalScrollBar from './components/HorizontalScrollBar'
import { AreaChartData } from './types'

function getRandomInt(_min: number, _max: number) {
  const min = Math.ceil(_min)
  const max = Math.floor(_max)
  return Math.floor(Math.random() * (max - min)) + min
}

const sampleData: AreaChartData = new Array(1000)
  .fill(0)
  .map(() => ({
    date: new Date(new Date().getTime() + getRandomInt(0, 1000)),
    value: getRandomInt(0, 100),
  }))
  .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())

/**
 * 타임라인 차트 영역
 */
const TimelineSection: React.FC = () => {
  const chartWrapperRef = useRef<HTMLDivElement | null>(null)
  const [chartWidth, setChartWidth] = useState<number | null>(null)
  const [scrollBarTwoPosX, setScrollBarTwoPosX] = useState<[number, number] | null>(null)

  // 전체 스케일
  const timelineScaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!chartWidth) return null
    return d3
      .scaleTime()
      .domain([sampleData[0].date, sampleData[sampleData.length - 1].date])
      .range([0, chartWidth])
  }, [chartWidth, sampleData])

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
    <section className="h-full bg-black grid grid-cols-1 grid-rows-[auto_1fr_auto] gap-1 p-2">
      {/* time */}
      <div className="text-white">time</div>

      {/* chart */}
      <div className="grid grid-cols-1 gap-y-2 overflow-y-auto overflow-x-hidden">
        <AreaChart
          chartWrapperRef={chartWrapperRef}
          chartWidth={chartWidth}
          scaleX={scrollbarScaleX}
          data={sampleData}
        />
        <AreaChart
          chartWrapperRef={chartWrapperRef}
          chartWidth={chartWidth}
          scaleX={scrollbarScaleX}
          data={sampleData}
        />
      </div>

      {/* horizontal scrollbar */}
      <HorizontalScrollBar
        chartWidth={chartWidth}
        scrollBarTwoPosX={scrollBarTwoPosX}
        setScrollBarTwoPosX={setScrollBarTwoPosX}
      />
    </section>
  )
}

export default TimelineSection

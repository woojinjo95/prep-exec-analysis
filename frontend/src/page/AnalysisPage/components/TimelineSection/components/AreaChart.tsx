import React, { useEffect, useRef, useState, useMemo } from 'react'
import * as d3 from 'd3'

import { AreaChartGenerator } from '../usecase'
import { AreaChartData } from '../types'

interface AreaChartProps {
  chartWidth: number | null
  chartWrapperRef: React.MutableRefObject<HTMLDivElement | null>
  scaleX: d3.ScaleTime<number, number, never> | null
  data: AreaChartData
}

/**
 * 영역 차트
 *
 * TODO: resizing event
 */
const AreaChart: React.FC<AreaChartProps> = ({ chartWidth, chartWrapperRef, scaleX, data }) => {
  const chartRef = useRef<HTMLDivElement | null>(null)
  const [chartHeight, setChartHeight] = useState<number | null>(null)

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (!chartHeight) return null
    return d3.scaleLinear().domain([0, 100]).range([chartHeight, 0])
  }, [chartHeight])

  useEffect(() => {
    if (!chartWrapperRef.current) return
    setChartHeight(chartWrapperRef.current.clientHeight)
  }, [])

  useEffect(() => {
    if (!chartRef.current || !chartWidth || !chartHeight || !scaleX || !scaleY) return

    const chart = new AreaChartGenerator(chartRef.current, data, chartWidth, chartHeight, scaleX, scaleY)
    chart.createChart()
  }, [chartWidth, chartHeight, scaleX, scaleY])

  return (
    <div className="grid grid-cols-1 grid-rows-[auto_1fr] h-40">
      <span className="sticky top-0 text-xs text-gray-400 z-10 px-1">CPU</span>

      <div ref={chartWrapperRef} className="border-l-[0.5px] border-r-[0.5px] border-[#37383E]">
        <div ref={chartRef} className="brightness-150" />
      </div>
    </div>
  )
}

export default AreaChart

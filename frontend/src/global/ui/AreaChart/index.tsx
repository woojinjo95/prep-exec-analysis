import React, { useEffect, useRef, useMemo } from 'react'
import * as d3 from 'd3'

import { AreaChartData } from '@global/types'
import { CHART_HEIGHT } from '@global/constant'
import { AreaChartGenerator } from './usecase'

interface AreaChartProps {
  chartWidth?: number | null
  scaleX: d3.ScaleTime<number, number, never> | null
  data: AreaChartData
  minValue?: number
  maxValue?: number
  strokeColor?: string
  fillColor?: string
}

/**
 * 영역 차트
 *
 * TODO: resizing event
 */
const AreaChart: React.FC<AreaChartProps> = ({
  chartWidth,
  scaleX,
  data,
  minValue: _minValue,
  maxValue: _maxValue,
  strokeColor,
  fillColor,
}) => {
  const chartRef = useRef<HTMLDivElement | null>(null)
  const minValue = useMemo(
    () => (_minValue !== undefined ? _minValue : Math.min(...data.map(({ value }) => value))),
    [],
  )
  const maxValue = useMemo(
    () => (_maxValue !== undefined ? _maxValue : Math.max(...data.map(({ value }) => value))),
    [],
  )

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([minValue, maxValue]).range([CHART_HEIGHT, 0]),
    [data, minValue, maxValue],
  )

  useEffect(() => {
    if (!chartRef.current || !chartWidth || !scaleX || !scaleY) return

    const chart = new AreaChartGenerator(
      chartRef.current,
      data,
      chartWidth,
      CHART_HEIGHT,
      scaleX,
      scaleY,
      minValue,
      strokeColor,
      fillColor,
    )
    chart.createChart()
  }, [chartWidth, scaleX, scaleY])

  return (
    <div style={{ height: CHART_HEIGHT }}>
      <div ref={chartRef} className="brightness-150" />
    </div>
  )
}

export default React.memo(AreaChart)

import React, { useMemo } from 'react'
import * as d3 from 'd3'
import { AreaChart } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { useMemory } from '../api/hook'

interface MemoryChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * Memory 사용률 차트
 */
const MemoryChart: React.FC<MemoryChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const { memory } = useMemory({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const memoryUsage = useMemo(() => {
    if (!memory) return null
    return memory.map(({ timestamp, memory_usage }) => ({
      datetime: new Date(timestamp).getTime(),
      value: Number(memory_usage),
    }))
  }, [memory])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([0, 100]).range([CHART_HEIGHT, 0]),
    [],
  )

  if (!memoryUsage) return <div />
  return (
    <AreaChart
      chartWidth={dimension?.width}
      scaleX={scaleX}
      scaleY={scaleY}
      data={memoryUsage}
      minValue={0}
      strokeColor="#fa70d8"
      fillColor="#fa70d8"
    />
  )
}

export default MemoryChart

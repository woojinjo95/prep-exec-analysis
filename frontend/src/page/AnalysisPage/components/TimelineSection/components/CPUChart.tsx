import React, { useMemo } from 'react'
import * as d3 from 'd3'
import { AreaChart } from '@global/ui'
import { CHART_HEIGHT } from '@global/constant'
import { useCPU } from '../api/hook'

interface CPUChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * CPU 사용률 차트
 */
const CPUChart: React.FC<CPUChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const { cpu } = useCPU({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const cpuData = useMemo(() => {
    if (!cpu) return null
    return cpu.map(({ timestamp, cpu_usage }) => ({
      datetime: new Date(timestamp).getTime(),
      value: Number(cpu_usage),
    }))
  }, [cpu])

  const scaleY: d3.ScaleLinear<number, number, never> | null = useMemo(
    () => d3.scaleLinear().domain([0, 100]).range([CHART_HEIGHT, 0]),
    [],
  )

  if (!cpuData) return <div />
  return (
    <AreaChart
      chartWidth={dimension?.width}
      scaleX={scaleX}
      scaleY={scaleY}
      data={cpuData}
      minValue={0}
      strokeColor="#f29213"
      fillColor="#f29213"
    />
  )
}

export default CPUChart

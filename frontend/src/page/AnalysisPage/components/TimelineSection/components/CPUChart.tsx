import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
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
    return cpu.map(({ timestamp, cpu_usage }) => ({ date: new Date(timestamp), value: Number(cpu_usage) }))
  }, [cpu])

  if (!cpuData) return <div />
  return (
    <AreaChart
      chartWidth={dimension?.width}
      scaleX={scaleX}
      data={cpuData}
      minValue={0}
      maxValue={100}
      strokeColor="#f29213"
      fillColor="#f29213"
    />
  )
}

export default React.memo(CPUChart)

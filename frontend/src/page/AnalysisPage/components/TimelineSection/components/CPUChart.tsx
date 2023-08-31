import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
import { useCPU } from '../api/hook'

interface CPUChartProps {
  chartWidth: Parameters<typeof AreaChart>[0]['chartWidth']
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * CPU 사용률 차트
 */
const CPUChart: React.FC<CPUChartProps> = ({ chartWidth, scaleX, startTime, endTime }) => {
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
      chartWidth={chartWidth}
      scaleX={scaleX}
      data={cpuData}
      minValue={0}
      maxValue={100}
      strokeColor="#f29213"
      fillColor="#f29213"
    />
  )
}

export default CPUChart

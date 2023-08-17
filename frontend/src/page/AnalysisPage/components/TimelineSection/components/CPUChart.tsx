import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
import { useCPUAndMemory } from '../api/hook'

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
  const { cpuAndMemory } = useCPUAndMemory({ start_time: startTime.toISOString(), end_time: endTime.toISOString() })

  const cpuUsage = useMemo(() => {
    if (!cpuAndMemory) return null
    return cpuAndMemory.map(({ timestamp, cpu_usage }) => ({ date: new Date(timestamp), value: cpu_usage }))
  }, [cpuAndMemory])

  if (!cpuUsage) return <div />
  return <AreaChart chartWidth={chartWidth} scaleX={scaleX} data={cpuUsage} minValue={0} maxValue={100} />
}

export default CPUChart

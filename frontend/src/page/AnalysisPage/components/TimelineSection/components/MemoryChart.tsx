import { AreaChart } from '@global/ui'
import React, { useMemo } from 'react'
import useWebsocket from '@global/module/websocket'
import { useCPUAndMemory } from '../api/hook'

interface MemoryChartProps {
  chartWidth: Parameters<typeof AreaChart>[0]['chartWidth']
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * Memory 사용률 차트
 */
const MemoryChart: React.FC<MemoryChartProps> = ({ chartWidth, scaleX, startTime, endTime }) => {
  const { cpuAndMemory, refetch } = useCPUAndMemory({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  const memoryUsage = useMemo(() => {
    if (!cpuAndMemory) return null
    return cpuAndMemory.map(({ timestamp, memory_usage }) => ({ date: new Date(timestamp), value: memory_usage }))
  }, [cpuAndMemory])

  if (!memoryUsage) return <div />
  return (
    <AreaChart
      chartWidth={chartWidth}
      scaleX={scaleX}
      data={memoryUsage}
      minValue={0}
      maxValue={100}
      strokeColor="#fa70d8"
      fillColor="#fa70d8"
    />
  )
}

export default MemoryChart

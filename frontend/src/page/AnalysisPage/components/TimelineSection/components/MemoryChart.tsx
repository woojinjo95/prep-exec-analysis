import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
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
    return memory.map(({ timestamp, memory_usage }) => ({ date: new Date(timestamp), value: Number(memory_usage) }))
  }, [memory])

  if (!memoryUsage) return <div />
  return (
    <AreaChart
      chartWidth={dimension?.width}
      scaleX={scaleX}
      data={memoryUsage}
      minValue={0}
      maxValue={100}
      strokeColor="#fa70d8"
      fillColor="#fa70d8"
    />
  )
}

export default React.memo(MemoryChart)

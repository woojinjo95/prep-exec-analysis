import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useMemory } from '../api/hook'

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
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { memory } = useMemory({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    testrun_id: testRunId || undefined,
  })

  const memoryUsage = useMemo(() => {
    if (!memory) return null
    return memory.map(({ timestamp, memory_usage }) => ({ date: new Date(timestamp), value: Number(memory_usage) }))
  }, [memory])

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

export default React.memo(MemoryChart)

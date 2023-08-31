import React, { useMemo } from 'react'
import { useRecoilValue } from 'recoil'
import { AreaChart } from '@global/ui'
import { scenarioIdState } from '@global/atom'
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
  const scenarioId = useRecoilValue(scenarioIdState)
  const { cpu } = useCPU({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    // FIXME: 동적으로 주입되도록 변경 필요
    testrun_id: '2023-08-14T054428F718593',
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

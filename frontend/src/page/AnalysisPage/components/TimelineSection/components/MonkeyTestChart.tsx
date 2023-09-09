import React, { useMemo } from 'react'
import { useMonkeySection } from '@page/AnalysisPage/api/hook'
import { RangeChart } from '@global/ui'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'

interface MonkeyTestChartProps {
  scaleX: Parameters<typeof RangeChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
  summary: AnalysisResultSummary
}

/**
 * Monkey Test 차트
 */
const MonkeyTestChart: React.FC<MonkeyTestChartProps> = ({ scaleX, startTime, endTime, dimension, summary }) => {
  const { monkeySection } = useMonkeySection({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const monkeyTestData = useMemo(() => {
    if (!monkeySection) return null
    return monkeySection.map(({ start_timestamp, end_timestamp }) => ({
      datetime: new Date(start_timestamp).getTime(),
      duration: new Date(end_timestamp).getTime() - new Date(start_timestamp).getTime(),
      color: summary.monkey_test?.color || 'white',
    }))
  }, [monkeySection, summary])

  if (!monkeyTestData) return <div />
  return (
    <div>
      <RangeChart scaleX={scaleX} data={monkeyTestData} />
    </div>
  )
}

export default MonkeyTestChart

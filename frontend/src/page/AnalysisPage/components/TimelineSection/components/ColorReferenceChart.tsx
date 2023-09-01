import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useColorReferences } from '../api/hook'

interface ColorReferenceChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  chartWidth: Parameters<typeof AreaChart>[0]['chartWidth']
  startTime: Date
  endTime: Date
}

/**
 * Color Reference 차트
 */
const ColorReferenceChart: React.FC<ColorReferenceChartProps> = ({ scaleX, chartWidth, startTime, endTime }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { colorReferences } = useColorReferences({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    testrun_id: testRunId || undefined,
  })

  const colorReferenceData = useMemo(() => {
    if (!colorReferences) return null
    return colorReferences.map(({ timestamp, color_reference }) => ({
      date: new Date(timestamp),
      value: color_reference,
    }))
  }, [colorReferences])

  if (!colorReferenceData) return <div />
  return <AreaChart chartWidth={chartWidth} scaleX={scaleX} data={colorReferenceData} minValue={0} maxValue={8} />
}

export default ColorReferenceChart

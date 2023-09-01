import { scenarioIdState, testRunIdState } from '@global/atom'
import { AreaChart } from '@global/ui'
import React, { useMemo } from 'react'
import { useRecoilValue } from 'recoil'
import { useLoudness } from '../api/hook'

interface LoudnessChartProps {
  chartWidth: Parameters<typeof AreaChart>[0]['chartWidth']
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * Loudness(소리) 변화 차트
 */
const LoudnessChart: React.FC<LoudnessChartProps> = ({ chartWidth, scaleX, startTime, endTime }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { loudness } = useLoudness({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    testrun_id: testRunId || undefined,
  })

  const loudnessData = useMemo(() => {
    if (!loudness) return null
    return loudness.map(({ timestamp, m }) => ({
      date: new Date(timestamp),
      value: m,
    }))
  }, [loudness])

  if (!loudnessData) return <div />
  return (
    <AreaChart
      chartWidth={chartWidth}
      scaleX={scaleX}
      data={loudnessData}
      minValue={-70}
      maxValue={0}
      strokeColor="#0106FF"
      fillColor="#686ade"
    />
  )
}

export default LoudnessChart

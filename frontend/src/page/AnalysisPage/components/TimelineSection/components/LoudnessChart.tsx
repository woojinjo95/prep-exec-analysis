import React, { useMemo } from 'react'
import { AreaChart } from '@global/ui'
import { useLoudness } from '../api/hook'

interface LoudnessChartProps {
  scaleX: Parameters<typeof AreaChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * Loudness(소리) 변화 차트
 */
const LoudnessChart: React.FC<LoudnessChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const { loudness } = useLoudness({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
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
      chartWidth={dimension?.width}
      scaleX={scaleX}
      data={loudnessData}
      minValue={-70}
      maxValue={0}
      strokeColor="#0106FF"
      fillColor="#686ade"
    />
  )
}

export default React.memo(LoudnessChart)

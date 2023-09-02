import React, { useMemo } from 'react'
import { PointChart, RangeChart } from '@global/ui'
import { useFreeze } from '../api/hook'

interface FreezeChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * Video Analysis Result(freeze) 차트
 */
const FreezeChart: React.FC<FreezeChartProps> = ({ scaleX, startTime, endTime }) => {
  const { freeze } = useFreeze({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const freezeData = useMemo(() => {
    if (!freeze) return null
    return freeze.map(({ timestamp, duration }) => ({ date: new Date(timestamp), duration: duration * 1000 }))
  }, [freeze])

  if (!freezeData) return <div />
  return <RangeChart scaleX={scaleX} data={freezeData} color="blue" />
}

export default React.memo(FreezeChart)

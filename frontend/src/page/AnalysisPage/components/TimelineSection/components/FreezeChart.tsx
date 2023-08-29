import { PointChart } from '@global/ui'
import React, { useMemo } from 'react'
import { useWebsocket } from '@global/hook'
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
  const { freeze, refetch } = useFreeze({ start_time: startTime.toISOString(), end_time: endTime.toISOString() })
  useWebsocket({
    onMessage: (message) => {
      if (message.msg === 'analysis_response') {
        refetch()
      }
    },
  })

  const freezeData = useMemo(() => {
    if (!freeze) return null
    return freeze.map(({ timestamp }) => new Date(timestamp))
  }, [freeze])

  if (!freezeData) return <div />
  return <PointChart scaleX={scaleX} data={freezeData} />
}

export default FreezeChart

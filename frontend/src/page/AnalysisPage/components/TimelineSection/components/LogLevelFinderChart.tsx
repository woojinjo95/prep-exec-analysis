import { PointChart } from '@global/ui'
import React, { useMemo } from 'react'
import { useWebsocket } from '@global/hook'
import { useLogLevelFinders } from '../api/hook'

interface LogLevelFinderChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * Log Level Finder 차트
 */
const LogLevelFinderChart: React.FC<LogLevelFinderChartProps> = ({ scaleX, startTime, endTime }) => {
  const { logLevelFinders, refetch } = useLogLevelFinders({
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

  const logLevelFinderData = useMemo(() => {
    if (!logLevelFinders) return null
    return logLevelFinders.map(({ timestamp }) => new Date(timestamp))
  }, [logLevelFinders])

  if (!logLevelFinderData) return <div />
  return <PointChart scaleX={scaleX} data={logLevelFinderData} color="red" />
}

export default LogLevelFinderChart

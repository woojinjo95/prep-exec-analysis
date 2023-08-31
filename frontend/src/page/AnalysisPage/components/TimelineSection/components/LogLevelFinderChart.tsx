import { PointChart } from '@global/ui'
import React, { useMemo } from 'react'
import { scenarioIdState } from '@global/atom'
import { useRecoilValue } from 'recoil'
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
  const scenarioId = useRecoilValue(scenarioIdState)
  const { logLevelFinders } = useLogLevelFinders({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    // FIXME: 동적으로 주입되도록 변경 필요
    testrun_id: '2023-08-14T054428F718593',
  })

  const logLevelFinderData = useMemo(() => {
    if (!logLevelFinders) return null
    return logLevelFinders.map(({ timestamp }) => new Date(timestamp))
  }, [logLevelFinders])

  if (!logLevelFinderData) return <div />
  return <PointChart scaleX={scaleX} data={logLevelFinderData} color="red" />
}

export default LogLevelFinderChart

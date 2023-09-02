import { PointChart } from '@global/ui'
import React, { useMemo } from 'react'
import { scenarioIdState, testRunIdState } from '@global/atom'
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
  const testRunId = useRecoilValue(testRunIdState)
  const { logLevelFinders } = useLogLevelFinders({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    testrun_id: testRunId || undefined,
  })

  const logLevelFinderData = useMemo(() => {
    if (!logLevelFinders) return null
    return logLevelFinders.map(({ timestamp }) => new Date(timestamp))
  }, [logLevelFinders])

  if (!logLevelFinderData) return <div />
  return <PointChart scaleX={scaleX} data={logLevelFinderData} color="red" />
}

export default React.memo(LogLevelFinderChart)

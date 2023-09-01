import React, { useMemo } from 'react'
import { PointChart } from '@global/ui'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState } from '@global/atom'
import { useEventLogs } from '../api/hook'

interface EventLogChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
}

/**
 * 이벤트 로그 차트
 */
const EventLogChart: React.FC<EventLogChartProps> = ({ scaleX, startTime, endTime }) => {
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const { eventLogs } = useEventLogs({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
    scenario_id: scenarioId || undefined,
    testrun_id: testRunId || undefined,
  })

  const eventLogsData = useMemo(() => {
    if (!eventLogs) return null
    return eventLogs.map(({ timestamp }) => new Date(timestamp))
  }, [eventLogs])

  if (!eventLogsData) return <div />
  return <PointChart scaleX={scaleX} data={eventLogsData} />
}

export default EventLogChart

import React, { useMemo } from 'react'
import { PointChart } from '@global/ui'
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
  const { eventLogs } = useEventLogs({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const eventLogsData = useMemo(() => {
    if (!eventLogs) return null
    return eventLogs.map(({ timestamp }) => new Date(timestamp))
  }, [eventLogs])

  if (!eventLogsData) return <div />
  return <PointChart scaleX={scaleX} data={eventLogsData} />
}

export default React.memo(EventLogChart)

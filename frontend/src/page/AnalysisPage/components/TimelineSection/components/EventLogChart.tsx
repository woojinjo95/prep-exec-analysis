import React, { useMemo } from 'react'
import { PointChart, Text, TimelineTooltip } from '@global/ui'
import { useEventLogs } from '../api/hook'
import { useTooltipEvent } from '../hook'

interface EventLogChartProps {
  scaleX: Parameters<typeof PointChart>[0]['scaleX']
  startTime: Date
  endTime: Date
  dimension: { left: number; width: number } | null
}

/**
 * 이벤트 로그 차트
 */
const EventLogChart: React.FC<EventLogChartProps> = ({ scaleX, startTime, endTime, dimension }) => {
  const { eventLogs } = useEventLogs({
    start_time: startTime.toISOString(),
    end_time: endTime.toISOString(),
  })

  const eventLogsData = useMemo(() => {
    if (!eventLogs) return null
    return eventLogs.map(({ timestamp, msg }) => ({ datetime: new Date(timestamp).getTime(), message: msg }))
  }, [eventLogs])

  const { posX, tooltipData, onMouseMove, onMouseLeave } = useTooltipEvent<NonNullable<typeof eventLogsData>[number]>({
    scaleX,
    offsetLeft: dimension?.left,
    width: dimension?.width,
  })

  if (!eventLogsData) return <div />
  return (
    <div onMouseMove={onMouseMove(eventLogsData)} onMouseLeave={onMouseLeave} className="relative">
      {!!posX && (
        <TimelineTooltip posX={posX} data={tooltipData}>
          <table className="border-t border-l border-charcoal">
            <tr>
              <th className="border-r border-b border-charcoal bg-charcoal py-2 px-4 text-left">
                <Text colorScheme="light" weight="medium">
                  Event Log
                </Text>
              </th>
              <td className="border-r border-b border-charcoal py-2 px-4 text-left">
                {/* TODO: 메시지 형식 확정 필요(기획) */}
                <Text colorScheme="light">{tooltipData?.message}</Text>
              </td>
            </tr>
          </table>
        </TimelineTooltip>
      )}

      <PointChart scaleX={scaleX} data={eventLogsData} />
    </div>
  )
}

export default EventLogChart

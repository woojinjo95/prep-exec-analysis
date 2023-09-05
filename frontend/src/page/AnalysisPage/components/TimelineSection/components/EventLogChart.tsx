import React, { useMemo, useRef } from 'react'
import { PointChart, Text, TimelineTooltip, TimelineTooltipItem } from '@global/ui'
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
  const wrapperRef = useRef<HTMLDivElement | null>(null)
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
        <div
          ref={wrapperRef}
          className="absolute top-0 h-full w-1 bg-white opacity-30 z-[5]"
          style={{
            transform: `translateX(${posX - 2}px)`,
          }}
        >
          {!!tooltipData && (
            <TimelineTooltip posX={posX} data={tooltipData} wrapperRef={wrapperRef}>
              <TimelineTooltipItem label="Event Log">
                {/* FIXME: 메시지 형식 확정 필요(기획) */}
                <Text colorScheme="light">{tooltipData.message}</Text>
              </TimelineTooltipItem>
            </TimelineTooltip>
          )}
        </div>
      )}

      <PointChart scaleX={scaleX} data={eventLogsData} />
    </div>
  )
}

export default EventLogChart
